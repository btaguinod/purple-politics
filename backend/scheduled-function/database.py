import os

from article import Article
from company import Company
from event import Event
from text_info import TextInfo

try:
    from config import DB_CREDENTIALS
except ImportError:
    DB_CREDENTIALS = os.environ['DB_CREDENTIALS']

from pymongo import MongoClient


class Database:
    """Cloud database connector for storing Event objects.

    Attributes:
        collection (Collection): Collection of Event object info.
    """

    def __init__(self, database_name: str = 'purplePolitics',
                 collection_name: str = 'events'):
        mongo_client = MongoClient(DB_CREDENTIALS)
        db = mongo_client.get_database(database_name)
        self.collection = db.get_collection(collection_name)

    def get_events(self, only_active: bool = True) -> list[Event]:
        """Retrieves Event objects from database.

        Returns:
            list[Event]: Event objects from database.
        """
        filter_args = {'active': True} if only_active else {}
        results = self.collection.find(filter_args)
        events = []
        for result in results:
            articles = []
            for article in result['articles']:
                company = article['company']
                text_info = article['textInfo']
                articles.append(Article(
                    Company(company['name'], company['bias']),
                    article['title'],
                    article['description'],
                    article['publishedTime'],
                    article['articleUrl'],
                    article['imageUrl'],
                    TextInfo(text_info['sentiment'], text_info['emotion'])
                ))
            events.append(Event(
                articles,
                result['eventId']
            ))
        return events

    def update_events(self, events: list[Event]):
        """Stores and updates Event objects from database.

        Attributes:
            events (list[Event]): Event objects.
        """

        for event in events:
            article_dicts = []
            for article in event.articles:
                article_dicts.append({
                    'title': article.title,
                    'description': article.description,
                    'publishedTime': article.published_time,
                    'articleUrl': article.article_url,
                    'imageUrl': article.image_url,
                    'textInfo': {
                        'sentiment': article.text_info.sentiment,
                        'emotion': article.text_info.emotion
                    },
                    'company': {
                        'name': article.company.name,
                        'bias': article.company.bias
                    }
                })
            search_query = {'eventId': event.event_id}
            update_query = {
                '$set': {'articles': article_dicts, 'active': event.active}
            }
            self.collection.update_one(search_query, update_query, True)
