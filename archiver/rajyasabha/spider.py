import asyncio
import logging
import time
from typing import Any

from archiver.models import RajyaSabhaQuestion
from archiver.spider import BaseSpider

logger = logging.getLogger("archiver")


class RajyaSabhaSpider(BaseSpider[RajyaSabhaQuestion]):
    BASE_URL = "https://rsdoc.nic.in/Question/Search_Questions"

    def get_url(self, search_string: str, *, fields: list[str] = ["qtitle"]) -> str:
        clauses: list[str] = []
        for field in fields:
            clauses.append(f"{field} LIKE '%{search_string}%'")
        clause = " OR ".join(clauses)
        return f"{self.BASE_URL}?whereclause=({clause})"

    async def get_page(self, search_string: str):
        url = self.get_url(search_string)
        headers = {"Content-Type": "application/json"}
        resp = await self.client.get(url, headers=headers)
        data: dict[str, Any] | list[dict[str, Any]] = resp.json()
        if isinstance(data, dict) and data.get("ErrorCode"):
            return None
        elif isinstance(data, list):
            return data

    async def parse(self, data: list[dict[str, Any]]):
        """Parses the response json and concurrently processes the items.

        Parameters
        ----------
        data: :class:`dict[str, Any]`
            The JSON response data.

        """
        tasks: list[asyncio.Task[None]] = []
        for raw in data:
            item = RajyaSabhaQuestion(**raw)
            task = asyncio.create_task(self.process_item(item))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def run(self, search_term: str):
        start = time.perf_counter()
        data = await self.get_page(search_term)
        if data:
            await self.parse(data)
        logger.info(f"Processed {len(self.items)} in {time.perf_counter() - start}ms.")
