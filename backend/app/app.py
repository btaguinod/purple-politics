from flask import Flask, jsonify
from pymongo import MongoClient
from scheduled_function.config import DB_CREDENTIALS

app = Flask(__name__)


mongoClient = MongoClient(DB_CREDENTIALS)
db = mongoClient.get_database('purplePolitics')
collection = db.get_collection('events')

@app.route('/articles/<id>/')
def addname(id):
    event = collection.find_one({"event_id": id})
    event['_id'] = str(event['_id'])
    print('YO', event)
    return jsonify(event)

@app.route('/events/')
def getnames():
    events = [event for event in collection.find({})]
    for event in events:
        event['_id'] = str(event['_id'])
    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True)