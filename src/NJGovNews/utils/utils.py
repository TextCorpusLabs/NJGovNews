import protego
import time
from .const import *
from typeguard import typechecked

@typechecked
def take_a_nap(rtxt: protego.Protego) -> None:
    delay = rtxt.crawl_delay(USER_AGENT)
    delay = delay if delay is not None else WEB_DELAY
    time.sleep(delay)
