import time
from datetime import datetime
from typing import Callable

from news import Config


def scheduler(task: Callable):
    """定时任务，需要任务在半小时内完成一次"""
    print("\n                                      --------------------------------- ")
    print("                                     |                                 |  ")
    print("                                     |            任务开始              |   ")
    print("                                     |                                 |  ")
    print("                                      ---------------------------------\n ")
    while True:
        time_task = datetime.strptime(Config.get_config("task", "time"), "%H:%M:%S")           # 获取任务时间
        time_now = datetime.strptime(time.strftime("%H:%M:%S", time.localtime()), "%H:%M:%S")  # 获取当前时间
        duration = (time_task - time_now).seconds  # 计算时间差
        time.sleep(int(duration))                  # 暂停执行
        task()  # 执行任务
        time.sleep(23.5 * 60 * 60)                   # 在下次任务时间点前半小时开始下次循环
