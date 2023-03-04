import time
from typing import Callable

from news import Config


def scheduler(task: Callable):
    """定时任务"""
    print("\n                                      --------------------------------- ")
    print("                                     |                                 |  ")
    print("                                     |            任务开始              |   ")
    print("                                     |                                 |  ")
    print("                                      ---------------------------------\n ")
    while True:
        time_now = time.strftime("%H:%M", time.localtime())  # 刷新
        if time_now == Config.get_config("task", "time"):  # 设置要执行的时间
            task()
            time.sleep(61)  # 停止执行61秒，防止反复运行程序。
