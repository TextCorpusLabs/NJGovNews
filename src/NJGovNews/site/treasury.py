import pathlib
import progressbar as pb
import protego
import requests_cache as requests
import tempfile
import typing as t
from ..utils import const, nap_if_needed
from lxml import etree
from typeguard import typechecked

URL_ROOT = f"{const.URL_TLD}/treasury"
URL_LIST = f"{URL_ROOT}/news.shtml"
XPATH_LIST  = f"//div[@class='card']/div/table/tbody/tr/td[2]/a[1]"

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
        _get_news_documents(urls, session, rtxt)


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

def _get_news_documents(urls: t.List[str], session: requests.session, rtxt: protego.Protego):
    pb_i = 1
    widgets = [ 'Retrieving news item ', pb.Counter(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']'), ' ', pb.Timer()]
    with pb.ProgressBar(widgets = widgets) as bar:
        for url in urls:
            bar.update(pb_i)
            _get_news_document(url, session, rtxt)
            pb_i =  pb_i + 1       
    pass

@typechecked
def _get_news_document(url: str, session: requests.session, rtxt: protego.Protego):
    if rtxt.can_fetch(const.USER_AGENT, url):
        with session.get(url) as response:
            nap_if_needed(response, rtxt)
            if response.status_code == 200:
                tree = _get_doc_model(response)
            else:
                print('Failed to retrieve {url}')
    else:
        print('Forbiden from retrieving {url}')
