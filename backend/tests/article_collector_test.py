import unittest

from article import Article
from article_collector import ArticleCollector

from company import companies


class MyTestCase(unittest.TestCase):
    MAX_ARTICLES = 100

    OUTPUT_MAX = 5

    def test_article_collector(self):
        print('Testing article collector...')

        for item in companies:
            company = item['company']
            url = item['url']
            print('Testing ' + str(company) + ':')
            collector = ArticleCollector(company, url)
            articles = collector.get_articles(100)
            self.assertIsInstance(articles, list)
            for article in articles:
                self.assertIsInstance(article, Article)
            print('\tFound ' + str(len(articles)) + ' articles')
            print('\tFirst ' + str(len(articles[:10])) + ':')

            for article in articles[:10]:
                print('\t\t' + str(article))


if __name__ == '__main__':
    unittest.main()
