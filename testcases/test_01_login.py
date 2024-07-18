"""
集成之前学习的技术知识点测试电商项目的登录模块：
1、数据准备好在excel表格
2、代码封装工具【方法】 --handle_excel读取测试用例的数据
3、pytest测试框架执行这些测试用例数据-- 数据驱动
- 注意： 转化数据类型。
4、做接口结果： 断言方法封装 --下节课做

data = {'用例编号': 'login_001', '用例标题': '登录成功', '优先级': 'p1',
'请求方法': 'post', '接口地址': 'http://shop.lemonban.com:8107/login',
'请求头': '{"Content-Type":"application/json"}',
'请求参数': '{"principal": "lemon_py", "credentials": "12345678", "appType": 3, "loginType": 0}',
'预期结果': None}

注意：excel表格里读取的数据是字符串，用于接口 测试请求发送 一定要做数据类型转化。== 字符串-->字典。
- eval() : 脱引号
- json数据反序列化-- json格式数据 转化为Python字典。

"""
import json

import pytest
import requests
from tools.handle_response_assert import response_assert
from tools.handle_excel import read_data
from tools.handle_path import exc_path
from tools.handle_requests import requests_api

# 第一步： handle_excel读取测试用例的数据  --列表嵌套字典，每个字典是一个用例
all_cases = read_data(exc_path,"登录")

# 第二步： pytest测试用例方法
@pytest.mark.parametrize("data",all_cases)
def test_login_case(data):
    resp = requests_api(data)
    expected = data["预期结果"]
    response_assert(expected,resp)

