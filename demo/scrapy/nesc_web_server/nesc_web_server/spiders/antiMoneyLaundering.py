import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from items import WebSiteItem


class AntimoneylaunderingSpider(CrawlSpider):
    name = "antiMoneyLaundering"
    allowed_domains = ["shanghai.pbc.gov.cn"]
    start_urls = ["http://shanghai.pbc.gov.cn/fzhshanghai/113577/114832/114918/index.html"]

    rules = (Rule(LinkExtractor(allow=r"Items/"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        item = {}
        # item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        # item["name"] = response.xpath('//div[@id="name"]').get()
        # item["description"] = response.xpath('//div[@id="description"]').get()
        return item
