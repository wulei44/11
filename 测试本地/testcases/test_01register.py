import unittest
import os
import requests
import random
from unittestreport import ddt, list_data
from common.handle_Excel import Login_Excel
from common.handle_path import data_path
from common.handle_log import my_log
from common.handle_conf import conf
from common.handle_asser import asser_indic
from common.handle_mysql import HandleDB

excel = Login_Excel(os.path.join(data_path, "cases.xlsx"), "register")
case = excel.login_excel_read()
# 接口ip地址
base_url = conf.get("env", "base_url")
 # 请求头
headers = eval(conf.get("env", "headers"))
@ddt
class TestRegister(unittest.TestCase):
    # excel = Login_Excel(os.path.join(data_path, "cases.xlsx"), "register")
    # case = excel.login_excel_read()
    # base_url = conf.get("env", "base_url")
    # headers = eval(conf.get("env", "headers"))
    @list_data(case)
    def test_register(self, item):
        # 1.准备用例数据
        # 接口地址
        url = base_url + item["url"]
        # 接口请求参数
        # 替换随机手机号
        phones_a=self.phones()
        if "#phone#" in item["data"]:
            item["data"] = item["data"].replace("#phone#", phones_a)
        params = eval(item["data"])
        # 请求方法
        method = item["method"].lower()
        # 预期结果
        expected = eval(item["expected"])
        row = item["case_id"] + 1
        # 2.调用测试接口,返回实际结果
        response = requests.request(method=method, url=url, json=params, headers=headers)
        response_json = response.json()
        try:
            asser_indic(expected, response_json)
            if response_json["msg"] == "OK":
                if HandleDB.find_one(sql="SELECT mobile_phone FROM future.member WHERE mobile_phone ={}".format(
                        phones_a)) == None:
                    HandleDB.close()
                    return AssertionError

        except AssertionError as e:
            # 根据需要回写Excel，回写需要耗费大量时间
            excel.write_data(row=row, column=8, value="不通过")
            my_log.error("注册接口用例--【{}】--用例未通过".format(item["title"]))
            # 记录详细的错误信息到日志
            # my_log.exception(e)
            raise e
        else:
            excel.write_data(row=row, column=8, value="pass")
            my_log.info("注册接口用例--【{}】--用例通过".format(item["title"]))

    def phones(self):
        phone = str(random.randint(15600000000, 15699999999))
        return phone
