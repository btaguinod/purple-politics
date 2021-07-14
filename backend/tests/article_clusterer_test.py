import json
import unittest

from article import Article
from article_clusterer import ClusterList
from article_collector import ArticleCollector
from company import companies, Company
from event import Event


class ArticleClustererTest(unittest.TestCase):
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

        # # For testing locally.
        # with open('../download_articles/data.json', 'r', encoding='utf-8') \
        #         as f:
        #     articles = json.loads(f.read())
        # for article in articles:
        #     all_articles.append(Article(
        #         Company(article['company'], 0),
        #         article['title'],
        #         article['description'],
        #         article['published_time'],
        #         article['article_url'],
        #         article['image_url']
        #     ))

        clusters = ClusterList(self.THRESHOLD)
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
