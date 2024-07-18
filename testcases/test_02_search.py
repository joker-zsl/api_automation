"""

"""
import json

import pytest
import requests
from tools.handle_response_assert import response_assert
from tools.handle_excel import read_data
from tools.handle_path import exc_path
from tools.handle_requests import requests_api

# 第一步： handle_excel读取测试用例的数据  --列表嵌套字典，每个字典是一个用例
all_cases = read_data(exc_path,"搜索")

# 第二步： pytest测试用例方法
@pytest.mark.parametrize("data",all_cases)
def test_search_case(data):
    resp = requests_api(data)
    expected = data["预期结果"]  # 从excel读取预期结果
    response_assert(expected,resp)

