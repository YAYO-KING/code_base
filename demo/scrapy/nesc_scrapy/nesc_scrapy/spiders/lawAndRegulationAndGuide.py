import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

"""
总结crawlspider的运行逻辑：

请求start_urls内的网址，拿到响应。
提取响应中的全部URL。
然后将提取出的全部URL，一个一个给rules规则，进行正则匹配符合规则的url，请求并拿到对应响应，将响应丢给回调函数，也就是callback指定的内容不符合规则的url，不处理，自动丢弃
直到没有新的url需要请求，自动停止爬虫

从start_urls中的url开始请求，拿到响应。
从响应中解析出全部的url，然后逐个放到rules规则中进行匹配。
url和规则allow匹配吻合，进一步请求，并把响应给规则中的callback指定的回调函数。
匹配不吻合，不处理，将url丢弃。
"""


# CrawlSpider
class LawandregulationandguideSpider(CrawlSpider):
    name = "lawAndRegulationAndGuide"
    allowed_domains = ["www.csrc.gov.cn",
                       "www.sac.net.cn",
                       "www.sse.com.cn",
                       "www.szse.cn",
                       "www.neeq.com.cn",
                       "www.chinaclear.cn"]

    # 将启动的url增加到了多条，请求多次就可以了。
    start_urls = [
        "http://www.csrc.gov.cn/csrc/c100028/common_xq_list.shtml",
        "http://www.csrc.gov.cn/csrc/c100029/common_list.shtml",
        "http://www.csrc.gov.cn/csrc/c100030/common_xq_list.shtml",
        "https://www.sac.net.cn/tzgg/",
        "https://www.sac.net.cn/ljxh/xhgzdt/",
        "http://www.sse.com.cn/aboutus/mediacenter/hotandd/",
        "http://www.szse.cn/aboutus/trends/news/",
        "http://www.bse.cn/news/important_news.html",
        "http://www.neeq.com.cn/news/important_news.html",
        "http://www.chinaclear.cn/zdjs/xtzgg/center_flist.shtml",
        "http://www.chinaclear.cn/zdjs/gsdtnew/gsdtnew.shtml"
    ]

    # 相比于Spider，这里多了rules
    # 提示：crawlspider和spider的重大区别，在于rules，这个是循环匹配和请求处理用的。
    """
    从start_urls列表中提取网址。
    请求网址并拿到响应。
    提取响应中的全部URL。
    将提取出的全部URL，一个一个给rules规则并进行正则匹配。
    符合规则的url，请求并拿到对应响应，如果follow为False，响应给回调函数，也就是callback指定的内容；如果follow为True，响应给回调函数处理，并且响应会回到第2步继续处理。
    不符合规则的url，不处理，自动丢弃。
    直到没有新的url需要请求，自动停止爬虫。
    """
    rules = (
        # URL 匹配规则
        # allow是允许的意思,也就是符合这类规则的url都可以请求并将响应丢给callback的值，也就是parse_item函数
        # 当follow为False，响应直接给回调函数，不做其他操作；
        # 当follow为True，响应除了会给回调函数，还会重新的，被解析链接和重新匹配rules
        # Rule(LinkExtractor(allow=r'http://angelimg.spbeen.com/index/\d+'),callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r"Items/"), callback="parse_item", follow=True),
    )

    # 相比于Spider的默认parse函数，这里是parse_item
    def parse_item(self, response):
        # 只输出响应的url
        print(response.url)

        item = {}
        # item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        # item["name"] = response.xpath('//div[@id="name"]').get()
        # item["description"] = response.xpath('//div[@id="description"]').get()
        return item
