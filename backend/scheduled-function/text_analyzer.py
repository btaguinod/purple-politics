from article import Article
from text_info import TextInfo
import os

try:
    from config import IBM_API_KEY
    from config import IBM_URL
except ImportError:
    IBM_API_KEY = os.environ['IBM_API_KEY']
    IBM_URL = os.environ['IBM_URL']

import requests
from requests.exceptions import HTTPError


class TextAnalyzer:
    """Analyzes emotion and sentiment from text.

    Attributes:
        units (int): Usage units from IBM api.
    """

    EXTRA_ATTEMPTS = 2

    def __init__(self):
        self.units = 0

    def analyze_text(self, text: str) -> TextInfo:
        """Gets emotion and sentiment from text.

        Args:
            text (str): Text to analyze.

        Returns:
            TextInfo: Information about texts.
        """
        try:
            response = requests.get(
                IBM_URL,
                params={
                    'version': '2021-03-25',
                    'text': text,
                    'features': 'sentiment,emotion'
                },
                headers={'Content-Type': 'application/json'},
                auth=('apikey', IBM_API_KEY)
            )
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            response_dict = response.json()
            sentiment = response_dict['sentiment']['document']['score']
            emotions = response_dict['emotion']['document']['emotion']
            emotion = max(emotions, key=emotions.get)

            usage = response_dict['usage']
            self.units += usage['text_units'] * usage['features']

            return TextInfo(sentiment, emotion)

    def analyze_url(self, url: str) -> TextInfo:
        """Gets emotion and sentiment from text in url.

        Args:
            url (str): Url containing text to analyze.

        Returns:
            TextInfo: Information about texts.
        """
        def send_request():
            return requests.get(
                IBM_URL,
                params={
                    'version': '2021-03-25',
                    'url': url,
                    'features': 'sentiment,emotion'
                },
                headers={'Content-Type': 'application/json'},
                auth=('apikey', IBM_API_KEY)
            )
        try:
            response = send_request()
            if response.status_code == 400:
                for _ in range(self.EXTRA_ATTEMPTS):
                    send_request()
                    if response.status_code == 200:
                        break
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err} with {url}')
            raise http_err
        except Exception as err:
            print(f'Other error occurred: {err} with {url}')
            raise err
        else:
            response_dict = response.json()
            sentiment = response_dict['sentiment']['document']['score']
            emotions = response_dict['emotion']['document']['emotion']
            emotion = max(emotions, key=emotions.get)

            usage = response_dict['usage']
            self.units += usage['text_units'] * usage['features']

            return TextInfo(sentiment, emotion)

