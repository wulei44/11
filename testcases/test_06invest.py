"""
==================================
Author:叶敏松
Time：2022/5/8 0008   17:27
奥利给-奥利给
==================================
"""
# 前置条件
#   1.用户登入、充值 （类前置）
#   2. 管理员登入 （类前置）
#   3. 创建项目 （类前置）
#   4. 审核项目 （类前置）
#   5. 用户进行投资 （执行用例）

# 用例方法
#   1.准备数据
#   2.发送请求
#   3.断言

# 数据库校验
#     1.用户表：用户的余额前后变化
#         投资前-投资后 == 投资金额
#     2.流水记录表：投资成功后新增一条流水记录
#         投资后的流水记录数量 - 投资前的流水记录数量 == 1
#     3.投资表：投资成功会新增一条投资记录
#         投资后用户的投资记录数量-投资前用户的投资记录数量 == 1
#     4.投资后（可投金额为0）满标情况，会生成回款计划  （比较麻烦没有使用代码实现）
#         1）、先把项目的投资记录ID全部查询出来
#         2）、遍历投资记录ID
#         3）、根据每个投资记录ID去查询是否生成回款计划表


import unittest
import os
import requests
from unittestreport import ddt, list_data
from common.handle_Excel import Login_Excel
from common.handle_path import data_path
from testcases.base import Base
from common.handle_conf import conf
from common.handle_data import replace_data
from common.handle_log import my_log
from common.handle_mysql import HandleDB



@ddt
class TestInvest(unittest.TestCase,Base):
    excel = Login_Excel(os.path.join(data_path, "cases.xlsx"), "invest")
    case = excel.login_excel_read()
    db = HandleDB
    @classmethod
    def setUpClass(cls) -> None:
        # 1.用户登入
        cls.user_login()

        # 2. 管理员登入
        cls.admin_login()
        # 3. 创建项目
        cls.add_project()
        # 4. 审核项目
        cls.audit()

    @list_data(case)
    def test_invest(self, item):
        url = conf.get("env", "base_url") + item["url"]
        expected = eval(item["expected"])
        item["data"] = replace_data(TestInvest, item["data"])
        # -------------用例执行前数据库查询--------------
        # 执行成功的用例去数据库查询
        if item["sql"]:
            sql1 = f"SELECT leave_amount from future.member WHERE id = {self.user_member_id}"
            sql2 = f"SELECT count(*) from future.invest WHERE member_id = {self.user_member_id}"
            sql3 = f"SELECT count(*) from future.financelog WHERE pay_member_id = {self.user_member_id}"
            # 查询数据库用户余额变化
            s_member=self.db.find_one(sql=sql1)[0]

            # 查询数据库用户的投资记录条数
            print(type(s_member))
            s_invest = self.db.find_one(sql=sql2)[0]
            # 查询数据库用户的流水记录条数
            s_financelog = self.db.find_one(sql=sql3)[0]

        params = eval(item["data"])
        response = requests.request(url=url, method=item["method"], headers=self.header, json=params)
        res = response.json()
        # -------------用例执行后数据库查询--------------
        # 执行成功的用例去数据库查询
        if item["sql"]:
            sql1 = f"SELECT leave_amount from future.member WHERE id = {self.user_member_id}"
            sql2 = f"SELECT count(*) from future.invest WHERE member_id = {self.user_member_id}"
            sql3 = f"SELECT count(*) from future.financelog WHERE pay_member_id = {self.user_member_id}"
            # 查询数据库用户余额变化
            e_member = self.db.find_one(sql=sql1)[0]

            # 查询数据库用户的投资记录条数
            e_invest = self.db.find_one(sql=sql2)[0]
            # 查询数据库用户的流水记录条数
            e_financelog = self.db.find_one(sql=sql3)[0]
        try:
            self.assertEqual(expected["code"], res["code"])
            # 断言实际结果中的msg是否包含，预期结果中的msg内容。
            self.assertIn(expected["msg"], res["msg"])
            if item["sql"]:
                # 断言：投资前-投资后 == 投资金额
                self.assertEqual(str(s_member - e_member), params["amount"])
                # 投资后的流水记录数量 - 投资前的流水记录数量 == 1
                self.assertEqual(e_financelog-s_financelog, 1)
                # 投资后用户的投资记录数量-投资前用户的投资记录数量 == 1
                self.assertEqual(e_invest-s_invest, 1)
        except AssertionError as e:
            my_log.error("-----【{}】----用例未通过".format(item["title"]))
            raise e
        else:
            my_log.info("-----【{}】----用例通过".format(item["title"]))
