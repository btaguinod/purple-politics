class Company:
    """Representation of online news article.

        Attributes:
            name (str): Name.
            bias (float): Political bias from -1 to 1 where left is negative
            and right is positive.
        """

    def __init__(self, name, bias):
        self.name = name
        self.bias = bias

    def __str__(self):
        return self.name


companies = [
    {
        'company': Company('CNN', -1),
        'url': 'http://rss.cnn.com/rss/cnn_allpolitics.rss'
    },
    {
        'company': Company('HuffPost', -1),
        'url': 'https://chaski.huffpost.com/us/auto/vertical/politics'
    },
    {
        'company': Company('LA Times', -0.5),
        'url': 'https://www.latimes.com/politics/rss2.0.xml#nt=1col-7030col1'
    },
    {
        'company': Company('CBS News', -0.5),
        'url': 'https://www.cbsnews.com/latest/rss/politics'
    },
    {
        'company': Company('BBC News', 0),
        'url': 'http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml'
    },
    {
        'company': Company('Epoch Times', 0.5),
        'url': 'https://www.theepochtimes.com/c-us-politics/feed'
    },
    {
        'company': Company('National Review', 1),
        'url': 'https://www.nationalreview.com/politics-policy/feed/'
    },
    {
        'company': Company('Fox News', 1),
        'url': 'http://feeds.foxnews.com/foxnews/politics'
    },
    {
        'company': Company('Daily Mail', 1),
        'url': 'https://www.dailymail.co.uk/news/us-politics/index.rss'
    }
]
