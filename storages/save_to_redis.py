from config import cgf
from log import app_logger
import redis
from random import choice
from config.settings import REDIS_KEY, PROXY_SCORE_INIT, PROXY_SCORE_MIN, PROXY_SCORE_MAX
from exception.pool_error import PoolEmptyException


class RedisClient(object):
    """redis connection client """

    def __init__(self):
        self.db = redis.Redis(host=cgf.get('redis', 'host'), port=cgf.get('redis', 'port'),
                              password=cgf.get('redis', 'password'), decode_responses=True)

    def add(self, proxy, score=PROXY_SCORE_INIT) -> int:
        """
        add proxy and set it to init score
        :param proxy:
        :param score:
        :return:
        """

        if not self.exists(proxy):
            maping = {proxy : score}
            return self.db.zadd(REDIS_KEY, maping)

    def exists(self, proxy) -> bool:
        """
        if proxy exists
        :param proxy:
        :return: bool
        """
        return not self.db.zscore(REDIS_KEY, proxy) is None

    def decrease(self, proxy) -> int:
        """
        decrease score of proxy, if small than PROXY_SCORE_MIN, delete it
        :param proxy:
        :return: new score
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > PROXY_SCORE_MIN:
            app_logger.error(f'{proxy} current score {score}, decrease 1')

            return self.db.zincrby(REDIS_KEY,  -1, proxy)
        else:
            app_logger.info(f'{proxy} current score {score},  remove it')
            self.db.zrem(REDIS_KEY, proxy)

    def set_max(self, proxy):
        """
        set proxy to max score
        :param proxy:
        :return:
        """
        app_logger.info(f'{proxy} is valid, set to {PROXY_SCORE_MAX}')
        maping = {proxy: PROXY_SCORE_MAX}
        return self.db.zadd(REDIS_KEY, maping)

    def random(self):
        """
        get random proxy
        firstly try to get proxy with max score
        if not exists, try to get proxy by rank
        if not exists, raise error
        :return: proxy, like 8.8.8.8:8
        """
        # try to get proxy with max score
        proxies = self.db.zrangebyscore(REDIS_KEY, PROXY_SCORE_MAX, PROXY_SCORE_MAX)
        if len(proxies):
            return choice(proxies)
        # else get proxy by rank
        proxies = self.db.zrevrange(REDIS_KEY, PROXY_SCORE_MIN, PROXY_SCORE_MAX)
        if len(proxies):
            return choice(proxies)
        # else raise error
        raise PoolEmptyException

    def count(self) -> int:
        """
        get count of proxy
        :return: count, int
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        get all proxy
        :return:
        """
        return self.db.zrangebyscore(REDIS_KEY, PROXY_SCORE_MIN, PROXY_SCORE_MAX)

    def batch(self, start, end):
        """
        get batch of proxies
        :param start: start index
        :param end: end index
        :return: list of proxies
        """
        return self.db.zrevrange(REDIS_KEY, start, end - 1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.decrease('101.254.136.130:443')
    print(result)
