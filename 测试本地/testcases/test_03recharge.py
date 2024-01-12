"""
充值的前提： 登入---> 提取token

unittest：
    用例级别的前置：setUp
    测试类级别的前置： setUpClass

"""
import unittest
import requests
import os
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from python_file.day_27_project.common.handle_conf import conf
from python_file.day_27_project.common.handle_Excel import Login_Excel
from python_file.day_27_project.common.handle_path import data_path
from python_file.day_27_project.common.handle_asser import asser_indic
from python_file.day_27_project.common.handle_log import my_log
from python_file.day_27_project.common.handle_mysql import HandleDB
from python_file.day_27_project.common.handle_data import replace_data
from  python_file.day_27_project.testcases.base import Base




@ddt
class TestRecharge(unittest.TestCase,Base):
    excel = Login_Excel(os.path.join(data_path, "cases.xlsx"), "recharge")
    case = excel.login_excel_read()
    base_url = conf.get("env", "base_url")
    @classmethod
    def setUpClass(cls):

        # cls.user_login()
        # params = eval(conf.get("test_data", "recharge_user"))
        # cls.mobile_phone = params["mobile_phone"]

        # 1.准备数据
        url = cls.base_url + "/member/login"
        header = eval(conf.get("env", "headers"))
        params = eval(conf.get("test_data", "recharge_user"))
        response = requests.post(url=url, headers=header, json=params)
        res = response.json()
        # 2.登入成功后去提取token
        token = jsonpath(res, "$..token")[0]
        # 将token添加进请求头中
        header["Authorization"] = "Bearer " + token
        # 保存含有token的请求头为类属性
        cls.header = header
        # # setattr(TestRegister,"handles",handle)
        # 2.提取mobile_id
        mobile_id = jsonpath(res, "$..id")[0]
        cls.member_id = mobile_id
        cls.mobile_phone = params["mobile_phone"]
    @list_data(case)
    def test_recharge(self, item):
        # 准备数据
        url =self.base_url + item["url"]
        method = item["method"].lower()
        # 通过字符串替换方法 动态设置参数
        # item["data"] = item["data"].replace("#member_id#", str(self.mobile_id))
        item["data"] = replace_data(cls=TestRecharge,data=item["data"])
        params = eval(item["data"])
        expected = eval(item["expected"])
        # 请求数据库查询余额
        sql = "SELECT leave_amount FROM future.member WHERE mobile_phone ={}".format(self.mobile_phone)
        start = HandleDB.find_one(sql)[0]
        # 调用接口
        response = requests.request(method=method, url=url, headers=self.header, json=params)
        res = response.json()
        # 请求数据库查询余额
        sql = "SELECT leave_amount FROM future.member WHERE mobile_phone ={}".format(self.mobile_phone)
        end = HandleDB.find_one(sql)[0]
        # 断言
        try:
            asser_indic(expected=expected, response=res)
            if res["msg"]=="OK":
                self.assertEqual(float(end-start),float(params["amount"]))
        except AssertionError as e:
            self.excel.write_data(row=item['case_id'] + 1, column=8, value='不通过 ')
            my_log.error("-----【{}】----用例未通过".format(item["title"]))
            raise e
        else:
            self.excel.write_data(row=item['case_id'] + 1, column=8, value="pass")
            my_log.info("-----【{}】----用例通过".format(item["title"]))
