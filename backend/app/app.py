from flask import Flask, jsonify
from pymongo import MongoClient

import os
try:
    from config import DB_CREDENTIALS
except ImportError:
    DB_CREDENTIALS = os.environ['DB_CREDENTIALS']

app = Flask(__name__)


mongoClient = MongoClient(DB_CREDENTIALS)
db = mongoClient.get_database('purplePolitics')
collection = db.get_collection('events')


@app.route('/articles/<id>/')
def get_articles(id):
    event = collection.find_one({"event_id": id})
    event['_id'] = str(event['_id'])
    print('YO', event)
    return jsonify(event)


@app.route('/events/')
def get_events():
    events = [event for event in collection.find({})]
    for event in events:
        event['_id'] = str(event['_id'])
    return jsonify(events)


if __name__ == "__main__":
    app.run(debug=True)