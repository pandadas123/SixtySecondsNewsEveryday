import configparser
import os


# 获取config配置文件
def get_config(section, key):
    config = configparser.ConfigParser()

    #      os.path.split(os.path.realpath(__file__))[0] 得到的是当前文件模块的目录
    path = os.getcwd() + os.sep + 'global.conf'

    config.read(path, "utf8")
    return config.get(section, key)
