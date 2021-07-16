class TextInfo:
    """Information relating to text.
    Attributes:
        sentiment (float): Decimal from -1.0 to 1.0 describing sentiment of
            text.
        emotion (str): emotion of text.
    """

    def __init__(self, sentiment: float, emotion: str):
        self.sentiment = sentiment
        self.emotion = emotion
