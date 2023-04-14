from .models import LokSabhaQuestion, RajyaSabhaQuestion
from typing import TypeVar, Generic
from logging import getLogger

T = TypeVar("T", LokSabhaQuestion, RajyaSabhaQuestion)

logger = getLogger("archiver")

class BaseSpider(Generic[T]):

    def __init__(self):
        self.items: list[T] = []

    async def process_item(self, item: T):
        if isinstance(item, LokSabhaQuestion):
            logger.debug(f"Processing Lok Sabha item {item.number}: {item.subject}\nDate: {item.date.strftime('%d-%m-%Y')} ({item.loksabhaNo}, session {item.sessionNo})\n")
        else:
            logger.debug(f"Processing item {item.number}: {item.subject}\nDate: {item.date.strftime('%d-%m-%Y')}")
        self.items.append(item)
