import datetime

import pymysql
from DBUtils.PooledDB import PooledDB, PooledDBError, PooledDedicatedDBConnection
from DBUtils.SteadyDB import SteadyDBCursor

from news import Config

# 创建数据库连接池
pool = PooledDB(creator=pymysql,  # 使用链接数据库的模块
                maxconnections=10,  # 连接池允许的最大连接数，0和None表示不限制连接数
                mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
                maxcached=8,  # 链接池中最多闲置的链接，0和None不限制
                host=Config.get_config("database", "host"),
                user=Config.get_config("database", "username"),
                password=Config.get_config("database", "password"),
                database=Config.get_config("database", "database"),
                charset=Config.get_config("database", "charset"),
                port=int(Config.get_config("database", "port")))


def get_connection() -> (PooledDedicatedDBConnection, SteadyDBCursor):
    """获取连接"""
    try:
        connection = pool.connection()
        cursor = connection.cursor()
        return connection, cursor
    except PooledDBError as e:
        print("Failed to create connection {}".format(e))
        raise IOError


def get_article(time: datetime.date) -> (str, bool):
    """
    获取指定日期文章
    :param time: 日期
    :return: 元组（str, bool)
    """
    connection, cursor = get_connection()  # 获取连接
    try:
        # 添加文章语句
        sql = "SELECT `articles` FROM news WHERE `time`=%s"
        cursor.execute(sql, time)
        connection.commit()
        result = cursor.fetchone()
        if result is not None:
            return result[0], True  # 返回文章结果和成功标志
        else:
            return "暂无文章", False  # 返回默认信息和失败标志
    except PooledDBError as e:
        print("新增文章失败 {}".format(e))
    finally:
        cursor.close()
        connection.close()


def add_article(content: str):
    """增加当天的文章"""
    connection, cursor = get_connection()  # 获取连接
    try:
        cursor = connection.cursor()
        # 添加文章语句
        sql = "INSERT INTO `news` (`time`, `articles`) VALUES (CURRENT_DATE, %s)"
        cursor.execute(sql, content)
        connection.commit()
    except PooledDBError as e:
        print("保存文章失败 {}".format(e))
    finally:
        cursor.close()
        connection.close()
