"""
1、def封装
2、参数化
3、返回值： 数据库断言不需要返回值
4、加上日志： 但凡你想确认数据结果的地方 都可以加上日志
5、因为有些接口不需要做数据提取，所以判空处理：
6、异常捕获： 因为断言失败要加日志 记录 并raise错误 使测试用例失败

"""
import json

import allure

from tools.handle_replace import replace_mark
from tools.handle_mysql import HandleMysql
from datas.db_data import my_db
from loguru import logger

@allure.step("数据库结果断言步骤")
def database_assert(assert_data):
    if assert_data is None: # 判空处理
        return
    logger.info("--------------------数据库断言开始----------------------------")
    # 第一步：先读取数据出来-- 反序列化 转化字典
    assert_data = json.loads(assert_data)
    logger.info(f"数据库断言的表达式：{assert_data}")
    # 第二步： 得到key【sql】 和value【预期数据库查询结果】
    for k,v in assert_data.items(): # k是sql语句，v是数据库预期结果
        # 第三步： sql里有占位符，先替换-调用replace方法
        k = replace_mark(k)
        logger.info(f"数据库查询sql是{k}")
        # 第四步： 调用数据库封装的方法 执行查询语句 得到数据库查询结果
        sql_result = HandleMysql(**my_db).query_data(k)  # 数据库的查询结果：{'count(*)': 1}| {'status': 2}
        # 第五步： 把预期结果和查询结果 断言
        for i in sql_result.values(): # i是数据库查询结果字典的values 1 2这个数据 ==执行结果
            logger.info(f"数据库断言的实际结果是{i}")
            logger.info(f"数据库断言的预期结果是{v}")
            try:
                assert i == v
                logger.info("数据库断言成功！")
            except AssertionError as e:
                logger.error("数据库断言失败！")
                raise e



if __name__ == '__main__':
    assert_data = '''{"select count(*) from tz_order where order_number = '#orderNumbers#'":1,
    "select status from tz_order where order_number = '#orderNumbers#'":1}'''
    database_assert(assert_data)