from spider import BaseCrawler
from lxml import etree
from Agent_Pool.log import app_logger


class IpHaiCrawler(BaseCrawler):
    urls = ['http://www.iphai.com/']

    def parse(self, html):
        res = html
        html_ = etree.HTML(res)
        proxys = html_.xpath('//*[@class="table-responsive module"]/table/tr')
        if len(proxys) == 0:
            app_logger.error('IpHaiCrawler give proxys error：proxys len is 0')
            return

        del proxys[0]
        for proxy in proxys:
            # 判断该IP是否高匿，类型
            type_niming = proxy.xpath('./td[3]/text()')[0].strip()
            host = proxy.xpath('./td[1]/text()')[0].strip()
            port = int(proxy.xpath('./td[2]/text()')[0].strip())
            if type_niming == '透明':
                continue

            if host is None:
                continue
            yield host + ':' + str(port)


if __name__ == '__main__':
    d = IpHaiCrawler()
    for s in d.crawl():
        print(s)