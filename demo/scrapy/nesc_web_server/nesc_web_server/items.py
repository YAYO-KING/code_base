import scrapy


# 实体模型
class WebSiteItem(scrapy.Item):
    category = scrapy.Field()
    categoryName = scrapy.Field()
    rootUrl = scrapy.Field()
    rootUrlName = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    content = scrapy.Field()
    releaseTime = scrapy.Field()
    createTime = scrapy.Field()
