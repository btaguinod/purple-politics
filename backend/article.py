

class Article:
    """Representation of online news article.

    Attributes:
        company (str): Company name.
        title (str): Article title.
        description (str): First lines of article.
        article_url (str): Link to article.
        image_url (str): Link to article thumbnail.
        published_time (str): Time article was posted in ISO 8601 format
    """

    def __init__(self, company: str, title: str, description: str,
                 article_url: str, image_url: str, published_time: str):
        self.company = company
        self.title = title
        self.description = description
        self.article_url = article_url
        self.image_url = image_url
        self.published_time = published_time

    def __str__(self):
        return self.company + ', ' + \
               self.title[:10] + ', ' + \
               self.description[:10] + ', ' + \
               self.article_url + ', ' + \
               self.image_url + ', ' + \
               self.published_time
