"""
==================================
Author:叶敏松
Time：2022/5/9 0009   13:26
奥利给-奥利给
==================================
"""
import requests
from common.handle_conf import conf
from jsonpath import jsonpath


class Base:
    @classmethod
    def user_login(cls):
        url = conf.get("env", "base_url") + "/member/login"
        headers = eval(conf.get("env", "headers"))
        params = eval(conf.get("test_data", "user"))
        response = requests.request(url=url, method="post", headers=headers, json=params)
        res = response.json()
        token = jsonpath(res, "$..token")[0]
        member_id = jsonpath(res, "$..id")[0]
        headers["Authorization"] = "Bearer " + token
        cls.header = headers
        cls.user_member_id = member_id

    @classmethod
    def admin_login(cls):
        url = conf.get("env", "base_url") + "/member/login"
        headers = eval(conf.get("env", "headers"))
        params = eval(conf.get("test_data", "admin_user"))
        response = requests.request(url=url, method="post", headers=headers, json=params)
        res = response.json()
        token = jsonpath(res, "$..token")[0]
        headers["Authorization"] = "Bearer " + token
        cls.admin_header = headers

    @classmethod
    def add_project(cls):
        url = conf.get("env", "base_url") + "/loan/add"
        params = eval(conf.get("test_data", "add").replace("#member_id#", str(cls.user_member_id)))
        response = requests.request(url=url, method="post", headers=cls.header, json=params)
        res = response.json()
        loan_id = jsonpath(res, "$..id")[0]
        cls.loan_id = loan_id

    @classmethod
    def audit(cls):
        url = conf.get("env", "base_url") + "/loan/audit"
        params = {"loan_id": cls.loan_id, "approved_or_not": "true"}
        response = requests.request(url=url, method="patch", headers=cls.admin_header, json=params)
        res = response.json()
        cls.res = res
