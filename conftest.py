"""
执行一个接口执行之前 先要执行另外一个接口 获取数据【token】 给到下一个使用：
- pytest的夹具
- yield 返回值
- conftest 共享

定义夹具 获取token


"""
import pytest
import requests
from jsonpath import jsonpath


@pytest.fixture()
def login_fixture():
    url_login = "http://shop.lemonban.com:8107/login"
    param = {"principal": "lemon_py", "credentials": "12345678", "appType": 3, "loginType": 0}
    resp = requests.request("post",url=url_login,json=param)
    access_token = jsonpath(resp.json(), "$..access_token")[0]  # jsonpath 提取数据
    token_type = jsonpath(resp.json(), "$..token_type")[0]
    token = token_type+access_token
    yield token  # 夹具的返回值
