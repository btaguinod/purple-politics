from article import Article
import feedparser
import time


class ArticleCollector:
    """Collector for online news articles.

    Attributes:
        company (str): Company name.
        url (str): RSS source URL.

    """

    def __init__(self, company, url):
        self.company = company
        self.url = url

    def get_articles(self, max_articles: int) -> list[Article]:
        """Get news articles using RSS feed.

        Attributes:
            max_articles: Maximum number of articles to return
        """

        articles = []
        entries = feedparser.parse(self.url).entries
        for entry in entries[:max_articles]:
            title = entry['title']
            description = entry['summary']
            article_url = entry['link']
            image_url = self._get_image_url(entry['media_content'])
            published_time = time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                           entry['published_parsed'])
            article = Article(self.company, title, description, article_url,
                              image_url, published_time)
            articles.append(article)
        return articles

    @staticmethod
    def _get_image_url(media_content: dict) -> str:
        image_sizes = dict()

        for media in media_content:
            content_type = None
            if 'medium' in media:
                content_type = media['medium']
            elif 'type' in media:
                content_type = media['type'][:5]

            if content_type == 'image':
                image_size = 0
                if 'height' in media and 'width' in media:
                    image_size = int(media['height']) * int(media['width'])
                elif 'isdefault' in media and media['isdefault'] == 'true':
                    image_size = float('inf')
                image_sizes[media['url']] = image_size
        return max(image_sizes, key=image_sizes.get)
