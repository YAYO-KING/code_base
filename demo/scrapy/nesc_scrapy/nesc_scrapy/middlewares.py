from scrapy import signals
import random
import json, requests, datetime  # 导入所需库

# 中间件 -- 中间件有两种，爬虫中间件和下载器中间件
from itemadapter import is_item, ItemAdapter


# 爬虫中间件
class NescScrapySpiderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):

        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


"""
下载中间件

from_crawler：一个类函数。组件注册后被初始化，这个函数先工作；
process_request：处理请求函数。每个请求都会经过这里，然后在进入下载器；可不返回；
process_response：处理响应的函数。每个响应都会经过且这个函数必须返回响应；
process_exception：处理异常的函数。一旦出现了异常，异常才会通过这里；可不返回；
spider_opened：爬虫启动函数，爬虫启动是，这个函数会被调用，通常作为日志输出。

# 重点函数【按先后顺序体现重要程序】是process_request、process_response、process_exception，例如在这里切换User-Agent和设置代理IP都是process_request函数处理的。
# 处理响应和处理异常的函数，通常都是出现了问题，用于发起补救措施的。例如，没有响应再发起请求等操作。
"""


class NescScrapyDownloaderMiddleware:

    def __init__(self):
        self.ua = [
            'chrome browser version:66',
            'firefox browser version:unknow',
            'qq browser',
            '360 browser very very slow',
            'IE version:6 ',
        ]

    # 一个类函数。组件注册后被初始化，这个函数先工作；
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    # 处理请求函数。每个请求都会经过这里，然后在进入下载器；可不返回；
    def process_request(self, request, spider):
        # 代码实现随机User-Agent中间件
        request.headers['User-Agent'] = random.choice(self.ua)
        return None

    # 处理响应的函数。每个响应都会经过且这个函数必须返回响应；
    def process_response(self, request, response, spider):
        return response

    # 处理异常的函数。一旦出现了异常，异常才会通过这里；可不返回；
    def process_exception(self, request, exception, spider):
        pass

    # 爬虫启动函数，爬虫启动是，这个函数会被调用，通常作为日志输出；
    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


"""
而下载器中间件切换请求的代理IP是突破各类IP封锁行为的利器，该知识点必须学会。

下面开始学习如何高效率的使用代理IP：

首先，新建一个下载器中间件的类，名称是ProxyIPMiddleware。
代理IP是从daili.spbeen.com接口上拿的，所以初始化函数要准备url接口，用于取IP。
为了保证高效率的使用IP，我们尽可能地一个IP要在有效期内提高使用率，因此需要存储IP和存储过期时间。
处理请求。请求进入中间件，判断IP是否失效，如果IP失效，重新请求一个，然后保存过期时间和IP。如果IP没有失效，则不做其他操作。
将IP设置给请求，将请求给下载器，等待响应
"""


class ProxyIPMiddleware:
    def __init__(self):
        # 存储URL的参数
        self.url = 'http://daili.spbeen.com/get_api_json?token=BP6clYrpKeTizKPq5T5j2gPN&num=1'
        # 存放代理的参数
        self.proxy = ''
        # 存储过期时间的参数
        self.expire_datetime = datetime.datetime.now() - datetime.timedelta(seconds=60)
        # 提取代理IP的函数

    def _get_proxyip(self):
        # 大致思路：请求url，因为是json字符串，所以用json解析成字典，然后从data中取出代理IP的值
        resp = requests.get(self.url)
        info = json.loads(resp.text)
        proxy = info['data'][0]
        # 将代理IP的值，赋值给proxy参数，过期时间也进行修改，当前时间+1分钟
        self.proxy = proxy
        self.expire_datetime = datetime.datetime.now() + datetime.timedelta(minutes=1)
        # 检测是否过期的函数

    def _check_expire(self):
        # 如果已过期，重新提取；如果没过期，不做任何操作。
        if datetime.datetime.now() >= self.expire_datetime:
            self._get_proxyip()
            print('=====================\n', '切换代理IP：' + self.proxy)
        # 处理请求的函数

    def process_request(self, spider, request):
        self._check_expire()  # 每次请求过来，都检查一下是否过期
        request.meta['proxy'] = 'http://' + self.proxy
        # 最后一行是固定的语法，给请求设置代理IP是给meta['proxy']赋值，且值的内容，必须是http协议卡死
