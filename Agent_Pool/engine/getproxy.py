# -*- coding: utf-8 -*-
"""爬虫启动器，获取代理"""
from storages.save_to_redis import RedisClient
from spider import __all__ as spider_classes
from config.settings import PROXY_NUMBER_MAX


class Getproxies(object):
    """
    getter of proxies
    """

    def __init__(self):
        self.redis = RedisClient()
        self.crawlers_cls = spider_classes
        self.crawlers = [crawler_cls() for crawler_cls in self.crawlers_cls]

    def is_full(self):
        """
        redis storage if full
        :return: bool
        """
        return self.redis.count() >= PROXY_NUMBER_MAX

    def run(self):
        """
        run all crawlers to get proxy
        :return:
        """
        if self.is_full():
            return
        for crawler in self.crawlers:
            for proxy in crawler.crawl():
                self.redis.add(proxy)


if __name__ == '__main__':
    getter = Getproxies()
    getter.run()