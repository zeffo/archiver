from scrapy import Spider

from .base import SpiderProtocol


class LokSabhaSpider(Spider, SpiderProtocol):
    def get_pages(self):
        ...
