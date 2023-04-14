from .models import LokSabhaQuestion, RajyaSabhaQuestion
from typing import TypeVar, Generic, Any
from logging import getLogger
import httpx

T = TypeVar("T", LokSabhaQuestion, RajyaSabhaQuestion)

logger = getLogger("archiver")

class BaseSpider(Generic[T]):

    def __init__(self):
        self.items: list[T] = []
        self.client = httpx.AsyncClient()

    async def __aenter__(self):
        return self
        
    async def __aexit__(self, *args: Any):
        await self.client.aclose()


    async def process_item(self, item: T):
        if isinstance(item, LokSabhaQuestion):
            logger.debug(f"Processing Lok Sabha item {item.number}: {item.subject}\nDate: {item.date.strftime('%d-%m-%Y')} ({item.loksabhaNo}, session {item.sessionNo})\n")
        else:
            logger.debug(f"Processing item {item.number}: {item.subject}\nDate: {item.date.strftime('%d-%m-%Y')}")
        self.items.append(item)
