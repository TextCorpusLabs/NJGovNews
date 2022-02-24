import protego
import requests
import time
from .const import *
from typeguard import typechecked

@typechecked
def nap_if_needed(response: requests.Response,  rtxt: protego.Protego) -> None:
    if not response.from_cache:
        delay = rtxt.crawl_delay(USER_AGENT)
        delay = delay if delay is not None else WEB_DELAY
        time.sleep(delay)
