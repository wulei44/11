"""
==================================
Author:叶敏松
Time：2022/4/22 0022   13:57
奥利给-奥利给
==================================
"""
import re
from common.handle_conf import conf


def replace_data(cls, data):
    """
    :param cls:  测试类
    :param data: 要替换的用例数据（字符串）
    :return:
    """
    while re.search("#(.+?)#", data):
        res2 = re.search("#(.+?)#", data)
        itme = res2.group()
        attr = res2.group(1)
        try:
            value = getattr(cls, attr)
        except AttributeError:
            value = conf.get("test_data",attr)

        # 数据替换
        data = data.replace(itme, str(value))

    return data
