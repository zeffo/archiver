from scrapy import Spider
from archiver.settings import SEARCH_TERMS


class BaseSpider(Spider):
    search_terms = SEARCH_TERMS
    URL: str
