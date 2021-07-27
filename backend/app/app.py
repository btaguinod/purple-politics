from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
from flask_restful import Resource, Api, request, abort

import os
try:
    from config import DB_CREDENTIALS
    origins = ['http://localhost:3000']
except ImportError:
    DB_CREDENTIALS = os.environ['DB_CREDENTIALS']
    origins = ['https://purplepolitics.netlify.app']

app = Flask(__name__)

CORS(app, origins=origins)
api = Api(app)

mongoClient = MongoClient(DB_CREDENTIALS)
db = mongoClient.get_database('purplePolitics')
collection = db.get_collection('events')


def get_param(param_name, default, is_acceptable, to_value):
    param_string = request.args.get(param_name)
    if param_string is None:
        param_string = default
    elif not is_acceptable(param_string):
        abort(400, message=f'"{param_string}" is not a valid {param_name} '
                           f'value')
    return to_value(param_string)


class Articles(Resource):
    DEFAULTS = {
        'sort': 'time',
        'ascending': 'false',
        'max': '10',
        'page': '1'
    }

    def get(self, event_id):
        sort = get_param('sort', 'time',
                         ['time', 'bias'].__contains__,
                         lambda x: x)
        ascending = get_param('ascending', 'false',
                              ['true', 'false'].__contains__,
                              lambda x: x == 'true')
        max_results = get_param('max', self.DEFAULTS['max'], str.isdigit, int)
        page = get_param('page', self.DEFAULTS['page'], str.isdigit, int)

        event = collection.find_one({"eventId": event_id})
        articles = event['articles']

        if sort == 'time':
            def key(article): return article['publishedTime']
        else:
            def key(article): return article['company']['bias']

        articles = sorted(articles, key=key, reverse=(not ascending))
        return {
            'count': len(articles),
            'articles': articles[:max_results * page]
        }


class Events(Resource):
    DEFAULTS = {
        'sort': 'latestTime',
        'ascending': 'false',
        'max': '10',
        'page': '1'
    }

    SORT_TYPES = ['latestTime', 'uniqueCompanies']

    def get(self):
        sort = get_param('sort', self.DEFAULTS['sort'],
                         self.SORT_TYPES.__contains__,
                         lambda x: x)
        ascending = get_param('ascending', self.DEFAULTS['ascending'],
                              ['true', 'false'].__contains__,
                              lambda x: x == 'true')
        max_results = get_param('max', self.DEFAULTS['max'], str.isdigit, int)
        page = get_param('page', self.DEFAULTS['page'], str.isdigit, int)

        events = self.get_database_events()
        events = self.sort_events(events, sort, ascending)
        return {
            'count': len(events),
            'events': events[:max_results * page]
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

    def sort_events(self, events, sort, ascending):
        if sort == 'uniqueCompanies':
            def key(event): return len(event['companies'])
        else:
            def key(event): return event[sort]

        return sorted(events, key=key, reverse=(not ascending))

class HomeEvents(Events):
    DEFAULTS = {
        'cardsSort': 'uniqueCompanies',
        'cardsAscending': 'false',
        'cardsMax': '30',
        'headlinesSort': 'latestTime',
        'headlinesAscending': 'false',
        'headlinesMax': '7'
    }
    def get(self):
        cards_sort = get_param('cardsSort', self.DEFAULTS['cardsSort'],
                               self.SORT_TYPES.__contains__,
                               lambda x: x)
        cards_ascending = get_param('cardsAscending',
                                    self.DEFAULTS['cardsAscending'],
                                    ['true', 'false'].__contains__,
                                    lambda x: x == 'true')
        cards_max_results = get_param('cardsMax', self.DEFAULTS['cardsMax'],
                                      str.isdigit, int)
        headlines_sort = get_param('headlinesSort',
                                   self.DEFAULTS['headlinesSort'],
                                   self.SORT_TYPES.__contains__,
                                   lambda x: x)
        headlines_ascending = get_param('headlinesAscending',
                                        self.DEFAULTS['headlinesAscending'],
                                        ['true', 'false'].__contains__,
                                        lambda x: x == 'true')
        headlines_max_results = get_param('headlinesMax',
                                          self.DEFAULTS['headlinesMax'],
                                          str.isdigit, int)

        events = self.get_database_events()

        card_events = self.sort_events(events, cards_sort, cards_ascending)
        headline_events = self.sort_events(events, headlines_sort,
                                           headlines_ascending)

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
