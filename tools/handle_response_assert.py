"""
函数优化：
1、加日志： 方便做跟踪
2、异常捕获： 断言成功或者失败的结果 记录日志  / 断言失败 ； 异常抛出
3、因为有些用例的步骤可能不需要做断言 这个预期结果字段空的 --None 判空处理。
"""
import json

import allure
from jsonpath import jsonpath
from loguru import logger

@allure.step("响应结果断言步骤")
def response_assert(expected_data,login_resp):
    """
    这是做响应断言的函数
    :param expected_data: 从excel表格里读取的预期结果表达式
    :param login_resp:登录的响应消息
    :return:
    """
    # 这是判断处理 --不需要断言
    if expected_data is None:
        logger.info("这条用例不需要做断言！！")
        return
    # 第一步： 反序列化操作： 转化为字典
    logger.info("----------------------断言开始-----------------------------")
    expected = json.loads(expected_data)
    logger.info(f"json反序列之后的期望结果是：{expected}")
    # 第二步： 取到期望结果键值对： key 是jsonpath 表示式，value是断言的预期结果
    for k,v in expected.items():
        if k.startswith("$"):
            # k是 "$..nickName"，v 是lemon_py
            try:
                actual_result = jsonpath(login_resp.json(),k)[0]
            except Exception as e:
                logger.error("接口执行失败，响应数据提取失败")
                raise e
            logger.info(f"执行结果是：{actual_result}")
            try:
                assert actual_result == v
                logger.info("断言通过！")
            except Exception as e:
                logger.error("断言失败！")
                raise e
        elif k == 'text':
            actual_result = login_resp.text
            logger.info(f"执行结果是：{actual_result}")
            try:
                assert actual_result == v
                logger.info("断言通过！")
            except Exception as e:
                logger.error("断言失败！")
                raise e

