from article import Article
from text_info import TextInfo

from config import IBM_API_KEY
from config import IBM_URL

import requests
from requests.exceptions import HTTPError


class TextAnalyzer:
    """Analyzes emotion and sentiment from text."""

    @staticmethod
    def analyze_text(text: str) -> TextInfo:
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
            return TextInfo(sentiment, emotion)









