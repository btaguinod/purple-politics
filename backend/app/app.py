from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS

import os
try:
    from config import DB_CREDENTIALS
    origins = ['http://localhost:3000']
except ImportError:
    DB_CREDENTIALS = os.environ['DB_CREDENTIALS']
    origins = ['https://purplepolitics.netlify.app']

app = Flask(__name__)

CORS(app, origins=origins)

mongoClient = MongoClient(DB_CREDENTIALS)
db = mongoClient.get_database('purplePolitics')
collection = db.get_collection('events')


@app.route('/articles/<event_id>/')
def get_articles(event_id):
    event = collection.find_one({"eventId": event_id})
    event['_id'] = str(event['_id'])
    return jsonify(event)


@app.route('/events/')
def get_events():
    events = [event for event in collection.find({})]
    for event in events:
        event['_id'] = str(event['_id'])
    return jsonify(events)


if __name__ == "__main__":
    app.run(debug=True)