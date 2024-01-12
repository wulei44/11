"""
此模块专门处理新项目中的绝对路径


"""
import os

# 项目根目录的绝对路径
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 用例数据所在路径（Excel表）
data_path = os.path.join(base_path, "datas")

# 配置文件所在路径
conf_path = os.path.join(base_path, "conf")

# 日志文件所在目录
log_path = os.path.join(base_path,"logs")

# 报告路径
report_path = os.path.join(base_path,"reports")

# 封装模块路径
common_path = os.path.join(base_path,"common")

# 用例模块所在路径
testcases_path = os.path.join(base_path,"testcases")



