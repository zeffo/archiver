from scrapy import Spider, Request
from typing import Protocol, runtime_checkable

from scrapy.http import TextResponse

from archiver.items import Question
from archiver.settings import SEARCH_TERMS


@runtime_checkable
class SpiderProtocol(Protocol):

    search_terms = SEARCH_TERMS

    URL: str

    def start_requests(self):
        req = Request(self.URL)
        yield req

    def get_data(self, response: TextResponse) -> list[Question]:
        raise NotImplementedError

    def get_total_pages(self, response: TextResponse) -> int:
        raise NotImplementedError


class BaseSpider(Spider):

    def __init_subclass__(cls) -> None:
        if not isinstance(cls, SpiderProtocol):
            raise TypeError(f"{cls.__name__} must implement SpiderProtocol!")


