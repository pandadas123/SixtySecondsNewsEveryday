import datetime
import smtplib
import time
from email.mime.text import MIMEText

from news import GetNews, Utils
from news import Config

"""发送邮件
"""


def mail_post(receivers: str, title: str, content: str) -> bool:
    """
    发送邮件工具
    :param receivers: 接收者，列表，可以有多个
    :param title: 标题
    :param content: 内容
    :return: 是否成功
    """
    # 设置服务器所需信息
    # 163邮箱服务器地址
    mail_host = Config.get_config("mail", "mail_host")
    # 163用户名
    mail_user = Config.get_config("mail", "mail_user")
    # 密码(部分邮箱为授权码)
    mail_pass = Config.get_config("mail", "mail_pass")
    # 邮件发送方邮箱地址
    sender = Config.get_config("mail", "sender")

    # 设置email信息
    # 邮件内容设置
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = title
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers

    # 登录并发送邮件
    try:
        # 连接到服务器
        smtp = smtplib.SMTP_SSL(mail_host)
        # 登录到服务器
        smtp.login(mail_user, mail_pass)
        # 发送
        smtp.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtp.quit()
        return True
    except smtplib.SMTPException as e:
        print('邮件发送失败', e)  # 打印错误
        return False


def news_post():
    news = GetNews.get_news(datetime.date.today())
    title = Config.get_config("mail", "title")
    receivers = Utils.get_receivers(Config.get_config("mail", "receivers"))

    if mail_post(receivers, title, news):
        print("\n                               ------------------------------                                     ")
        print("                              | 发送成功 {}  |".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        print("                               ------------------------------                                     ")
        print("=====================================================================================================\n")
        print(news)
        print("\n=====================================================================================================")
    else:
        print("\n                               ------------------------------                                     ")
        print("                              | 发送失败 {}  |".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        print("                               ------------------------------                                     ")
