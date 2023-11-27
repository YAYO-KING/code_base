# 管道
from itemadapter import ItemAdapter

# 媒体管道
from scrapy.pipelines.media import MediaPipeline

# 文件管道
from scrapy.pipelines.files import FilesPipeline

# 图片管道
from scrapy.pipelines.images import ImagesPipeline
import json


"""
管道的3个函数：
当爬虫启动时，open_spider会被执行，且爬虫作为spider参数传入这个函数，这里可以做一些预处理，例如根据爬虫名，链接对应的数据库。这个函数只会被启动一次。
当爬虫返回了item或者字典dict数据时，数据会被送到process_item函数中，此时函数可以收到item数据和spider爬虫。
process_item函数要做的就是将item中的数据做存储。例如存储到数据库、存储到本地。
process_item函数处理完数据之后，必须返回item ，代码return item，必须返回。
process_item处理数据要返回的原因是：管道是可以注册多个，且item是按顺序进入管道，管道1需要返回给管道2。只有前面的管道给了数据，后面的管道才可以接收到数据。
当爬虫全部处理完之后，爬虫被自动关闭，且管道的close_spider函数会被调用，执行关闭管道的操作。这里通常做的操作是断开数据库、关闭文件。
爬虫关闭后，管道也被关闭，引擎关闭，完成抓取。
"""

class NescScrapyPipeline:
    """
    爬虫启动时，这个函数会被调用
    当爬虫启动时，open_spider会被执行，且爬虫作为spider参数传入这个函数，这里可以做一些预处理，例如根据爬虫名，链接对应的数据库。这个函数只会被启动一次
    """
    def open_spider(self, spider):
        pass

    """
    爬虫关闭时，这个函数会被调用
    当爬虫全部处理完之后，爬虫被自动关闭，且管道的close_spider函数会被调用，执行关闭管道的操作。这里通常做的操作是断开数据库、关闭文件
    爬虫关闭后，管道也被关闭，引擎关闭，完成抓取
    """
    def close_spider(self, spider):
        pass

    """
    当item被爬虫返回时，会进入管道内的process_item函数
    当爬虫返回了item或者字典dict数据时，数据会被送到process_item函数中，此时函数可以收到item数据和spider爬虫
    process_item函数要做的就是将item中的数据做存储。例如存储到数据库、存储到本地
    process_item函数处理完数据之后，必须返回item ，代码return item，必须返回
    process_item处理数据要返回的原因是：管道是可以注册多个，且item是按顺序进入管道，管道1需要返回给管道2。只有前面的管道给了数据，后面的管道才可以接收到数据
    """
    def process_item(self, item, spider):
        return item


# 自定义一个文件下载管道
class MyFilePipeline(object):
    def process_item(self, item, spider):
        """
        下载成功之后，item['files']中保存着三个字段信息，分别是checksum、path、url

        进来的数据是item，item里面有两个字段，一个是file_urls，另一个是files，我们需要处理的是files这个字段的值；
        每个文件都有一个信息，且这个files内容是列表，所以要循环取值并处理；
        文件和文件信息文本需要保存一起，文件的路径是files/full/，所以文件也需要保存到这里；
        文件和文件信息文本最好是紧挨着。所以文件信息文本的名称和文件名称是一样的，只是后缀不同；

        先导入json库，后面需要用到。
        item['files']是列表，循环取出来。
        从中提取出文件名，info['path'].split('/')[-1].split('.')[0]这里是分割字符串的操作。
        输出一下，确保无误，方便查看。
        操作文件，用二进制写的形式打开。文本的操作路径是根据文件保存的路径写的，是固定的。
        打开文件后，把文件信息写入。这个文件信息就是最开始循环的info参数。
        info参数是字典，如果直接写入，只能操作字符串或者字节。此时，在第1步中导入的json库就发挥了作用，它可以将字典转换成字符串。
        """
        for info in item['files']:
            # 文件名
            filename = info['path'].split('/')[-1].split('.')[0]
            print(filename)
            # 将文件信息保存到本地
            with open('files/full/{}.txt'.format(filename), 'w') as file:
                file.write(json.dumps(info))

        return item

