from article_clusterer import Clusterer
from article_collector import ArticleCollector
from company import companies

import os

from database import Database

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
    print('\tFound', len(all_articles), 'total')
    print()

    print('Analyzing Sentiment:')
    text_analyzer = TextAnalyzer()
    for article in all_articles:
        article_text = article.title + ' ' + article.description
        article.text_info = text_analyzer.analyze_text(article_text)
    print()

    print('Clustering ' + str(len(all_articles)) + ' Articles:')
    clusters = Clusterer(0.3)
    clusters.add(all_articles)
    events = clusters.get_events()
    print('Created ' + str(len(events)) + ' clusters')

    print('Connecting to database:')
    database = Database()

    print('\tInserting Events')
    database.update_events(events)

    print('Done')
