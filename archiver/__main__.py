from archiver.loksabha.spider import LokSabhaSpider
from archiver.rajyasabha.spider import RajyaSabhaSpider

import asyncio
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("archiver")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("archiver.log", mode="w")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

async def main():
    async with RajyaSabhaSpider() as spider:
        page = await spider.get_page(search_string="mental health")
        if page:
            print(len(page))
            
        

asyncio.run(main())
