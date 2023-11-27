from enum import Enum


class ResponseStatus(Enum):
    SUCCESS = {"code": 200, "message": "请求成功"}
    FAILED = {"code": 500, "message": "请求失败"}

    LOCK_FAIL = {"code": 500, "message": "加锁失败"}

    NOT_FOUND = {'code': 404, 'message': '资源未找到'}

    def getCode(self):
        return self.value['code']

    def getMessage(self):
        return self.value['message']

