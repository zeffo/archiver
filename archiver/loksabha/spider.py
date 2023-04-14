from typing import Any
from yarl import URL
from httpx import AsyncClient
import asyncio
import time
import logging
from archiver.spider import BaseSpider
from archiver.models import LokSabhaQuestion

logger = logging.getLogger("archiver")

class Spider(BaseSpider[LokSabhaQuestion]):
    BASE_URL = "https://eparlib.nic.in/restv3/fetch/all?collectionId=3"
    PAGE_SIZE = 100

    def get_url(self, *, loksabha_no: int, search_string: str, page_no: int = 0) -> URL:
        params = {
            "loksabhaNo": loksabha_no,
            "anyWhere": search_string,
            "start": page_no * self.PAGE_SIZE,
            "rows": self.PAGE_SIZE
        }
        url = URL(self.BASE_URL) % params
        return url

    def get_total_records(self, data: dict[str, Any]) -> int:
        return int(data.get("rowsCount", 0))

    async def get_page(self, client: AsyncClient, *, loksabha_no: int, search_string: str, page_no: int):
        url = self.get_url(loksabha_no=loksabha_no, search_string=search_string, page_no=page_no)
        resp = await client.get(str(url))
        return resp.json()
    
    async def parse(self, data: dict[str, Any]):
        for raw in data["records"]:
            item = LokSabhaQuestion(**raw)
            asyncio.create_task(self.process_item(item))

    async def parse_page(self, client: AsyncClient, *, loksabha_no: int, search_string: str, page_no: int):
        page = await self.get_page(client, loksabha_no=loksabha_no, search_string=search_string, page_no=page_no)
        await self.parse(page)
        
    async def run(self, search_string: str):
        start = time.perf_counter()
        async with AsyncClient() as client:
            tasks: list[asyncio.Task[Any]] = []
            for lok_no in range(1, 18):
                initial = await self.get_page(client, loksabha_no=lok_no, search_string=search_string, page_no=0)
                await self.parse(initial)
                pages = self.get_total_records(initial) // self.PAGE_SIZE
                for i in range(1, pages):
                    coro = self.parse_page(client, loksabha_no=lok_no, search_string=search_string, page_no=i)
                    task = asyncio.create_task(coro)
                    tasks.append(task)
            await asyncio.gather(*tasks)
        logger.info(f"Processed {len(self.items)} in {time.perf_counter() - start}ms.")

