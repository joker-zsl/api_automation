"""
1、def封装
2、参数化
3、返回值： 因为数据都存在环境变量 所以不需要返回值
4、加上日志： 但凡你想确认数据结果的地方 都可以加上日志
5、因为有些接口不需要做数据提取，所以判空处理：

注册接口，要二次修改 extract提取的方法。加一个判断分支：思路如下 {"check_code":"text"}
    * 1、针对键值对的值做判断，是$开头的就是jsonpath
    * 2、v如果是text 就是直接获取响应文本。
    * 3、结果都是存在环境变量里的。
"""


import json

import allure
from jsonpath import jsonpath
from loguru import logger
from tools.envi_data import EnviData

@allure.step("提取响应结果")
def extract_response(response,extract_data):
    # 因为有些接口不需要做数据提取，所以判空处理：
    if extract_data is None:
        logger.info("这条用例不需要做响应结果的数据提取！")
        return
    # 第一步： 反序列化 -字典
    logger.info("-----------------响应结果提取开始------------------------------")
    extract_data = json.loads(extract_data)
    logger.info(f"提取的向红结果的表达式是：{extract_data}")
    for k,v in extract_data.items():  # k 是access_token | check_code 变量名字，v是$..access_token | text
        # 因为响应结果有可能是json格式 也有可能是文本格式： 所以，这里要做判断分支：
        if v.startswith("$"):
            # 使用jsonpath表达式 提取login响应结果里的值
            value = jsonpath(response.json(),v)[0]  # 是access_token的具体值
        elif v == "text": # 如果是文本 用响应消息获取文本
            value = response.text
        # 存起来到环境变量里去
        setattr(EnviData,k,value)
    logger.info(f"提取并设置环境变量之后的类属性是：{EnviData.__dict__}")




if __name__ == '__main__':
    response = {"access_token": "0efdce50-0e2f-4ed0-b4d1-944be5ab518a",
                "token_type": "bearer", "refresh_token": "4bfc3638-e7e4-4844-a83d-c0f8340bc146",
                "expires_in": 1295999,
                "pic": "http://mall.lemonban.com:8108/2023/09/b5a479b28d514aa59dfa55422b23a6f0.jpg",
                "userId": "46189bfd628e4a738f639017f1d9225d", "nickName": "lemon_auto", "enabled": True}

    extract_data = '{"access_token":"$..access_token","token_type":"$..token_type"}'
    extract_response(response,extract_data)
