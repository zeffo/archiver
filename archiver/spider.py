from scrapy import Spider
from archiver.settings import SEARCH_TERMS


class BaseSpider(Spider):
    search_terms = SEARCH_TERMS

    def log_error(self, data):
        self.logger.error(f"ERROR PARSING QUESTION:\n{data}")
