import re


def ascii2utf8(str_matched: re.Match) -> str:
    """
    ASCII码转换工具，传入数字转为字符
    :param str_matched: 将要匹配的字符串
    :return: 转化后的字符串
    """
    ascii_str = str_matched.group(1)    # 匹配到的ASCII码，字符串
    ascii_char = chr((int(ascii_str)))  # 将ASCII码转化为对应的字符
    return ascii_char


def ascii_replace(contents: list) -> list:
    """
    将带有ASCII码的内容转化为utf-8
    :param contents: 内容列表
    :return: 转化后的列表
    """
    match = []
    match_ascii = re.compile(r"&#(\d+);")  # 匹配ASCII码
    for item in contents:                  # 对每一条进行转换
        match_final = re.sub(match_ascii, ascii2utf8, item)                # 将ASCII码转化为字符
        match_utf8 = match_final.encode('utf-8').decode('unicode_escape')  # 将Unicode转化为utf8
        match.append(match_utf8)
    return match


def list2string(content_list: list) -> str:
    """
    python列表转化为字符串，用换行符分割
    :param content_list: 列表形式的文章内容
    :return: 一整个的字符串文章
    """
    return "\n\n".join(content_list)  # "\n"表示分隔符为换行符


def string2list(string: str) -> list:
    """
    类似于  `string1  排列的特殊字符串转化为列表
            string2
            string3`
    :param string: 要转化的字符串
    :return: 列表
    """
    return string.split()


def receivers_list2str(receivers_list: list) -> str:
    """
    将列表类型的邮件接受者转化为以逗号分隔的字符串
    :param receivers_list: 接受列表形式的邮件接受者
    :return: 返回以逗号分隔的字符串
    """
    return ",".join(receivers_list)


def get_receivers(receivers_conf: str) -> str:
    """
    将配置文件里的receivers转化为以逗号分隔的字符串，便于邮件发送
    :param receivers_conf: 配置文件中的receivers
    :return: 逗号分隔的字符串
    """
    receivers_list = string2list(receivers_conf)
    return receivers_list2str(receivers_list)
