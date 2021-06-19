import unittest

from article import Article
from article_collector import ArticleCollector


class MyTestCase(unittest.TestCase):
    URLS = {
        'CNN': 'http://rss.cnn.com/rss/cnn_allpolitics.rss',
        'Fox News': 'http://feeds.foxnews.com/foxnews/politics',
        'LA Times': 'https://www.latimes.com/politics/rss2.0.xml#nt=1col-7030col1'
    }
    MAX_ARTICLES = 100

    OUTPUT_MAX = 5

    def test_something(self):
        print('Testing article collector...')

        for company, url in self.URLS.items():
            print('Testing ' + company + ':')
            collector = ArticleCollector(company, url)
            articles = collector.get_articles(100)
            self.assertIsInstance(articles, list)
            for article in articles:
                self.assertIsInstance(article, Article)
            print('\tFound ' + str(len(articles)) + ' articles')

            for article in articles:
                print('\t\t' + str(article))


if __name__ == '__main__':
    unittest.main()
