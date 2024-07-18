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
from tools.handle_db_assert import database_assert

# 第一步： handle_excel读取测试用例的数据  --列表嵌套字典，每个字典是一个用例
all_cases = read_data(exc_path,"修改用户头像")


# 第二步： pytest测试用例方法
@pytest.mark.parametrize("data",all_cases)
def test_modidy_potraite_case(data):  # 调用夹具
    resp = requests_api(data)
    expected = data["预期结果"]  # 从excel读取预期结果
    db_assert = data["数据库断言"]
    response_assert(expected,resp)
    # 数据库断言
    database_assert(db_assert)

