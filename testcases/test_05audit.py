"""
==================================
Author:叶敏松
Time：2022/5/7 0007   18:09
奥利给-奥利给
==================================
"""
# 审核项目
# 每次审核都需要创建一个项目 并获取此次的项目ID     ----> 创建项目（用例级别前置）
# 需要两个账号： 管理员账号（用于审核 ） 普通账号（新建项目） ---> 类级别前置


import unittest
import os
import requests
from unittestreport import ddt, list_data
from common.handle_Excel import Login_Excel
from common.handle_path import data_path
from common.handle_conf import conf
from jsonpath import jsonpath
from common.handle_data import replace_data
from common.handle_mysql import HandleDB
from common.handle_log import my_log
from testcases.base import Base

excl = Login_Excel(filename=os.path.join(data_path, "cases.xlsx"), sheetname="audit")
db = HandleDB
case = excl.login_excel_read()

@ddt
class TestAudit(unittest.TestCase,Base):
    @classmethod
    def setUpClass(cls) -> None:
        # 1. 普通用户登入
        cls.user_login()

        # 2. 管理员登入
        cls.admin_login()

    def setUp(self) -> None:
        # 创建项目
        self.add_project()

    @list_data(case)
    def test_audit(self, item):
        # 准备数据
        url = conf.get("env", "base_url") + item["url"]
        item["data"] = replace_data(TestAudit, item["data"])
        params = eval(item["data"])
        expected = eval(item["expected"])
        # 调用接口
        response = requests.request(url=url, method=item["method"], headers=self.admin_header, json=params)
        res = response.json()
        # 保存审核通过的项目为 pass_loan_id
        if item["title"] == "审核通过" and res["msg"] == "OK":
            TestAudit.pass_loan_id = jsonpath(params, "$..loan_id")[0]

        # 断言
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 数据库查询
            if res["msg"] == "OK":
                status = db.find_one(sql=f"SELECT STATUS FROM future.loan WHERE id = {self.loan_id}")[0]
                self.assertEqual(status, expected["status"])
        except AssertionError as  e:
            # 记录日志
            my_log.error("-----【{}】----用例未通过".format(item["title"]))
            raise e
        else:
            my_log.info("-----【{}】----用例通过".format(item["title"]))
