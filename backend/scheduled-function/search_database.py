from algoliasearch.search_client import SearchClient
from config import ALGOLIA_ID, ALGOLIA_API_KEY
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
            articleDicts = []
            unique_companies = set()
            for article in event.articles:
                articleDicts.append({
                    'title': article.title,
                    'description': article.description,
                    'image': article.image_url
                })
                unique_companies.add(article.company)
            eventDicts.append({
                'objectID': event.event_id,
                'articles': articleDicts,
                'companyCount': len(unique_companies)
            })

        request_options = {'autoGenerateObjectIDIfNotExist': False}
        self.index.save_objects(eventDicts, request_options)
