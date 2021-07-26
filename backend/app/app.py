from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
from flask_restful import Resource, Api, request

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
    def get(self, event_id):
        event = collection.find_one({"eventId": event_id})
        return event['articles']


class Events(Resource):
    def get(self):

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


api.add_resource(Articles, '/articles/<event_id>')
api.add_resource(Events, '/events')


if __name__ == "__main__":
    app.run(debug=True)
