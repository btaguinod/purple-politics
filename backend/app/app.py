from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from datetime import datetime

import os
try:
    from config import DB_CREDENTIALS
    origins = ['http://localhost:3000']
except ImportError:
    DB_CREDENTIALS = os.environ['DB_CREDENTIALS']
    origins = ['https://purplepolitics.netlify.app']

app = Flask(__name__)

CORS(app)

mongoClient = MongoClient(DB_CREDENTIALS)
db = mongoClient.get_database('purplePolitics')
collection = db.get_collection('events')


@app.route('/articles/<event_id>')
def get_articles(event_id):
    event = collection.find_one({"eventId": event_id})
    return jsonify(event['articles'])


@app.route('/events')
def get_events():
    events = []
    for event in collection.find():
        articles = event['articles']
        companies = set([article['company']['name'] for article in articles])
        sorted_articles = sorted(articles, key=lambda x: x['publishedTime'])
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
    return jsonify(events)


if __name__ == "__main__":
    app.run(debug=True)
