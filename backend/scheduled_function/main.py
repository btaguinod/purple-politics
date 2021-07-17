from article_clusterer import Clusterer
from article_collector import ArticleCollector
from company import companies

from config import DB_CREDENTIALS

from pymongo import MongoClient

from text_analyzer import TextAnalyzer

if __name__ == "__main__":
    print('Retrieving Articles:')
    all_articles = []
    for item in companies:
        company = item['company']
        url = item['url']
        print('Retrieving ' + str(company) + ':')
        collector = ArticleCollector(company, url)
        articles = collector.get_articles(100)
        print('\tFound', len(articles))
        all_articles += articles
    print()

    print('Analyzing Sentiment:')
    for article in all_articles:
        article_text = article.title + ' ' + article.description
        article.text_info = TextAnalyzer.analyze_text(article_text)
    print()

    print('Clustering ' + str(len(all_articles)) + ' Articles:')
    clusters = Clusterer(0.3)
    clusters.add(all_articles)
    events = clusters.get_events()
    print('Created ' + str(len(events)) + ' clusters')

    print('Connecting to database:')
    mongo_client = MongoClient(DB_CREDENTIALS)
    db = mongo_client.get_database('purplePolitics')
    collection = db.get_collection('events')
    print('\tInserting Events')
    all_events = []
    for event in events:
        article_dicts = []
        for article in event.articles:
            article_dicts.append({
                'title': article.title,
                'description': article.description,
                'publishedTime': article.published_time,
                'articleUrl': article.article_url,
                'imageUrl': article.image_url,
                'textInfo': {
                    'sentiment': article.text_info.sentiment,
                    'emotion': article.text_info.emotion
                },
                'company': {
                    'name': article.company.name,
                    'bias': article.company.bias
                }
            })
        event_dict = {
            'eventId': str(event.event_id),
            'title': event.title,
            'articles': article_dicts
        }
        all_events.append(event_dict)
    collection.insert_many(all_events)
    print('Done')
