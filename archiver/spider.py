from .models import LokSabhaQuestion, RajyaSabhaQuestion
from typing import TypeVar, Generic
from logging import getLogger

T = TypeVar("T", LokSabhaQuestion, RajyaSabhaQuestion)

logger = getLogger("archiver")

class BaseSpider(Generic[T]):

    def __init__(self):
        self.items: list[T] = []

    async def process_item(self, item: T):
        logger.debug(f"Processing {item.number}: {item.subject}, {item.date.strftime('%d-%m-%Y')})")
        self.items.append(item)
