import unittest
import os
import requests
from unittestreport import ddt, list_data
from common.handle_Excel import Login_Excel
from common.handle_path import data_path
from common.handle_conf import conf
from common.handle_asser import asser_indic
from common.handle_log import my_log


@ddt
class TestLogin(unittest.TestCase):
    excel = Login_Excel(filename=os.path.join(data_path, "cases.xlsx"), sheetname="login")
    case = excel.login_excel_read()
    # 公共数据
    # 接口总地址（环境）
    base_url = conf.get("env", "base_url")
    # 请求头
    header = eval(conf.get("env", "headers"))


    @list_data(case)
    def test_login(self, item):
        # 1.准备用例数据
        # 接口地址
        url = self.base_url+item["url"]
        # 请求方法
        method = item["method"]
        # 预期结果
        expected = eval(item["expected"])
        # 请求数据
        params = eval(item["data"])
        # 2.发送请求返回实际结果
        response = requests.request(method=method,url=url,headers=self.header,json=params)
        res = response.json()
        # 3.断言，记录日志
        try:
            asser_indic(expected=expected,response=res)
        except AssertionError as e:
            self.excel.write_data(row=item["case_id"]+1,column=8,value="不通过")
            my_log.error("----登入接口用例：【{}】------用例未通过".format(item["title"]))
            # my_log.exception(e)
            raise e
        else:
            self.excel.write_data(row=item["case_id"] + 1, column=8, value="pass")
            my_log.info("----登入接口用例：【{}】------用例通过pass".format(item["title"]))
            # my_log.exception(e)



