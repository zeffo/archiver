# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from .items import Question
    from scrapy import Spider


class ArchiverPipeline:
    def process_item(self, item: Question, spider: Spider):
        """This function is called for every Question found by the spiders.

        This should be used for GCloud dumps in the future.
        Currently, it saves the PDFs in folders created according to date.
        """

        data_dir = Path("data/")
        if not data_dir.exists():
            data_dir.mkdir()

        date = data_dir / item.date.strftime("%d.%m.%Y")
        if not date.exists():
            date.mkdir()

        item.save(date)

        return item
