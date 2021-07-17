import unittest

from scheduled_function.article import Article
from scheduled_function.article_clusterer import Clusterer
from scheduled_function.article_collector import ArticleCollector
from scheduled_function.company import companies
from scheduled_function.event import Event


class ClustererTest(unittest.TestCase):
    THRESHOLD = 0.3

    def test_add(self):
        print('Testing add function:')

        all_articles = []
        for item in companies:
            company = item['company']
            url = item['url']
            print('Retrieving ' + str(company) + ':')
            collector = ArticleCollector(company, url)
            articles = collector.get_articles(100)
            print('\t', 'Found', len(articles))
            all_articles += articles
        print('Clustering ' + str(len(all_articles)) + ' Articles:')

        clusters = Clusterer(self.THRESHOLD)
        clusters.add(all_articles)

        for i, event in enumerate(clusters.get_events()):
            if len(event.articles) < 3:
                continue
            self.assertIsInstance(event, Event)
            print('Event ', i + 1)
            for article in event.articles:
                self.assertIsInstance(article, Article)
                print('\t', article.company.name, ': ', article.title, article.article_url)
        print()


if __name__ == '__main__':
    unittest.main()