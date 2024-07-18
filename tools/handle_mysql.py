import pymysql
from pymysql.cursors import DictCursor
from loguru import logger

class HandleMysql:
    def __init__(self,user,password,database,port,host):
        """
        定义了两个实例属性： conn cursor ，可以用于后续实例方法共享。
        """
        self.conn = pymysql.connect(
            user=user,
            password=password,
            database=database,
            port=port,
            host=host,
            charset="utf8mb4",
            cursorclass=DictCursor)
        self.cursor = self.conn.cursor()
    def query_data(self,query_sql,match_num=1,size=None):
        """

        :param query_sql: 查询sql语句
        :param match_num: 用户获取条数 match_num=1，fetchone；match_num=2，fetchmany，match_num=-1，fetchall
        :param size:当match_num=2，size是查询的条数，传参。
        :return: 返回查询结果数据
        """
        try:
            result = self.cursor.execute(query_sql)  # 结果条数 >0 才有获取详细数据必要
            logger.info(f"数据库的查询结果条数为：{result}")
            if result > 0:
                if match_num==1:
                    data = self.cursor.fetchone()
                    logger.info(f"查询结果数据为：{data}")
                    return data
                elif match_num == 2:
                    data = self.cursor.fetchmany(size = size)
                    logger.info(f"查询结果数据为：{data}")
                    return data
                elif match_num == -1:
                    data = self.cursor.fetchall()
                    logger.info(f"查询结果数据为：{data}")
                    return data
                logger.warning("请传入1,2,-1的match_num")
            logger.info("数据库没有查询结果！")
        except:
            logger.error("数据库操作异常！")
        finally:
            self.cursor.close()
            self.conn.close()

if __name__ == '__main__':
    my_db = {
        "user": "lemon_auto",
        "password": "lemon!@123",
        "database": "yami_shops",
        "port": 3306,
        "host": "mall.lemonban.com"}

    sql = "select mobile_code  from tz_sms_log where user_phone='13645321122' order by rec_date desc limit 1;"
    result = HandleMysql(**my_db).query_data(sql)
    print(result)