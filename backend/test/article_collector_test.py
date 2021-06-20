import unittest

from article import Article
from article_collector import ArticleCollector


class MyTestCase(unittest.TestCase):
    URLS = {
        'CNN': 'http://rss.cnn.com/rss/cnn_allpolitics.rss',
        'HuffPost': 'https://chaski.huffpost.com/us/auto/vertical/politics',
        'LA Times': 'https://www.latimes.com/politics/rss2.0.xml#nt=1col'
                    '-7030col1',
        'CBS News': 'https://www.cbsnews.com/latest/rss/politics',
        'BBC News':  'http://feeds.bbci.co.uk/news/world/us_and_canada/rss'
                     '.xml',
        'Epoch Times': 'https://www.theepochtimes.com/c-us-politics/feed',
        'National Review': 'https://www.nationalreview.com/politics-policy'
                           '/feed/',
        'Fox News': 'http://feeds.foxnews.com/foxnews/politics',
        'Daily Mail': 'https://www.dailymail.co.uk/news/us-politics/index.rss'
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
            print('\tFirst ' + str(len(articles[:10])) + ':')

            for article in articles[:10]:
                print('\t\t' + str(article))


if __name__ == '__main__':
    unittest.main()
