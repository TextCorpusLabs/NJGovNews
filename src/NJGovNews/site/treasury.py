from fileinput import filename
import json
import jsonlines
import pathlib
import progressbar as pb
import typing as t
from typeguard import typechecked

@typechecked
def scrape(file_out: pathlib.Path) -> None:
    print('---------')
    print('SITE: treasury')
    print(f'file_out: {str(file_out)}')
    print('---------')
