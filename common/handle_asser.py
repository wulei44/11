"""字典成员断言"""


def asser_indic(expected, response):
    """

    :param expected: 预期结果
    :param response: 实际结果
    :return: 断言错误信息
    """
    for k, v in expected.items():
        if response.get(k) != None and response.get(k) == v:
            pass
        else:
            raise AssertionError(f"实际结果：{response}---- not in ------预期结果：{expected}")
