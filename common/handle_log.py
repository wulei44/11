import logging
import os
from   common.handle_conf import conf
from common.handle_path import log_path


class Create_log():
    def create_log(self, name="my_log", filename="logs.logs", level="DEBUG", sh_level="DEBUG", fh_level="DEBUG"):
        """

        :param name: 日志收集器名称
        :param filename: 输出到文件的地址
        :param level: 日志收集器收集错误的等级
        :param sh_level: 日志收集器输出到控制台的等级
        :param fh_level: 日志收集器输出到文件的等级
        :return: 返回一个日志收集器
        """
        # 第一步：创建日志收集器
        log = logging.getLogger(name)
        # 第二步：设置日志收集器的错误等级
        log.setLevel(level)
        # 第三步：设置输出渠道
        # 3.1：输出到控制台渠道
        sh = logging.StreamHandler()
        # 设置输出日志的等级
        sh.setLevel(sh_level)
        # 将输出渠道绑定到收集器上
        log.addHandler(sh)
        # 3.2:输出到文件渠道
        fh = logging.FileHandler(r"{}".format(filename), encoding="utf-8")
        # 设置输出日志的等级
        fh.setLevel(fh_level)
        # 将输出渠道绑定到收集器上
        log.addHandler(fh)
        # 第四步:设置日志输出格式
        formats = "%(asctime)s - [%(filename)s -->line：%(lineno)d] - %(levelname)s: %(message)s"
        # 4.1:创建格式对象
        log_format = logging.Formatter(formats)
        # 4.2：设置输出到控制台的格式
        sh.setFormatter(log_format)
        # 4.3：设置输出到文件的格式
        fh.setFormatter(log_format)

        # 返回一个日志收集器
        return log



my_log = Create_log().create_log(
    name=conf.get("logging", "name"),
    level=conf.get("logging", "level"),
    filename=os.path.join(log_path,conf.get("logging", "filename")),
    sh_level=conf.get("logging", "sh_level"),
    fh_level=conf.get("logging", "fh_level")
)
