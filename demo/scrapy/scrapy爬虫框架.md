Scrapy 是一款由 Python 语言开发高效的爬虫框架，使用 lxml（专业的 XML 处理包）、cssselect 高效地提取 HTML 页面的有效信息，同时它也提供了有效的线程管理。 

组件：
Engine 引擎
Spider 爬虫
Scheduler 调度器
Download 下载器
Pipeline 管道

安装：
pip install scrapy 
conda install scrapy

先pip list看一下是否有twisted，如果已经有了就不需要安装了

windows需要额外安装下twisted
这个twisted的库，是一个异步框架库，scrapy就是依赖它实现的高并发。
https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted
找到你需要的twisted并下载。如果你不清楚需要哪一个，请全部下载并安装测试。命令行：pip install twisted-xxxxxxx.whl

推荐安装一个非必要库pywin32，它可能会自动安装，可能也不会，命令是：python -m pip install pywin32


Scrapy组件介绍：
引擎(Engine)：负责整个系统的数据流处理，触发事务。
调度器(Scheduler)：接受引擎发过来的请求，压入队列中，并在引擎再次请求的时候返回。
下载器(Downloader): 下载网页内容，并将网页内容返回给爬虫。
爬虫(Spider): 爬虫是主要干活的，用来制定特定域名或网页的解析规则。
项目管道(Item Pipeline): 清洗验证存储数据，页面被蜘蛛解析后，被发送到项目管道，并经过几个特定的次序处理数据。
下载器中间件(Downloader Middleware): 位于引擎和下载器之间，处理引擎与下载器之间的请求及响应。
爬虫中间件(Spider Middleware)：位于引擎和爬虫之间，处理从引擎发送到调度的请求及响应。


新建scrapy爬虫项目：
scrapy 查看基本信息

scrapy startproject nesc_scrapy

cd nesc_scrapy

创建爬虫：
默认使用的是basic模板
scrapy genspider 爬虫名称 域名
scrapy genspider regulatoryDynamics http://www.csrc.gov.cn/csrc/c100028/common_xq_list.shtml
爬虫文件都在爬虫项目的spiders目录下
如果想要创建crawlspider模板，则命令行需要加上-t crawl
scrapy genspider -t crawl lawAndRegulationAndGuide http://www.csrc.gov.cn/csrc/c101953/zfxxgk_zdgk.shtml



启动爬虫：
scrapy crawl regulatoryDynamics
scrapy crawl regulatoryDynamics --nolog  # 不带日志的方式启动爬虫
日志的信息非常详细，除非是特殊情况，例如调试、查错等，否则都需要去除无关的日志，然后针对于相关的信息输出，查看出错原因。

日志里面有详细的请求记录，nolog不会展示
日志里面有注册启用的各种组件，nolog不会展示
如果爬虫执行出现了错误，nolog也不会展示
最后的统计信息比较详细，nolog也不会展示

查看当前项目下的所有爬虫：
scrapy list

爬虫日志信息：
'downloader/request_count': 5 请求次数5次
'downloader/response_count': 5 响应次数5次
'start_time': datetime.datetime(2019, 10, 19, 13, 48, 0, 281386) 开始时间
'finish_time': datetime.datetime(2019, 10, 19, 13, 48, 1, 432281) 结束时间


爬虫模板：
scrapy genspider -l
内置的4个爬虫模板，分别是：
basic：基础爬虫模板 Spider
crawl：进阶模板，基础URL种类封装的爬虫模板 CrawlSpider
csvfeed：进阶模板，提取csv格式数据的爬虫模板 CSVFeedSpider
xmlfeed：进阶模板，提取xml格式数据的爬虫模板 XMLFeedSpider



管道说明：
Pipeline是scrapy组件管道的名称，常用的操作有这几个：
    下载图片
    下载文件
    将数据存储进mongo、mysql这类数据库
    数据预处理
    数据存储到本地
    数据写入文件
同样Scrapy内置了pipeline的几个类，分别是：（这三者的关系是：ImagesPipeline 继承 FilesPipeline 继承 MediaPipeline）
    媒体管道 MediaPipeline（基础的object对象。它只是一个基类，不能直接使用）
    文件管道 FilePipeline
    图片管道 ImagePipeline
其中，媒体管道是不能用的，请使用文件管道和图片管道。
除了原生的下载管道，我们也可以自建管道。例如将抓到的数据存储进本地的数据库。


中间件：
中间件有两种，爬虫中间件和下载器中间件
下载器是负责请求url并拿到响应的组件，下载器中间件是请求进入下载器之前的一个插件。
下载器中间件MiddlewareDownloaderMiddleware源码：
这里写了五个函数，依次为：
from_crawler：一个类函数。组件注册后被初始化，这个函数先工作；
process_request：处理请求函数。每个请求都会经过这里，然后在进入下载器；可不返回；
process_response：处理响应的函数。每个响应都会经过且这个函数必须返回响应；
process_exception：处理异常的函数。一旦出现了异常，异常才会通过这里；可不返回；
spider_opened：爬虫启动函数，爬虫启动是，这个函数会被调用，通常作为日志输出。
重点函数【按先后顺序体现重要程序】是process_request、process_response、process_exception，例如在这里切换User-Agent和设置代理IP都是process_request函数处理的。


代理IP的说明：
随着互联网的飞速发展，越来越多的用户在上网过程中暴露个人的隐私信息，使用代理IP可以伪装用户真实IP地址，主要的功能有：
1、加快访问速度
通常代理服务器都具有缓冲的功能，有很大的存储空间，网络出现拥挤或故障时，可通过代理服务器访问目的网站，节约带宽、显著提高访问速度和效率。
2、保护隐私信息
高质量代理IP对网络安全有很大的好处，电脑免受病毒的侵扰，尤其是对于企业来说，可以有效保护企业内部信息，防止黑客攻击。


