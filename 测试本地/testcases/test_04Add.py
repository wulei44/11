"""
==================================
Author:叶敏松
Time：2022/5/6 0006   17:09
奥利给-奥利给
==================================
"""
# 需要先进行登入（类级别前置）
# 提取用户ID 、token添加进信息头

import unittest
import os
import requests
from unittestreport import ddt,list_data
from common.handle_Excel import Login_Excel
from common.handle_path import data_path
from common.handle_conf import conf
from common.handle_data import replace_data
from common.handle_asser import asser_indic
from common.handle_log import my_log
from common.handle_mysql import HandleDB
from testcases.base import Base


@ddt
class Test_Add(unittest.TestCase,Base):
    excel = Login_Excel(filename=os.path.join(data_path, "cases.xlsx"), sheetname="Add")
    case = excel.login_excel_read()
    db = HandleDB

    @classmethod
    def setUpClass(cls) :
        # 1.用户登入
        cls.user_login()


    @list_data(case)
    def test_add(self,item):
        # 准备数据
        # 动态数据替换
        item["data"] = replace_data(Test_Add,item["data"])
        params = eval(item["data"])
        expected = eval(item["expected"])
        url = conf.get("env","base_url")+item["url"]

        method = item["method"]
        sql = f"SELECT * FROM future.loan WHERE member_id = {self.user_member_id}"
        # 查询此用户创建的项目前的数量
        start_count = len(self.db.get_all(sql=sql))
        response = requests.request(url=url,method=method,headers=self.header,json=params)
        res = response.json()
        # 数据库查询此用户创建的项目后的数量
        end_count = len(self.db.get_all(sql=sql))
        try:
            asser_indic(expected=expected,response=res)
            if res["msg"] == "OK":
                self.assertEqual(end_count-start_count,1)
            # else:
            #     self.assertEqual(end_count-start_count,0)
        except AssertionError as e:
            self.excel.write_data(row=item['case_id']+1,column=8,value='不通过')
            my_log.error("-----【{}】----用例未通过".format(item["title"]))
            raise e
        else:
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='pass ')
            my_log.info("-----【{}】----用例通过".format(item["title"]))


