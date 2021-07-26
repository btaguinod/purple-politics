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


class Articles(Resource):
    sort_types = ['time', 'bias']

    def get(self, event_id):
        sort = request.args.get('sort')
        if sort is None:
            sort = 'time'
        if sort not in self.sort_types:
            abort(400, message=f'{sort} is not a valid sort attribute.')

        ascending = request.args.get('ascending')
        if ascending is None or ascending.lower():
            ascending = False
        elif ascending.lower() == 'true':
            ascending = True
        else:
            abort(400, message='ascending needs to be "True" or "False".')

        max_results = request.args.get('max')
        if max_results is None:
            max_results = 25
        elif max_results.isdigit():
            max_results = int(max_results)
        else:
            abort(400, message='max needs to be an integer.')

        event = collection.find_one({"eventId": event_id})
        articles = event['articles']

        if sort == 'time':
            def key(article): return article['publishedTime']
        else:
            def key(article): return article['company']['bias']

        articles = sorted(articles, key=key, reverse=(not ascending))
        return articles[:max_results]


class Events(Resource):
    sort_types = ['latestTime', 'mostCompanies']

    def get(self):
        sort = request.args.get('sort')
        if sort is None:
            sort = 'latestTime'
        if sort not in self.sort_types:
            abort(400, message=f'{sort} is not a valid sort attribute.')

        ascending = request.args.get('ascending')
        if ascending is None or ascending.lower():
            ascending = False
        elif ascending.lower() == 'true':
            ascending = True
        else:
            abort(400, message='ascending needs to be "True" or "False".')

        max_results = request.args.get('max')
        if max_results is None:
            max_results = 25
        elif max_results.isdigit():
            max_results = int(max_results)
        else:
            abort(400, message='max needs to be an integer.')

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

        if sort == 'mostCompanies':
            def key(event): return len(event['companies'])
        else:
            def key(event): return event[sort]

        events = sorted(events, key=key, reverse=(not ascending))
        return events[:max_results]


api.add_resource(Articles, '/articles/<event_id>')
api.add_resource(Events, '/events')


if __name__ == "__main__":
    app.run(debug=True)
