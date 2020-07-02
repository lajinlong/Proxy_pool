# -*- coding: utf-8 -*-
"""测试代理有效性"""
import aiohttp
import asyncio
from Agent_Pool.log import app_logger
from config.settings import TEST_URL, TEST_TIMEOUT, TEST_VALID_STATUS, TEST_BATCH
from Agent_Pool.storages.save_to_redis import RedisClient
from aiohttp import ClientProxyConnectionError, ServerDisconnectedError, ClientOSError, ClientHttpProxyError
from asyncio import TimeoutError
EXCEPTIONS = (
    ClientProxyConnectionError,
    ConnectionRefusedError,
    TimeoutError,
    ServerDisconnectedError,
    ClientOSError,
    ClientHttpProxyError
)


class Tester(object):
    """
    tester for testing proxies in queue
    """

    def __init__(self):
        self.redis = RedisClient()
        self.loop = asyncio.get_event_loop()

    async def test(self, proxy):
        """
        test single proxy
        :param proxy:
        :return:
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                app_logger.debug(f'testing {proxy}')
                async with session.get(TEST_URL, proxy=f'http://{proxy}', timeout=TEST_TIMEOUT,
                                       allow_redirects=False) as response:
                    if response.status in TEST_VALID_STATUS:
                        self.redis.set_max(proxy)
                        app_logger.debug(f'proxy {proxy} is valid, set max score')
                    else:
                        self.redis.decrease(proxy)
                        app_logger.debug(f'proxy {proxy} is invalid, decrease score')
            except EXCEPTIONS:
                self.redis.decrease(proxy)
                app_logger.debug(f'proxy {proxy} is invalid, decrease score')

    def run(self):
        """
        test main method
        :return:
        """
        # event loop of aiohttp
        app_logger.info('stating tester...')
        count = self.redis.count()
        app_logger.debug(f'{count} proxies to test')
        for i in range(0, count, TEST_BATCH):
            # start end end offset
            start, end = i, min(i + TEST_BATCH, count)
            app_logger.debug(f'testing proxies from {start} to {end} indices')
            proxies = self.redis.batch(start, end)
            tasks = [self.test(proxy) for proxy in proxies]
            # run tasks using event loop
            self.loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    tester = Tester()
    tester.run()