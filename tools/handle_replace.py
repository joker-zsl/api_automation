"""
1、def封装
2、参数化
3、返回值： 最终要拿到替换后的字符串 ---  头部 参数 要用于发送接口测试的
4、加上日志： 但凡你想确认数据结果的地方 都可以加上日志
5、因为有些接口不需要做数据提取，所以判空处理：
6、异常捕获： 因为有可能环境变量里没有这个属性名 和属性值

"""
import re

import allure
from loguru import logger
from tools.envi_data import EnviData
from tools.handle_generate import GenData


@allure.step("替换占位符变量")
def replace_mark(str_data):
    while True:
        if str_data is None:
            return
        result = re.search("#(.*?)#",str_data)
        if result is None:  # 如果没有占位符 就是None 跳出循环
            break
        mark = result.group()  # 结果是  #prodId# --要被替换的子字符串| #gen_unregister_phone()#
        logger.info(f"要被替换的子字符串:{mark}")
        if "()" in mark:
            fun_name = result.group(1)  # 第一个分组的值 结果是 gen_unregister_phone()
            logger.info(f"要提取环境变量的函数名:{fun_name}")
            # 通过eval拖引号之后，不可以直接GenData().gen_unregister_name()，要导包
            gen_data = eval(f'GenData().{fun_name}')  # 接口函数的返回值结果-生成的数据
            logger.info(f"生成的随机的数据是：{gen_data}")
            # 1、存数据到环境变量里 -- 类属性的名字 函数名去掉()
            var_name = fun_name.strip("()")   # 结果是 gen_unregister_phone
            setattr(EnviData,var_name,gen_data)   # 属性名：gen_unregister_phone 属性值： gen_data
            logger.info(f"环境变量的属性值：{EnviData.__dict__}")
            # 2、完成第一条的参数的替换  用刚刚生成的数据替换
            str_data = str_data.replace(mark,str(gen_data))
            logger.info(f"替换完成后的字符串是:{str_data}")
        else:
            var_name = result.group(1) # 第一个分组的值 结果是 prodId
            logger.info(f"要提取环境变量的属性名:{var_name}")
            try:
                var_value = getattr(EnviData,var_name)  # 结果 ： 7717--int类型
            except AttributeError as e:
                logger.error(f"环境变量里不存在这个属性：{var_name}")
                raise e
            logger.info(f"要提取环境变量的属性值:{var_value}")
            str_data = str_data.replace(mark,str(var_value))
            logger.info(f"替换完成后的字符串是:{str_data}")
    return str_data

if __name__ == '__main__':
    # str_data = '{"basketId": 0, "count": 1, "prodId": #prodId#, "shopId": 1, "skuId": #skuId#}'
    str_data = '{"mobile": "#gen_unregister_phone()#"}'
    replace_mark(str_data)