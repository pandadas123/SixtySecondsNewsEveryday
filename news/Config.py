import configparser
import os

config = configparser.ConfigParser()
#      os.path.split(os.path.realpath(__file__))[0] 得到的是当前文件模块的目录
path = os.getcwd() + os.sep + 'global.conf'


# 获取config配置文件
def get_config(section, key):
    global config, path
    config.read(path, "utf8")
    _config = config.get(section, key)
    config.clear()  # 清楚缓存，实时读取配置
    return _config
