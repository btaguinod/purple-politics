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
        earliest_article = min(articles, key=lambda x: x['publishedTime'])
        latest_article = max(articles, key=lambda x: x['publishedTime'])
        events.append({
            'eventId': event['eventId'],
            'title': earliest_article['title'],
            'imageUrl': earliest_article['imageUrl'],
            'earliestTime': earliest_article['publishedTime'],
            'latestTime': latest_article['publishedTime'],
            'companies': list(companies)
        })
    return jsonify(events)


if __name__ == "__main__":
    app.run(debug=True)
