from .loksabha.spider import Spider
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
    async with Spider() as spider:
        await spider.run("mental health")

asyncio.run(main())
