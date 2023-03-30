from typing import Protocol
from archiver.items import Question


class SpiderProtocol(Protocol):
    def get_pages(self) -> list[Question]:
        ...
