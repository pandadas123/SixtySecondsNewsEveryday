import requests
import re
import datetime

from news import NewsDatabase
from news import Utils

"""获取每天60秒读懂世界文章
"""


def get_original_content() -> str:
    """
    从指定知乎获取文章原始内容
    :return: 返回获取到的内容
    """
    url_zhihu = "https://www.zhihu.com/api/v4/columns/c_1261258401923026944/items"  # 文章api
    param = "limit=1"  # 设置限制的数量
    origin_contents = requests.get(url=url_zhihu, params=param).text  # 发送请求
    return origin_contents


def regex_match(contents: str) -> list:
    """
    用正则表达式找到有效内容
    :param contents: 抓取的原始文章内容
    :return: 原始内容用正则表达式截取后的内容
    """
    match_p = re.compile(r"<p\s+data-pid=[^<>]+>([^<>]+)<\\/p>")  # 首次匹配规则：获取带有data-pi的p标签
    match_content = re.compile(r"(?<=>)\S+(?=<)")  # 获取p标签内容,带有ASCII码

    contents_p = re.finditer(match_p, contents)  # 带有p标签的内容
    contents_ascii = []                          # 去除p标签，带有ASCII码的内容
    for item in contents_p:      # 对每个p标签获取包裹的内容
        contents_ascii.append(re.search(match_content, item.group()).group())
    return contents_ascii[2:]  # 截去没用的部分


def ascii_replace(contents: list) -> list:
    """
    将带有ASCII码的内容转化为utf-8
    :param contents: 内容列表
    :return: 转化后的列表
    """
    match = []
    match_ascii = re.compile(r"&#(\d+);")  # 匹配ASCII码
    for item in contents:                  # 对每一条进行转换
        match_final = re.sub(match_ascii, Utils.ascii2utf8, item)                # 将ASCII码转化为字符
        match_utf8 = match_final.encode('utf-8').decode('unicode_escape')  # 将Unicode转化为utf8
        match.append(match_utf8)
    return match


def get_news(time) -> str:
    """
    整合操作获取字符串形式的文章
    :return: 返回文章
    """
    news_db, is_exist = NewsDatabase.get_article(time)
    if is_exist:
        return news_db
    elif time == datetime.date.today():
        con_origin = get_original_content()   # 获取原始内容
        con_ascii = regex_match(con_origin)   # 正则匹配
        news_list = ascii_replace(con_ascii)  # ASCII转化
        news_online = Utils.list2string(news_list)   # 列表转字符串
        NewsDatabase.add_article(news_online)  # 保存到数据库
        return news_online
    else:
        return news_db
