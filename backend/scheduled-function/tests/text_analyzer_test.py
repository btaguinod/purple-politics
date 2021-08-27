import unittest

from text_analyzer import TextAnalyzer
from text_info import TextInfo

class TextAnalyzerTest(unittest.TestCase):
    TEST_TEXT = 'House select committee on Capitol insurrection will hold ' \
                'first hearing July 27 with Capitol Police. The House select ' \
                'committee investigating the US Capitol riot will hold its ' \
                'first hearing on July 27 to hear directly from law ' \
                'enforcement officers and others who responded to the ' \
                'attack, and potential witnesses have been asked for their ' \
                'availability and told to save the date. '

    def test_single_text(self):
        print('Testing text:')
        text_analyzer = TextAnalyzer()
        print('\t text: ' + self.TEST_TEXT)
        text_info = text_analyzer.analyze_text(self.TEST_TEXT)
        self.assertIsInstance(text_info, TextInfo)
        self.assertIsInstance(text_info.sentiment, float)
        print('\t sentiment: ' + str(text_info.sentiment))
        self.assertIsInstance(text_info.emotion, str)
        print('\t emotion: ' + str(text_info.emotion))
        print('\t units: ' + str(text_analyzer.units))

    TEST_URL = 'http://rss.cnn.com/~r/rss/cnn_allpolitics/~3/eP5tOTmFQrM/2Wv7mCr'

    def test_single_url(self):
        print('Testing url:')
        text_analyzer = TextAnalyzer()
        print('\t url: ' + self.TEST_URL)
        text_info = text_analyzer.analyze_url(self.TEST_URL)
        self.assertIsInstance(text_info, TextInfo)
        self.assertIsInstance(text_info.sentiment, float)
        print('\t sentiment: ' + str(text_info.sentiment))
        self.assertIsInstance(text_info.emotion, str)
        print('\t emotion: ' + str(text_info.emotion))
        print('\t units: ' + str(text_analyzer.units))


if __name__ == '__main__':
    unittest.main()
