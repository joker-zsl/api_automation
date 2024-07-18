"""
用户名有长度要求： 4-16位长度的用户名

因为这些生成数据的方法可能需要后续进行扩展： 生成其他的数据。
所以可以把这些方法都当到一个类里。 统一管理。

思考：这个函数应该在哪里执行呢？
思路：
1、执行第一个接口的时候，需要替换掉参数里的占位符位置-- 调用函数并执行函数的结果

"""

from faker import Faker
from tools.handle_mysql import HandleMysql
from datas.db_data import my_db

class GenData:
    def gen_unregister_phone(self):
        fk = Faker(locale="zh_CN")
        while True:
            # 第一步：调用faker类生成手机号码
            phone_number = fk.phone_number()
            # 第二步：把生成的数据去数据库里确认是否真的不重复
            sql = f'select * from tz_user where user_mobile = "{phone_number}"'
            sql_result = HandleMysql(**my_db).query_data(sql)
            if sql_result is not None: # 如果数据里有这个号码 继续生成 循环
                continue
            else:  # 如果数据里没有这个号码 得到号码 跳出循环
                return phone_number

    def gen_unregister_name(self):
        fk = Faker(locale="zh_CN")
        while True:
            # 第一步：调用faker类生成用户名
            username = fk.user_name()
            # 第二步：把生成的数据去数据库里确认是否真的不重复
            sql = f'select * from tz_user where user_name = "{username}"'
            sql_result = HandleMysql(**my_db).query_data(sql)
            if sql_result is not None or (len(username) < 4 or len(username) > 16): # 如果数据里有这个号码 继续生成 循环
                continue
            else:  # 如果数据里没有这个号码 得到号码 跳出循环
                return username

if __name__ == '__main__':
    print(GenData().gen_unregister_phone())
    print('GenData().gen_unregister_name()')
    result = eval('GenData().gen_unregister_name()')
    print(result)
