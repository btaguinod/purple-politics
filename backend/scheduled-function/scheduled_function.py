from article_collector import ArticleCollector
from company import companies
from text_analyzer import TextAnalyzer
from article_clusterer import Clusterer
from database import Database


class ScheduledFunction:
    """Function that collects, analyzes, clusters, and stores news articles.

    Attributes:
        article_collectors (list[ArticleCollector]): News article collectors.
        text_analyzer (TextAnalyzer): News text analyzer.
        database (Database): Event database.
        clusterer (Clusterer): Clusters Article objects into Event objects.
    """

    COLLECTOR_MAX = 100
    CLUSTERER_THRESHOLD = 0.3
    DATABASE_NAME = 'purplePolitics'
    COLLECTION_NAME = 'events'

    def __init__(self):
        self.article_collectors = []
        for company_dict in companies:
            company = company_dict['company']
            url = company_dict['url']
            self.article_collectors.append(ArticleCollector(company, url))
        self.text_analyzer = TextAnalyzer()
        self.clusterer = Clusterer(self.CLUSTERER_THRESHOLD)
        self.database = Database(self.DATABASE_NAME, self.COLLECTION_NAME)

    def main(self):
        """Collects, analyzes, clusters, and stores news articles."""

        print('Retrieving events from database:')
        events = self.database.get_events()
        print(f'\tFound {len(events)} events\n')

        old_articles = []
        for event in events:
            for article in event.articles:
                old_articles.append(article)

        print('Retrieving articles from RSS feeds:')
        new_articles = []
        for article_collector in self.article_collectors:
            articles = article_collector.get_articles(self.COLLECTOR_MAX)
            new_articles += articles
            print(f'\tFound {len(articles)} articles from '
                  f'{article_collector.company}')
        print(f'Found {len(new_articles)} new articles total\n')

        print('Removing repeat articles:')
        for article in new_articles:
            if article in old_articles:
                new_articles.remove(article)
        print(f'{len(new_articles)} articles remaining\n')

        print('Analyzing article text:')
        for article in new_articles:
            article_text = article.title + ' ' + article.description
            article.text_info = self.text_analyzer.analyze_text(article_text)
        print(f'Used {self.text_analyzer.units} units\n')

        print(f'Adding articles to {len(events)} clusters:')
        self.clusterer.add_events(events)
        self.clusterer.add_articles(new_articles)
        new_events = self.clusterer.get_events()
        print(f'Completed clustering with {len(new_events)} clusters:\n')

        print('Adding events to database')
        self.database.update_events(self.clusterer.get_events())
        print('Done\n')


if __name__ == "__main__":
    function = ScheduledFunction()
    function.main()
