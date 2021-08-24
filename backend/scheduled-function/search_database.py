import os
from algoliasearch.search_client import SearchClient
try:
    from config import ALGOLIA_ID, ALGOLIA_API_KEY
except ImportError:
    ALGOLIA_ID = os.environ['ALGOLIA_ID']
    ALGOLIA_API_KEY = os.environ['ALGOLIA_API_KEY']
from event import Event


class SearchDatabase:
    """A database connector that stores data for the cloud search engine.

    Attributes:
        index (SearchIndex): Connection to database table.
    """

    def __init__(self):
        client = SearchClient.create(ALGOLIA_ID, ALGOLIA_API_KEY)
        self.index = client.init_index('purple_politics')

    def update(self, events: list[Event]):
        """Update search database with events.

        Args:
            events (list[Event]): Events to insert into database.
        """

        eventDicts = []
        for event in events:
            articles = event.articles
            unique_companies = set(
                [article.company.name for article in articles])
            sorted_articles = sorted(articles,
                                     key=lambda x: x.published_time)
            earliest_article = sorted_articles[0]
            latest_article = sorted_articles[-1]
            image_url = ""
            for article in sorted_articles:
                if article.image_url != "":
                    image_url = article.image_url
                    break

            articleDicts = []
            for article in event.articles:
                articleDicts.append({
                    'title': article.title
                })

            eventDicts.append({
                'objectID': event.event_id,
                'articles': articleDicts,
                'companyCount': len(unique_companies),

                'title': earliest_article.title,
                'imageUrl': image_url,
                'earliestTime': earliest_article.published_time,
                'latestTime': latest_article.published_time,
                'companies': list(unique_companies)
            })

        request_options = {'autoGenerateObjectIDIfNotExist': False}
        self.index.save_objects(eventDicts, request_options)

    def clear(self):
        """Delete all events in the search database."""

        self.index.clear_objects()


