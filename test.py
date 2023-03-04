import datetime

from news import GetNews

news_test = GetNews.get_news(datetime.date.today())

print(news_test)