"""
文件下载结果：

文件名的位置在path里面，这里有9fbd8fb9f733fa06da238b76982cd6ccc8ee5fdd.jpg，所以需要从这里面提取出名称。
"full/9fbd8fb9f733fa06da238b76982cd6ccc8ee5fdd.jpg"做分割操作，取出9fbd8fb9f733fa06da238b76982cd6ccc8ee5fdd.jpg。
按点分割，取出9fbd8fb9f733fa06da238b76982cd6ccc8ee5fdd。
拼接上txt的后缀，完成了文本文件名，9fbd8fb9f733fa06da238b76982cd6ccc8ee5fdd.txt。
指定文件存储路径files/full。

{
    "file_urls": [
        "http://image.angelimg.spbeen.com/00000mx00000/lyem1OIlNGFB3SZ5fcWa294009/Co9cS8MKcZ22GrSZtC0Y294009-BewkhM.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/VVqDqOGxfyqHINZkBuaQ280188/afY0vNpvU2pyfmvbj88A280188-kgReFT.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/J570Y7BTCuGFcFGsmV3a295688/ZVAczQrYNJQ5M06PRE3x295688-PfHf6y.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/ToCKE4Nq5uOMyJQeYdYf295242/EHrmYddf6IL7tYK8gW3CI2FvU5.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/rxEtP8CZ2TmSRWnCAoPV294513/P035OYiml8LasjVdd4X4294513-54ark5.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/p7F4kjlqULQNnyuduLvf307412/UOmf1nOVWWmgAMsLzAJV5699e8483932ac6c3f9ad1a36c972c70.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/Db0tbdefzl4TejkbFxYb304904/y4mfGwt7pNDPwsJnjKJa304904-xEoa63.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/CVHIh1LXce2Ap6EwSuhr300893/dqFNXHwPgWW7voTWChEu300893-B0k8tL.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/amGSC6EdMDSVyGIY5CNr307127/YXi6AmeSEOogtEKWtFC3307127-J76q3d.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/ixNAK95uorIsJvZbcTzH296417/37y5cinJj3f6MYw25HjEhUo3ix.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/XEhL1sRZFJAtLSWJ7wrT280963/Od37SgQqoRCwDLhkjj0d280963-fRG2fg.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/CW2kFoEyRLVIMm6aKIca277338/Zr769tZMRLhstWY3zqtC277338-TjNC7f.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/lLpdwk5exZPspHCGH4Br278925/xuMCzKKBKBMPmkv9ioWK278925-aXGK4h.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/esY9K65dyBHSKUFndupD278947/2r3YpVhNUoQDkDLKKjLf278947-BW1vRx.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/2RZuuQ7mCFHWaOVyW7kN281088/6gYomC8TZC4C5jAZsfSH281088-takKOz.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/3Ts3GQEVjq7Dlr1orCbL276281/ztjNJoaVhkuXlWIOaspt276281-7Lmln3.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/HtP23pW5tTVsZfA23pe1281126/ER6nCZAfTsU3VxqyDIF3281126-WVvf5q.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/02dQvoD8GjGdTEe9dB7w296685/eGdic4T1hqJZmyW0pF7k296685-5YZw2w.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/B1JQ6NtTWYxsjzmS5ibo295124/F9CJD3ntZzWBkXnd3Oi0dfetoD.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/DSTZpCccRhpiPyRSdupN308020/qrqhaWNojgMabWw90M52dbc5d6c97f7d3155c06a6fc03663ca0d.jpeg",
        "http://image.angelimg.spbeen.com/00000mx00000/cQJ8ysZsDsH02J9i8rd9288837/9JkUnIXc09gYWh0I77Nx288837-KJaeGy.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/ojXBpTFWLtpf4KjAbskD288030/pjVGIs1sXHouBcAr9SIs288030-DuR81l.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/R76SQeLBm8EmhXPKC4at290717/bKY5JEeclJVf5JFqJT8I290717-9m6j3z.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/quwXha3AcfqscIJBtspm307545/dU0zVZdEimFJGb0IFYRYc2a17aad9ba94aa62fb4aca9a97e0c4c.jpg",
        "http://image.angelimg.spbeen.com/00000mx00000/jGyHuPtH2GBcPkKdKGrx289632/oqHsqWOg7lyQJi0vhYWZ289632-ZRthk9.jpg"
    ],
    "files": [
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/lyem1OIlNGFB3SZ5fcWa294009/Co9cS8MKcZ22GrSZtC0Y294009-BewkhM.jpg",
            "path": "full/326b028b5eb157dfdce4d583fb9f8772309bdf5d.jpg",
            "checksum": "24acecefd416e052ae4c3ceae12c50a4"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/VVqDqOGxfyqHINZkBuaQ280188/afY0vNpvU2pyfmvbj88A280188-kgReFT.jpg",
            "path": "full/8193845753e50dd9f44c1066625dced7be27d437.jpg",
            "checksum": "661b579b7406334ea77d79d2be587f59"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/J570Y7BTCuGFcFGsmV3a295688/ZVAczQrYNJQ5M06PRE3x295688-PfHf6y.jpg",
            "path": "full/686d19ccc5e78749f037ac428a6b5c9f0a9385fd.jpg",
            "checksum": "98aa89353437ebe244cf0032faab6841"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/ToCKE4Nq5uOMyJQeYdYf295242/EHrmYddf6IL7tYK8gW3CI2FvU5.jpg",
            "path": "full/6287f6d746a61d0cd6529cd262e4c50a9446bf80.jpg",
            "checksum": "9274f445f01f156dd9549cbc14f42ca8"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/rxEtP8CZ2TmSRWnCAoPV294513/P035OYiml8LasjVdd4X4294513-54ark5.jpg",
            "path": "full/cd4a2f9dcf62d8acbea13bba6a722ad82e87bb05.jpg",
            "checksum": "9765dccdd5fc1a626a09521c72ad297e"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/p7F4kjlqULQNnyuduLvf307412/UOmf1nOVWWmgAMsLzAJV5699e8483932ac6c3f9ad1a36c972c70.jpg",
            "path": "full/18dbf54fbfa1cad86ac51bdf115a5cb4d8277f4a.jpg",
            "checksum": "cd57d5f2234a30d65a696c62f04c9b6f"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/Db0tbdefzl4TejkbFxYb304904/y4mfGwt7pNDPwsJnjKJa304904-xEoa63.jpg",
            "path": "full/08cd2dd62d0abcfbbc6d4e8814260c4cb1e044b7.jpg",
            "checksum": "e2115a64b4e7ed49120de6ab1080be7f"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/CVHIh1LXce2Ap6EwSuhr300893/dqFNXHwPgWW7voTWChEu300893-B0k8tL.jpg",
            "path": "full/6b6552b549162d02b01f195b0dc054152e8890e5.jpg",
            "checksum": "2e7f0053ce0a275d939569bdbc3ccaae"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/amGSC6EdMDSVyGIY5CNr307127/YXi6AmeSEOogtEKWtFC3307127-J76q3d.jpg",
            "path": "full/bc2bbf7a2301d98c52b2d843b9041acc689d2033.jpg",
            "checksum": "6463344b0848f33b6193ee9c68492e04"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/ixNAK95uorIsJvZbcTzH296417/37y5cinJj3f6MYw25HjEhUo3ix.jpg",
            "path": "full/cdddf2d4a8485a11cc31844fb27d3d0a9c809f56.jpg",
            "checksum": "789ff613f3b97e917c9bab7238cb8b04"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/XEhL1sRZFJAtLSWJ7wrT280963/Od37SgQqoRCwDLhkjj0d280963-fRG2fg.jpg",
            "path": "full/2f054d6a55ef1453a0084b6cd8be51bdaca677d2.jpg",
            "checksum": "fe529b1c273ae2be73311a818736a4d7"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/CW2kFoEyRLVIMm6aKIca277338/Zr769tZMRLhstWY3zqtC277338-TjNC7f.jpg",
            "path": "full/cf1ff22b97521609de845abde939096e49c0d816.jpg",
            "checksum": "c017cf680d2314dd365548556942d49d"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/lLpdwk5exZPspHCGH4Br278925/xuMCzKKBKBMPmkv9ioWK278925-aXGK4h.jpg",
            "path": "full/0ff646d70dcf86e32cd23b3c0ab5b33aa3f7c636.jpg",
            "checksum": "5fa17709c2c1bc853aeb1c45c1606b3e"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/esY9K65dyBHSKUFndupD278947/2r3YpVhNUoQDkDLKKjLf278947-BW1vRx.jpg",
            "path": "full/c14b873955a6e5d195f15c6a7e2495a97a7c52bd.jpg",
            "checksum": "4060b0fedf983e7490b4422038f4ceb6"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/2RZuuQ7mCFHWaOVyW7kN281088/6gYomC8TZC4C5jAZsfSH281088-takKOz.jpg",
            "path": "full/6f0d853c570eab9997b2bb12b0d3b33cd0d53503.jpg",
            "checksum": "9b687e6665f71d02bba3624050df76cc"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/3Ts3GQEVjq7Dlr1orCbL276281/ztjNJoaVhkuXlWIOaspt276281-7Lmln3.jpg",
            "path": "full/0bc4bc141877644a3e66c1f989b530519af642f4.jpg",
            "checksum": "f1ea365ddb48107c82cdba36b2c0a4ce"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/HtP23pW5tTVsZfA23pe1281126/ER6nCZAfTsU3VxqyDIF3281126-WVvf5q.jpg",
            "path": "full/0450449ca0d91f05771be5640360506ea6bb65fe.jpg",
            "checksum": "6b4e39b9e4c1a41260f09cfe1db47051"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/02dQvoD8GjGdTEe9dB7w296685/eGdic4T1hqJZmyW0pF7k296685-5YZw2w.jpg",
            "path": "full/5407262cbedd0ea0e066b8a52c81a1679077ea27.jpg",
            "checksum": "87d23e74e0ff9e4fc0a579395832e57e"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/B1JQ6NtTWYxsjzmS5ibo295124/F9CJD3ntZzWBkXnd3Oi0dfetoD.jpg",
            "path": "full/a0a9672c51d9dba984e53de670a29a9c2dbd07be.jpg",
            "checksum": "bdae71f6ad131ddc61786497da606ac1"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/DSTZpCccRhpiPyRSdupN308020/qrqhaWNojgMabWw90M52dbc5d6c97f7d3155c06a6fc03663ca0d.jpeg",
            "path": "full/2ea8da59dd20cc8fcfacbbe89e45c17b69141869.jpeg",
            "checksum": "0a11d48b55b6a7357b38e0bd2efcfb2b"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/cQJ8ysZsDsH02J9i8rd9288837/9JkUnIXc09gYWh0I77Nx288837-KJaeGy.jpg",
            "path": "full/b7d0b987d5a509b737ffdbe6d7784827969119cd.jpg",
            "checksum": "7da155dc2bff4802336a55b6ba9f9446"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/ojXBpTFWLtpf4KjAbskD288030/pjVGIs1sXHouBcAr9SIs288030-DuR81l.jpg",
            "path": "full/5a3a4febf910f13eb8ffb71b26c53b7491d96cf0.jpg",
            "checksum": "e85b734d7306836e1583a3c930347b2e"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/R76SQeLBm8EmhXPKC4at290717/bKY5JEeclJVf5JFqJT8I290717-9m6j3z.jpg",
            "path": "full/008ac2e4352671e63e88fa135dfd48f76c84aa69.jpg",
            "checksum": "ad99d1616a8cf4774669518d45d254d1"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/quwXha3AcfqscIJBtspm307545/dU0zVZdEimFJGb0IFYRYc2a17aad9ba94aa62fb4aca9a97e0c4c.jpg",
            "path": "full/5bd52027d88d21e85a23433f10db372e9ce937be.jpg",
            "checksum": "283e4e979e3a609e88d88beab4ce1a82"
        },
        {
            "url": "http://image.angelimg.spbeen.com/00000mx00000/jGyHuPtH2GBcPkKdKGrx289632/oqHsqWOg7lyQJi0vhYWZ289632-ZRthk9.jpg",
            "path": "full/9fbd8fb9f733fa06da238b76982cd6ccc8ee5fdd.jpg",
            "checksum": "65489c7942d67995a30c6adef4628024"
        }
    ]
}
"""