from article import Article


class Event:
    """Collection of news articles with shared topic.

    Attributes:
        articles (list): group of relevant articles.
        title (str): Short summary of articles.
    """

    def __init__(self, articles: list[Article], title: str = None):
        self.articles = articles
        self.title = title