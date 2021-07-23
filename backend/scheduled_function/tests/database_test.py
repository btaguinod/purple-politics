import unittest

from article import Article
from article_clusterer import Clusterer
from article_collector import ArticleCollector
from company import companies, Company
from database import Database
from event import Event
from text_info import TextInfo


class TestDatabase(unittest.TestCase):
    THRESHOLD = 0.3

    def test_get_events(self):
        print('Testing get events')

        database = Database('test', 'events')
        events = database.get_events()
        for event in events:
            self.assertIsInstance(event, Event)

    def test_add_events(self):
        print('Testing add events')

        database = Database('test', 'events')

        all_articles = []
        for item in companies:
            company = item['company']
            url = item['url']
            collector = ArticleCollector(company, url)
            articles = collector.get_articles(100)
            all_articles += articles

        for article in all_articles:
            article.text_info = TextInfo(0, 'Sadness')

        clusters = Clusterer(self.THRESHOLD)
        clusters.add(all_articles)

        database.update_events(clusters.get_events())
        events = database.get_events()

    def test_update_events(self):
        print('Testing update events')

        database = Database('test', 'events')

        events = database.get_events()
        for event in events:
            event.articles = [Article(Company('company', 0), 'title',
                                      'description', 'time', 'article',
                                      'image', TextInfo(0, 'Emotion'))]

        database.update_events(events)


if __name__ == '__main__':
    unittest.main()
