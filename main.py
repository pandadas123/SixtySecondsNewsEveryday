from news import ScheduledTask
from news.MailPoster import news_post

if __name__ == "__main__":
    ScheduledTask.scheduler(news_post)