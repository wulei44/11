
import pymysql.cursors
from common.handle_conf import conf
from handle_log import my_log
class HandleDb:
    def __init__(self,
                 # host=configIni.get("mysql", "host"),
                 # user=configIni.get("mysql", "user"),
                 # password=configIni.get("mysql", "passwd"),
                 # port=configIni.getint("mysql", "port"),
                 # db=configIni.get("mysql", "db"),

                 host=conf.get("mysql", "host"),
                 port=conf.getint("mysql", "port"),
                 user=conf.get("mysql", "user"),
                 password=conf.get("mysql", "password")

                 ):
        try:
            # 1、建立连接
            self.conn = pymysql.connect(host=host,
                                        user=user,
                                        password=password,
                                        port=port,
                                        # db=db,
                                        # cursorclass=pymysql.cursors.DictCursor,  # 数据是字典格式
                                        autocommit=True)  # 修改数据自动提交,对数据库做修改时，会有个频繁提交过程
            # 2、建立游标
            self.cur = self.conn.cursor()
        except   :

            my_log.info("数据库连接失败！！请检查")
            raise

    # 获取查询结果的个数
    def get_count(self, sql, args=None):
        self.conn.commit()  # autocommit=True 类似
        return self.cur.execute(sql, args)

    # 获取查询的一条数据/1个数据
    def find_one(self, sql, args=None):
        self.conn.commit()  # autocommit=True 类似
        self.cur.execute(sql, args)
        return self.cur.fetchone()

    # 获取查询到的所有数据
    def get_all(self, sql, args=None):
        self.conn.commit()  # autocommit=True 类似
        self.cur.execute(sql, args)
        return self.cur.fetchall()

    # 修改数据 - 事务的回滚(rollback)和提交(commit) - 事务的4个特性
    def update(self, sql, args=None):  # autocommit=True 每改一条commit，太频繁了，对于测试影响不大
        self.cur.execute(sql, args)
        # self.conn.commit()

    # 关闭连接
    def close(self):
        self.cur.close()
        self.conn.close()


HandleDB = HandleDb(
    conf.get("mysql", "host"),
    conf.getint("mysql", "port"),
    conf.get("mysql", "user"),
    conf.get("mysql", "password"),
)

if __name__ == '__main__':
    hd = HandleDb()
    # count = hd.get_count('select * from futureloan.member where mobile_phone=15500000000;')
    sql = "sELECT STATUS FROM future.loan WHERE id =85904"
    count = hd.find_one(sql)
    print(count)


# import pymysql.cursors
# from python_file.day_26_project.common.handle_conf import conf
#
#
# class HandleMysql():
#     def __init__(self, host, port, user, password, *args, **kwargs):
#         self.con = pymysql.connect(
#             host=host,
#             port=port,
#             user=user,
#             password=password,
#             charset="utf8",
#             # cursorclass=pymysql.cursors.DictCursor,
#             *args,
#             **kwargs
#         )
#
#     def find_all(self, sql):
#         with self.con as cur:
#             cur.execute(sql)
#             res = cur.fetchall()
#             cur.close()
#         return res
#
#     def find_one(self, sql):
#         with self.con as cur:
#             cur.execute(sql)
#             res = cur.fetchone()
#             cur.close()
#         return res
#
#
# HandleDB = HandleMysql(
#     conf.get("mysql", "host"),
#     conf.getint("mysql", "port"),
#     conf.get("mysql", "user"),
#     conf.get("mysql", "password"),
# )
