import shortuuid

from article import Article


class Event:
    """Collection of news articles with shared topic.

    Attributes:
        articles (list): group of relevant articles.
    """

    def __init__(self, articles: list[Article]):
        self.event_id = shortuuid.uuid()
        self.articles = articles
