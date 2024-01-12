from unittestreport import TestRunner
import unittest
import os
from common.handle_path import testcases_path, report_path

res = unittest.defaultTestLoader.discover(testcases_path)
runner = TestRunner(res, filename=os.path.join(report_path, "python123.html"))
runner.run()
runner.send_email(host="smtp.qq.com",
                      port=465,
                      user="2206256132@qq.com",
                      password="wqheqcpudmwceaec",
                      to_addrs="2206256132@qq.com",
                      is_file=True)
