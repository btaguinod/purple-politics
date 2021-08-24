from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
from flask_restful import Resource, Api, abort
from utils.get_param import get_int_param, get_bool_param, get_string_param
from algoliasearch.search_client import SearchClient

import os
try:
    from config import DB_CREDENTIALS, ALGOLIA_ID, ALGOLIA_API_KEY
    origins = ['http://localhost:3000']
except ImportError:
    DB_CREDENTIALS = os.environ['DB_CREDENTIALS']
    ALGOLIA_ID = os.environ['ALGOLIA_ID']
    ALGOLIA_API_KEY = os.environ['ALGOLIA_API_KEY']
    origins = ['https://purplepolitics.netlify.app',
               'https://purplepoliticsevents.com']

app = Flask(__name__)

CORS(app, origins=origins)
api = Api(app)

mongo_client = MongoClient(DB_CREDENTIALS)
db = mongo_client.get_database('purplePolitics')
collection = db.get_collection('events')

search_client = SearchClient.create(ALGOLIA_ID, ALGOLIA_API_KEY)
search_index = search_client.init_index('purple_politics')

class Articles(Resource):
    DEFAULT_PARAMS = {
        'sort': 'time',
        'ascending': False,
        'max': 30,
        'page': 1
    }

    def get(self, event_id):
        defaults = self.DEFAULT_PARAMS

        sort = get_string_param('sort', defaults['sort'], ['time', 'bias'])
        ascending = get_bool_param('ascending', defaults['ascending'])
        max_results = get_int_param('max', defaults['max'])
        page = get_int_param('page', defaults['page'])

        event = collection.find_one({"eventId": event_id})
        articles = event['articles']

        if sort == 'time':
            def key(article): return article['publishedTime']
        else:
            def key(article): return article['company']['bias']

        articles = sorted(articles, key=key, reverse=(not ascending))
        return {
            'count': len(articles),
            'articles': articles[max_results * (page - 1):max_results * page]
        }


class Events(Resource):
    DEFAULT_PARAMS = {
        'query': None,
        'sort': 'latestTime',
        'ascending': False,
        'removeNoImg': False,
        'max': 30,
        'page': 1
    }

    SORT_TYPES = ['relevance', 'latestTime', 'uniqueCompanies']

    def get(self):
        defaults = self.DEFAULT_PARAMS

        query = get_string_param('query', defaults['query'])
        sort = get_string_param('sort', defaults['sort'], self.SORT_TYPES)
        if sort == 'relevance' and query is None:
            abort(400, message='Can\'t sort by relevance with no query')
        ascending = get_bool_param('ascending', defaults['ascending'])
        remove_no_img = get_bool_param('removeNoImg',
                                        defaults['removeNoImg'])
        max_results = get_int_param('max', defaults['max'])
        page = get_int_param('page', defaults['page'])

        if query is None:
            events = self.get_database_events()
        else:
            events = self.get_search_events(query)
        events = self.sort_events(events, sort, ascending)

        if remove_no_img:
            def has_img(event): return event['imageUrl'] != ""
            events = list(filter(has_img, events))

        return {
            'count': len(events),
            'events': events[max_results * (page - 1):max_results * page]
        }

    def get_database_events(self):
        events = []
        for event in collection.find():
            articles = event['articles']
            companies = set(
                [article['company']['name'] for article in articles])
            sorted_articles = sorted(articles,
                                     key=lambda x: x['publishedTime'])
            earliest_article = sorted_articles[0]
            latest_article = sorted_articles[-1]
            image_url = ""
            for article in sorted_articles:
                article_image_url = article['imageUrl']
                if article_image_url != "":
                    image_url = article_image_url
                    break

            events.append({
                'eventId': event['eventId'],
                'title': earliest_article['title'],
                'imageUrl': image_url,
                'earliestTime': earliest_article['publishedTime'],
                'latestTime': latest_article['publishedTime'],
                'companies': list(companies)
            })
        return events

    def get_search_events(self, query):
        events = search_index.search(query, {'hitsPerPage': 1000})['hits']

        for event in events:
            event['eventId'] = event.pop('objectID')
            event.pop('articles')
            event.pop('companyCount')
            event.pop('_highlightResult')
        return events

    def sort_events(self, events, sort, ascending):
        if sort == 'uniqueCompanies':
            def key(event): return len(event['companies'])
        elif sort == 'latestTime':
            def key(event): return event['latestTime']
        else:
            return events
        return sorted(events, key=key, reverse=(not ascending))


class HomeEvents(Events):
    DEFAULT_PARAMS = {
        'cardsSort': 'latestTime',
        'cardsAscending': False,
        'cardsRemoveNoImg': True,
        'cardsMax': 30,

        'headlinesSort': 'latestTime',
        'headlinesAscending': False,
        'headlinesRemoveNoImg': False,
        'headlinesMax': 7
    }

    def get(self):
        defaults = self.DEFAULT_PARAMS

        cards_sort = get_string_param('cardsSort', defaults['cardsSort'],
                                      self.SORT_TYPES)
        cards_ascending = get_bool_param('cardsAscending',
                                         defaults['cardsAscending'])
        cards_max_results = get_int_param('cardsMax', defaults['cardsMax'])
        cards_remove_no_img = get_bool_param('cardsRemoveNoImg',
                                              defaults['cardsRemoveNoImg'])
        headlines_sort = get_string_param('headlinesSort',
                                          defaults['headlinesSort'],
                                          self.SORT_TYPES)
        headlines_ascending = get_bool_param('headlinesAscending',
                                             defaults['headlinesAscending'])
        headlines_remove_no_img = get_bool_param('headlinesRemoveNoImg',
                                                  defaults[
                                                      'headlinesRemoveNoImg'])
        headlines_max_results = get_int_param('headlinesMax',
                                              defaults['headlinesMax'])

        events = self.get_database_events()

        card_events = filter(lambda x: len(x['companies']) >= 4, events)
        card_events = self.sort_events(card_events, cards_sort, cards_ascending)
        headline_events = self.sort_events(events, headlines_sort,
                                           headlines_ascending)

        def has_img(event): return event['imageUrl'] != ""
        if cards_remove_no_img:
            card_events = list(filter(has_img, card_events))
        if headlines_remove_no_img:
            headline_events = list(filter(has_img, headline_events))

        return {
            'cardEvents': card_events[:cards_max_results],
            'headlineEvents': headline_events[:headlines_max_results]
        }


class Base(Resource):
    def get(self):
        return 'Welcome! supported endpoints are /articles/<event_id>, ' \
               '/events, and /home-events'


api.add_resource(Articles, '/articles/<event_id>')
api.add_resource(Events, '/events')
api.add_resource(HomeEvents, '/home-events')
api.add_resource(Base, '/')

if __name__ == "__main__":
    app.run(debug=True)