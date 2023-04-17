
from archiver.spider import BaseSpider
from archiver.models import RajyaSabhaQuestion
from typing import Any

class RajyaSabhaSpider(BaseSpider[RajyaSabhaQuestion]):
    BASE_URL = "https://rsdoc.nic.in/Question/Search_Questions"

    def get_url(self, search_string: str, *, fields: list[str] = ["qtitle", "qn_text"]) -> str:
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