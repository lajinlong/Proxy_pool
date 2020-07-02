'''爬虫父类'''

from retrying import retry
import requests
from log import app_logger
import asyncio
import aiohttp


class BaseCrawler(object):
    urls = []
    # new_loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(new_loop)
    LOOP = asyncio.get_event_loop()
    asyncio.set_event_loop(LOOP)

    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None)
    async def _get_page(self, url):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                        url,  timeout=10
                ) as resp:
                    # print(dir(resp.content),resp.content)
                    return await resp.text()
            except:
                return ''

    def crawl(self):
        """
        crawl main method
        """
        for url in self.urls:
            app_logger.info(f'fetching {url}')
            # html = self.LOOP.run_until_complete(asyncio.gather(self._get_page(url)))
            html = self.LOOP.run_until_complete(self._get_page(url))
            # print('html', html)
            for proxy in self.parse(html):
                # app_logger.info(f'fetched proxy {proxy.string()} from {url}')
                yield proxy