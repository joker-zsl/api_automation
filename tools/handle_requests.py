"""
方法优化：
1、日志加上

2、测试用例方法里调用夹具 获取返回值。
- 更新requests-api，需要做token处理：
 - 设置一个默认参数：token = None
 - 如果接口需要鉴权，测试用例里调用夹具，得到token，requests_api传递token参数；--requests 更新头部
 - 如果接口不需要鉴权： token不传  None。 不会做更新头部的操作。

"""



import json

import allure
import requests
from tools.handle_path import pic_path
from loguru import logger
from tools.handle_extract import extract_response
from tools.handle_replace import replace_mark
from tools.handle_presql import pre_sql

@allure.step("发送接口请求")
def requests_api(casedata,token=None):
    method = casedata["请求方法"]
    url = casedata["接口地址"]
    headers = casedata["请求头"]
    params = casedata["请求参数"]
    presql = casedata["前置SQL"]
    # 在执行前置SQL之前，替换占位符数据
    presql = replace_mark(presql)
    # 在数据替换之前调用前置SQL方法：调用完成后，把结果放到环境变量里
    pre_sql(presql)
    # 在发送请求之前完成头部和参数的替换--调用替换的函数==结果是字符串
    headers = replace_mark(headers)
    params = replace_mark(params)
    url = replace_mark(url) # 替换掉url地址里的占位符
    # 反序列操作: 结合判空处理，
    if headers is not None:
        headers = json.loads(headers)
        if token is not None:  # 这是做接口如果需要鉴权，传进来token 更新头部信息。
            headers["Authorization"] = token  # 字典新增 / 修改
    if params is not None:
        params = json.loads(params)
    logger.info("---------------------------请求消息-----------------------------------")
    logger.info(f"请求方法是{method}")
    logger.info(f"请求地址是{url}")
    logger.info(f"请求头部是{headers}")
    logger.info(f"请求参数是{params}")
    #接口请求可能是get  post  put等各种请求方法 分支判断
    if method.lower() == "get":
        resp = requests.request(method=method, url=url, params=params,headers=headers)
    elif method.lower() == "post":
        if headers is None:
            logger.info("头部为空，检查excel表格里头部信息！")
            return
        # post请求：content-type的类型有关系。需要对每一种类型做处理 分支判断
        if headers["Content-Type"] == "application/json":
            resp = requests.request(method=method, url=url, json=params, headers=headers)
        if headers["Content-Type"] == "application/x-www-form-urlencoded":
            resp = requests.request(method=method, url=url, data=params, headers=headers)
        if headers["Content-Type"] == "multipart/form-data":
            # 发送请求的时候不能带上  'Content-Type': 'multipart/form-data'  删除之后才发送接口请求。
            headers.pop("Content-Type") # 字典删除元素
            filename = params["filename"]  # 文件名字 值
            file_obj = {"file": (filename, open(pic_path/filename, "rb"))}  # 文件参数
            logger.info(f"文件接口的参数是：{file_obj}")
            logger.info(f"文件接口的头部是：{headers}")
            resp = requests.request(method=method, url=url,headers=headers,files=file_obj)
    elif method.lower() == "put":
        resp = requests.request(method=method, url=url, json=params, headers=headers)
    logger.info("------------------------------响应消息-----------------------------")
    logger.info(f"接口响应状态码是：{resp.status_code}")
    logger.info(f"接口响应体是：{resp.text}")
    # 提取响应结果的数据-- 调用提取数据的函数
    extract_response(resp,casedata["提取响应字段"])
    return resp

