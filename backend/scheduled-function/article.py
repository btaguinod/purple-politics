from company import Company
from text_info import TextInfo


class Article:
    """Representation of online news article.

    Attributes:
        company (Company): Company name.
        title (str): Article title.
        description (str): First lines of article.
        article_url (str): Link to article.
        image_url (str): Link to article thumbnail.
        published_time (str): Time article was posted in ISO 8601 format
    """

    def __init__(self, company: Company, title: str, description: str,
                 published_time: str, article_url: str, image_url: str,
                 text_info: TextInfo = None):
        self.company = company
        self.title = title
        self.description = description
        self.published_time = published_time
        self.article_url = article_url
        self.image_url = image_url
        self.text_info = text_info

    def __str__(self):
        return str(self.company) + ', ' + \
               self.title[:10] + ', ' + \
               self.description[:10] + ', ' + \
               self.published_time + ', ' + \
               self.article_url + ', ' + \
               self.image_url

    def __hash__(self) -> int:
        return hash(self.article_url)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Article):
            return self.article_url == o.article_url
        return False
