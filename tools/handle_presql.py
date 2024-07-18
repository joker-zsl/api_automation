"""
1、def封装
2、参数化
3、返回值： 因为数据都存在环境变量 所以不需要返回值
4、加上日志： 但凡你想确认数据结果的地方 都可以加上日志
5、因为有些接口不需要做前置SQL，所以判空处理：

"""
import json
from tools.handle_mysql import HandleMysql
from datas.db_data import my_db
from tools.envi_data import EnviData
from loguru import logger

def pre_sql(sql_data):
    if sql_data is None:
        return
    # 第一步： 字符串做反序列化操作--转化为字典
    logger.info("---------------------前置SQL执行开始-------------------------")
    sql_data = json.loads(sql_data)
    logger.info(f"前置sql提取表达式为：{sql_data}")
    # 第二步： 分别得到key 和value ==for遍历 items()
    for k,v in sql_data.items(): # k 是变量变量名- mobile_code，v是sql语句
        sql_result = HandleMysql(**my_db).query_data(v)  # 结果是字典 {'mobile_code': '845305'}
        # 第三步： 查完后结果存储在环境变量作为属性。属性名就是k 变量名；mobile_code
        for i,j in sql_result.items(): # i 是变量名 j 是v属性值
            setattr(EnviData,i,j)  # 把结果存在环境变量里
    logger.info(f"提取并设置环境变量之后的类属性是：{EnviData.__dict__}")


if __name__ == '__main__':
    sql_data = '''{"mobile_code":
        "select mobile_code  from tz_sms_log where user_phone='13422337768' order by rec_date desc limit 1;"}'''
    pre_sql(sql_data)