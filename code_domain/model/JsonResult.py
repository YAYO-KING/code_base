# json结果类
import json
from code_domain.enums import ResponseStatus


class JsonResult:
    code: int = 200

    message: str = "请求成功"

    data: object = None

    # 类只能有一个构造函数，即__init__方法
    def __init__(self, code: int, message: str, data: object):
        self.code = code
        self.message = message
        self.data = data

    @staticmethod
    def build(code: int, message: str, data: object):
        return JsonResult(code, message, data)

    @staticmethod
    def ok():
        return JsonResult(200, "请求成功", None)

    @staticmethod
    def okData(data:object):
        return JsonResult(200, "请求成功", data)

    @staticmethod
    def fail():
        return JsonResult(500, "请求失败", None)

    @staticmethod # 静态方法
    def response(response: ResponseStatus):
        return JsonResult(response.getCode(), response.getMessage(), None)


if __name__ == '__main__':
    print(JsonResult.ok())
    print(ResponseStatus.FAILED)
    # print(JsonResult.response(ResponseStatus.FAILED))
