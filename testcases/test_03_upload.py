"""
调用夹具，得到token；
发送请求的方法 里没有使用token 地方。
"""
import json

import pytest
import requests
from tools.handle_response_assert import response_assert
from tools.handle_excel import read_data
from tools.handle_path import exc_path
from tools.handle_requests import requests_api

# 第一步： handle_excel读取测试用例的数据  --列表嵌套字典，每个字典是一个用例
all_cases = read_data(exc_path,"上传")

# 第二步： pytest测试用例方法
@pytest.mark.parametrize("data",all_cases)
def test_upload_case(data,login_fixture):  # 调用夹具
    token = login_fixture  # 获取夹具的返回值 赋值给token这个变量
    resp = requests_api(data,token=token)
    expected = data["预期结果"]  # 从excel读取预期结果
    response_assert(expected,resp)

