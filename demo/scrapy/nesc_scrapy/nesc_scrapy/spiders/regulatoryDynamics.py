import scrapy


class RegulatorydynamicsSpider(scrapy.Spider):
    # 爬虫名称
    name = "regulatoryDynamics"
    allowed_domains = ["www.csrc.gov.cn"]
    # 爬虫启动时，每次都是从爬虫类的start_urls字段中，取出全部的url内容，然后发起请求并将响应给默认的parse函数
    start_urls = ["http://www.csrc.gov.cn/csrc/c100028/common_xq_list.shtml"]

    # 在Spider的源码类中，有一个特殊的函数叫做start_requests。它的作用是启动爬虫，发起最开始的请求。
    # 只要修改此函数，即可在爬虫启动时，满足任意关于请求的需求
    # 使用了start_requests，就基本可以不使用start_urls了
    def start_requests(self):
        # cls = self.__class__
        # if method_is_overridden(cls, Spider, 'make_requests_from_url'):
        #     warnings.warn(
        #         "Spider.make_requests_from_url method is deprecated; it "
        #         "won't be called in future Scrapy releases. Please "
        #         "override Spider.start_requests method instead (see %s.%s)." % (
        #             cls.__module__, cls.__name__
        #         ),
        #         )
        #     for url in self.start_urls:
        #         yield Request(url, dont_filter=True);
        # else:
        #     for url in self.start_urls:
        #         yield Request(url, dont_filter=True)
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # pass
        # 响应的状态码status，以及响应的url
        print(response.status, response.url)
        # 提取出当前响应的全部a标签的链接，然后进行输出
        links = response.xpath('.//ul[@id="list"]/li/a/@href').extract()
        print(links)
        # 将获取到的连接再进行请求爬取（scrapy会自动的过滤url，不用担心出现请求死循环的现象）
        for link in links:
            yield scrapy.Request(link, callback=self.parse)  # yield返回请求，目标网址是解析出来的链接，回调函数是parse函数

        # 获取请求传参
        # floor_num = response.meta.get('floor_num',False)
        # 请求传参
        # yield scrapy.Request(link,callback=self.parse, meta={'floor_num':floor_num})


        # 图片管道有特定的机构，插入图片管道的item，必须有image_urls和images这两个字段
        # item = {}
        # item['image_urls'] = response.xpath('.//img/@src').extract()  # image_urls 是列表结构，里面保存需要下载的图片链接。
        # item['images'] = []  # images 是列表结构，里面是保存图片下载完成后的几个详细信息
        # yield item


        # 文件下载通道需要特定的结构 file_urls，列表格式，需要将下载的链接都放这里files，列表格式，等下载好之后，具体的数据会被放在这里字典创建且赋值后，直接yield返回即可
        # item = {}
        # item['file_urls'] = response.xpath('.//img/@src').extract()
        """
        下载成功之后，item['files']中保存着三个字段信息，分别是checksum、path、url
        在爬虫运行时，文件会被保存到本地。但文件的三个信息不会保存起来，只会输出；一旦终端软件关闭，信息就丢失了。
        为避免上述问题，我们可以写一个管道，把从下载文件中得到的checksum、path、url的信息进行保存，命名格式是"文件名称.txt"。



        """
        # item['files'] = []
        # yield item
