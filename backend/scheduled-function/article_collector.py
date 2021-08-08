from article import Article
import feedparser
import time
from datetime import datetime, timedelta, timezone


def curr_time(offset: int = 0) -> str:
    """Returns current time with an offset.

    Args:
        offset (int): Number of offset days.

    Returns:
        str: time iso format.
    """

    return str((datetime.now(timezone.utc) + timedelta(offset)).isoformat())


class ArticleCollector:
    """Collector for online news articles.

    Attributes:
        company (str): Company name.
        url (str): RSS source URL.
    """

    def __init__(self, company, url):
        self.company = company
        self.url = url

    def get_articles(self, max_articles: int, start_time: str = curr_time(-3),
                     end_time: str = curr_time(0)) -> list[Article]:
        """Get news articles using RSS feed.

        Args:
            max_articles (int): Maximum number of articles to return.
            start_time (str): Earliest time to return.
            end_time (str): Latest time to return.

        Returns:
            list[Article]: Articles.
        """

        articles = []
        entries = feedparser.parse(self.url).entries
        for entry in entries[:max_articles]:
            if 'published_parsed' not in entry:
                continue
            published_time = time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                           entry['published_parsed'])
            if published_time < start_time or published_time > end_time:
                continue
            title = entry['title']
            description = self.remove_html_tags(entry['summary'])
            article_url = entry['link']
            image_url = self.get_image_url(entry)
            article = Article(self.company, title, description, published_time,
                              article_url, image_url)
            articles.append(article)
        return articles

    @staticmethod
    def remove_html_tags(text: str) -> str:
        while '<' in text and '>' in text:
            text = text[:text.find('<')] + text[text.find('>') + 1:]
        return text

    @staticmethod
    def get_image_url(entry: dict) -> str:
        if 'media_content' not in entry:
            return ''

        media_content = entry['media_content']
        image_sizes = dict()
        for media in media_content:
            content_type = None
            if 'medium' in media:
                content_type = media['medium']
            elif 'type' in media:
                content_type = media['type'][:5]

            if content_type == 'image':
                image_size = 0
                if 'width' in media:
                    image_size = int(media['width'])
                elif 'isdefault' in media and media['isdefault'] == 'true':
                    image_size = float('inf')
                image_sizes[media['url']] = image_size
        return max(image_sizes, key=image_sizes.get)