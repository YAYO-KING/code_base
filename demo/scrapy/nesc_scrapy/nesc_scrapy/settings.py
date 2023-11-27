# 爬虫项目名称
BOT_NAME = "nesc_scrapy"

SPIDER_MODULES = ["nesc_scrapy.spiders"]
NEWSPIDER_MODULE = "nesc_scrapy.spiders"

# 配置图片下载到本地的目录
IMAGES_STORE = "images"
# 配置缩略图
IMAGES_THUMBS = {
    '50x50': (50, 50),  # '50x50':(50,50)即：每张图片生成一张宽、高各50px的缩略图
}

# 配置文件管道下载的本地目录
FILES_STORE = "files"

# 用户代理
# USER_AGENT = "nesc_scrapy (+http://www.yourdomain.com)"

"""
网站的服务和类型各不相同，引擎无法判断网站哪些内容可展示，哪些内容不展示。
因此，网站和搜索引擎之间，遵守如下规则：
引擎搜索之前，它会先查看网站主域名的robots.txt 路径，例如 www.spbeen.com/robots.txt
robots.txt的内容，标明了哪些链接可以访问，哪些链接不能访问
robots.txt的内容，还可以针对不同的搜索引擎，写不一样的访问规则
"""
# 每个新建的Scrapy项目，默认度是遵循网站的robots.txt文件内容 True遵守  False不遵守
ROBOTSTXT_OBEY = True

# scrapy是爬虫框架，自身基于异步请求库Twisted，所以它自身是支持并发默认16并发数。
# 并发数
CONCURRENT_REQUESTS = 8

# 请求延迟的字段，配合并发数，就可以像脚本爬虫一样，慢慢的处理请求了
# 单位：s 每次请求间隔等待3秒，是强制固定的。你也可自定义设置成1、2、0.5、0.1、0.01、0.005 秒等情况
"""
以上字段和值，虽然解释是对的，但是等待时间不是固定的。也就是说，如果你设置 1，每次请求的间隔不是固定的1秒钟，而是一个范围值。
这个范围是 0.5*1 ~ 1.5*1，也就是在0.5秒和1.5秒之间随机的设置的值。
还需要注意的是，设置了下载延迟对多并发也会有影响。
多并发指的是同一时间可以存在16个请求【默认16个】，有了下载延迟之后，每次请求的发出时间，即前一个请求发出去之后，间隔一段时间再发出后一个请求。
间隔时间是相对发出时间来计算的，响应回来的时间和间隔时间没有任何的联系。
"""
DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# 修改默认的请求头
DEFAULT_REQUEST_HEADERS = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    # "Accept-Language": "en",

    # 请求的代理信息 -- 一般复制浏览器的值
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Referer': 'http://angelimg.spbeen.com',
}

# 爬虫中间件
SPIDER_MIDDLEWARES = {
    # 项目名.文件名.类名
    "nesc_scrapy.middlewares.NescScrapySpiderMiddleware": 543,
}

# 下载中间件
# 注意：在项目中注册下载器中间件的时候，切记，数字不能重复。
DOWNLOADER_MIDDLEWARES = {
    # 具体注册的写法是“项目名.文件名.类名”:数字
    "nesc_scrapy.middlewares.NescScrapyDownloaderMiddleware": 543,
    # 代理IP中间件
    "nesc_scrapy.middlewares.ProxyIPMiddleware": 750,
}

# 扩展插件
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# 管道文件
# 配置管道pipelines
# 注册的多个管道 传入的数据item会挨个进入管道给管道进行处理
# 管道数值代表执行的先后  数值越小越先执行
"""
注册的管道哪个在上一行，哪个在下一行都无所谓，重点是对应每个注册管道对应的值。
这个值很有讲究，因为关乎顺序问题：

数值低的item先进入这个管道，管道处理数据。
数值低的管道返回item再进入数值高的管道。
切记管道注册时，千万不要用相同的数值。
"""
ITEM_PIPELINES = {
    "nesc_scrapy.pipelines.NescScrapyPipeline": 300,
    # 启用图片下载通道
    'scrapy.pipelines.images.ImagesPipeline': 2,
    # 启用文件下载通道
    'scrapy.pipelines.files.FilesPipeline': 1,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
