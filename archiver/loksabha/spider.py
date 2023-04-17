from typing import Any
from yarl import URL
from httpx import AsyncClient
import asyncio
import time
import logging
from archiver.spider import BaseSpider
from archiver.models import LokSabhaQuestion

logger = logging.getLogger("archiver")


class LokSabhaSpider(BaseSpider[LokSabhaQuestion]):
    BASE_URL = "https://eparlib.nic.in/restv3/fetch/all?collectionId=3"
    PAGE_SIZE = 100

    def get_url(self, *, loksabha_no: int, search_string: str, page_no: int = 0) -> URL:
        """Returns the query URL with the given parameters.

        Parameters
        ----------
        loksabha_no: :class:`int`
            The Lok Sabha number.

        search_string: :class:`str`
            The keyword(s) to search for.

        page_no: :class:`int` = 0
            The page number to retrieve. Defaults to zero.
            Page size can be configured via the PAGE_SIZE attribute.

        Returns
        -------
        :class:`yarl.URL`
            The URL object.
        """
        lok_no = f"{loksabha_no:02}"
        params = {
            "loksabhaNo": lok_no,
            "anyWhere": search_string,
            "start": page_no * self.PAGE_SIZE,
            "rows": self.PAGE_SIZE,
        }
        url = URL(self.BASE_URL) % params
        return url

    def get_total_records(self, data: dict[str, Any]) -> int:
        """Returns the total amount of records found.

        Parameters
        ----------
        data: :class:`dict[str, Any]`
            The JSON data.

        Returns
        -------
        :class:`int`
            The total amount of records available.

        """

        return int(data.get("rowsCount", 0))

    async def get_page(
        self,
        *,
        loksabha_no: int,
        search_string: str,
        page_no: int,
        client: AsyncClient | None = None,
    ):
        """Makes a request to the endpoint with the given parameters and returns the response JSON.

        Parameters
        ----------
        loksabha_no: :class:`int`
            The Lok Sabha number.

        search_string: :class:`str`
            The keyword(s) to search for.

        page_no: :class:`int`
            The page number to retrieve.

        client: :class:`AsyncClient | None`
            The httpx AsyncClient to use.
            Passing None will utilize the internal AsyncClient.
            Defaults to None.

        Returns
        -------
        :class:`dict[str | Any]`
            The JSON response data.

        """
        url = self.get_url(
            loksabha_no=loksabha_no, search_string=search_string, page_no=page_no
        )
        client = client or self.client
        resp = await client.get(str(url))
        logger.debug(f"Request made to {resp.url}: {resp.status_code}")
        return resp.json()

    async def parse(self, data: dict[str, Any]):
        """Parses the response json and concurrently processes the items.

        Parameters
        ----------
        data: :class:`dict[str, Any]`
            The JSON response data.

        """
        for raw in data.get("records", tuple()):
            item = LokSabhaQuestion(**raw)
            asyncio.create_task(self.process_item(item))

    async def parse_page(
        self,
        *,
        loksabha_no: int,
        search_string: str,
        page_no: int,
        client: AsyncClient | None = None,
    ):
        """Retrieves a page and parses it.
        This simply calls `get_page` and `parse`.

        Parameters
        ----------
        loksabha_no: :class:`int`
            The Lok Sabha number.

        search_string: :class:`str`
            The keyword(s) to search for.

        page_no: :class:`int`
            The page number to retrieve.

        client: :class:`AsyncClient | None`
            The httpx AsyncClient to use.
            Passing None will utilize the internal AsyncClient.
            Defaults to None.
        """

        page = await self.get_page(
            loksabha_no=loksabha_no,
            search_string=search_string,
            page_no=page_no,
            client=client,
        )
        await self.parse(page)

    async def run(self, search_string: str):
        """Retrieves all data for the given search string.

        Parameters
        ----------
        search_string: :class:`str`

        """

        start = time.perf_counter()
        tasks: list[asyncio.Task[Any]] = []
        for lok_no in range(1, 18):
            initial = await self.get_page(
                loksabha_no=lok_no, search_string=search_string, page_no=0
            )
            await self.parse(initial)
            pages = self.get_total_records(initial) // self.PAGE_SIZE
            for i in range(1, pages):
                coro = self.parse_page(
                    loksabha_no=lok_no, search_string=search_string, page_no=i
                )
                task = asyncio.create_task(coro)
                tasks.append(task)
        await asyncio.gather(*tasks)
        logger.info(f"Processed {len(self.items)} in {time.perf_counter() - start}ms.")
