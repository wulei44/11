import os
from configparser import ConfigParser
from common.handle_path import conf_path


class Config(ConfigParser):
    def __init__(self, conf_file):
        """

        :param conf_file: ini 配置文件地址
        """
        super().__init__()
        self.read(conf_file, encoding="utf-8")


conf = Config(conf_file=os.path.join(conf_path, "config.ini"))


