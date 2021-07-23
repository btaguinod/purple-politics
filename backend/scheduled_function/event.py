import shortuuid

from article import Article


class Event:
    """Collection of news articles with shared topic.

    Attributes:
        articles (list): group of relevant articles.
        event_id (str): Event identifier.
    """

    def __init__(self, articles: list[Article], event_id: str = None):
        self.articles = articles
        self.event_id = str(shortuuid.uuid()) if event_id is None else event_id
