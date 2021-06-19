

class Article:
    def __init__(self, company: str, title: str, description: str,
                 article_url: str, image_url: str, published_time: str):
        self.company = company
        self.title = title
        self.description = description
        self.article_url = article_url
        self.image_url = image_url
        self.published_time = published_time
