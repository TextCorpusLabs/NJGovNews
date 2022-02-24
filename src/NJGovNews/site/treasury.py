import csv
import pathlib
import progressbar as pb
import protego
import requests_cache as requests
import tempfile
import typing as t
from ..utils import const, nap_if_needed
from collections import namedtuple
from lxml import etree
from typeguard import typechecked

URL_ROOT = f"{const.URL_TLD}/treasury"
URL_LIST = f"{URL_ROOT}/news.shtml"
XPATH_LIST  = f"//div[@class='card']/div/table/tbody/tr/td[2]/a[1]"
XPATH_DATE = "//div[@class='container bg-light']/div/div/div[2]/div[1]/br"
XPATH_CONTACT = "//div[@class='container bg-light']/div/div/div[2]/div[2]/br[1]"
XPATH_PHONE = "//div[@class='container bg-light']/div/div/div[2]/div[2]/br[2]"
XPATH_TITLE = "//div[@class='container bg-light']/div/div/div[3]/div/center/strong"
XPATH_BODY = "//div[@class='container bg-light']/div/div/div[3]/div/p"

NewsArticle = namedtuple('NewsArticle', 'url date contact phone title body')

@typechecked
def scrape(file_out: pathlib.Path) -> None:
    print('---------')
    print('SITE: Department of the Treasury')
    print(f'file_out: {str(file_out)}')
    print('---------')
    file_out.parent.mkdir(parents = True, exist_ok = True)
    cache = file_out.parent.joinpath('./treasury.cache.sqlite')
    no_cache = {const.URL_ROBOTS: 0, URL_LIST: 0}    
    with requests.CachedSession(cache, backend = 'sqlite', urls_expire_after = no_cache) as session:
        session.headers['User-Agent'] = const.USER_AGENT
        rtxt = _get_robots(session)
        urls = _get_news_list(session, rtxt)
        urls = [f'{URL_ROOT}/{url}' for url in urls]
        docs = _get_news_documents(urls, session, rtxt)
        _save_documents(docs, file_out)

@typechecked
def _get_robots(session: requests.session) -> protego.Protego:
    print('Retrieving robots.txt ...')
    with session.get(const.URL_ROBOTS) as response:            
        rtxt = protego.Protego.parse(response.text)
        nap_if_needed(response, rtxt)
    return rtxt

@typechecked
def _get_news_list(session: requests.session, rtxt: protego.Protego) -> t.List[str]:
    print('Retrieving news feed ...')
    results = []
    if rtxt.can_fetch(const.USER_AGENT, URL_LIST):
        with session.get(URL_LIST) as response:
            nap_if_needed(response, rtxt)
            if response.status_code == 200:
                tree = _get_doc_model(response)
                nodes = tree.findall(XPATH_LIST)
                results = [node.attrib['href'] for node in nodes]
                results = [url for url in results if url.startswith('news/') and url.endswith('.shtml')]
            else:
                print('Failed to retrieve {URL_LIST}')
    else:
        print('Forbiden from retrieving {URL_LIST}')
    return results

@typechecked
def _get_doc_model(response: requests.response) -> etree:
    with tempfile.TemporaryFile('x+', encoding = response.encoding) as fp:
        fp.write(response.text)
        fp.flush()
        fp.seek(0)
        tree = etree.parse(fp, etree.HTMLParser())
    return tree

def _get_news_documents(urls: t.List[str], session: requests.session, rtxt: protego.Protego) -> t.Iterator[NewsArticle]:
    pb_i = 1
    widgets = [ 'Retrieving news item ', pb.Counter(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']'), ' ', pb.Timer()]
    with pb.ProgressBar(widgets = widgets) as bar:
        for url in urls:
            bar.update(pb_i)
            yield _get_news_document(url, session, rtxt)
            pb_i =  pb_i + 1

@typechecked
def _get_news_document(url: str, session: requests.session, rtxt: protego.Protego) -> NewsArticle:
    strip = lambda x: x.strip()
    get_tail = lambda x: _optional(x.tail, strip)
    get_text = lambda x: _optional(x.text, strip)
    if rtxt.can_fetch(const.USER_AGENT, url):
        with session.get(url) as response:
            nap_if_needed(response, rtxt)
            if response.status_code == 200:
                tree = _get_doc_model(response)
                date = _optional(tree.find(XPATH_DATE), get_tail)
                contact = _optional(tree.find(XPATH_CONTACT), get_tail)
                phone = _optional(tree.find(XPATH_PHONE), get_tail)
                title = _optional(tree.find(XPATH_TITLE), get_text)
                body = _process_body(tree.findall(XPATH_BODY))
                return NewsArticle(url, date, contact, phone, title, body)
            else:
                print('Failed to retrieve {url}')
    else:
        print('Forbiden from retrieving {url}')

@typechecked
def _optional(root: t.Any, func: t.Callable) -> t.Optional[str]:
    if root == None:
        return None
    else:
        return func(root)

@typechecked
def _process_body(nodes: t.List[etree.Element]) -> t.List[str]:
    body = [[text.strip() for text in node.itertext()] for node in nodes]
    body = [[frag for frag in para if len(frag) > 0] for para in body]
    body = [' '.join(para) for para in body if len(para) > 0]
    return body

@typechecked
def _save_documents(docs:t.Iterator[NewsArticle], file_out: pathlib.Path) -> None:
    with open(file_out, 'w', encoding = 'utf-8', newline = '') as file_out:
        writer = csv.writer(file_out, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
        writer.writerow(['url', 'date', 'contact', 'phone', 'title', 'body'])
        for doc in docs:
            writer.writerow([doc.url, doc.date, doc.contact, doc.phone, doc.title, '\n'.join(doc.body)])
