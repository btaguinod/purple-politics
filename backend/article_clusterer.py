import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import math

from article import Article
from event import Event

nltk.download('stopwords')
nltk.download('punkt')


class NLPArticle:
    """Article Container with vector for similarity comparisons.

    Attributes:
        article (Article): Article object.
        vector (numpy.ndarray): Numpy vector representation.
    """

    def __init__(self, article: Article):
        self.article = article
        self.vector = None

    def set_tf_vector(self, index: list[str]) -> list[str]:
        """Calculate and store term frequency vector.

        Args:
            index (list[str]): Word index.

        Returns:
            list[str]: Updated word index.
        """

        new_index = index.copy()
        tokens = self.preprocess_text()
        unique_words = set(tokens)

        text_freq_dict = {word: 0 for word in unique_words}
        for word in tokens:
            text_freq_dict[word] += 1

        if new_index is None:
            new_index = list(unique_words)
        else:
            addition = [word for word in unique_words if word not in new_index]
            new_index += addition

        tf = []
        for word in new_index:
            tf.append(text_freq_dict[word] if word in unique_words else 0)

        self.vector = np.array(tf) / len(tokens)
        return new_index

    def pad_tf_vector(self, new_len: int):
        """Pad the term frequency vector with zeros.

        Args:
            new_len (int): Length vector will be extended to.
        """

        self.vector = np.pad(self.vector, (0, new_len))

    def preprocess_text(self) -> list[str]:
        """Turn text into tokens without stopwords and punctuation.

        Returns:
            list[str]: List of tokens.
        """

        text = self.article.title + ' ' + self.article.description
        text = text.translate(str.maketrans('', '', string.punctuation))
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(text)
        filtered_tokens = []
        for token in tokens:
            if token.lower not in stop_words:
                filtered_tokens.append(token)
        return filtered_tokens


class Cluster:
    """Cluster of NLPArticle objects.

    Attributes:
        nlp_articles (list[NLPArticle]): Stored NLPArticle objects
        self.vector (numpy.ndarray): Average of term frequency vectors in
            NLPArticle objects.
    """

    def __init__(self, nlp_articles: list[NLPArticle]):
        self.nlp_articles = nlp_articles
        self.vector = None

    def set_tf_vector(self, index: list[str]):
        """Calculate and store average term frequency vector.

        Args:
            index (list[str]): Word index.
        """

        new_index = index
        self.vector = np.zeros(len(new_index))
        for nlp_article in self.nlp_articles:
            self.vector += nlp_article.vector
        self.vector /= len(self.nlp_articles)

    def get_event(self) -> Event:
        """Gets event representation.

        Returns:
            Event: Event representation.
        """

        articles = []
        for nlp_article in self.nlp_articles:
            articles.append(nlp_article.article)
        return Event(articles)


class ClusterList:
    """List of Cluster objects.

    Attributes:
        threshold (float): Cosine similarity from 0 to 1 for clustering
            strictness.
        clusters (list[Cluster]): Stored Cluster objects.
        index (list[str]): Word index.
    """

    def __init__(self, threshold: float = 0.4, events: list[Event] = None):
        self.threshold = threshold
        self.clusters = []
        if events is not None:
            for event in events:
                nlp_articles = []
                for article in event.articles:
                    nlp_articles.append(NLPArticle(article))
                self.clusters.append(Cluster(nlp_articles))

        self.index = []
        for cluster in self.clusters:
            for nlp_article in cluster.nlp_articles:
                self.index = nlp_article.set_tf_vector(self.index)
            cluster.set_tf_vector(self.index)

    def add(self, articles: list[Article]):
        """Add Article objects to cluster.

        Args:
            articles (list[Article]): Article objects.
        """

        nlp_articles = [NLPArticle(article) for article in articles]
        for nlp_article in nlp_articles:
            self.index = nlp_article.set_tf_vector(self.index)
        self.pad_vectors(nlp_articles)
        for cluster in self.clusters:
            self.pad_vectors(cluster.nlp_articles)
        self.add_to_clusters(nlp_articles)

    def get_events(self) -> list[Event]:
        """Get Event representation.

        Returns:
            list[Event]: Event representation.
        """

        return [cluster.get_event() for cluster in self.clusters]

    def pad_vectors(self, nlp_articles: list[NLPArticle]):
        """Pad vectors to length of word index.

        Args:
            nlp_articles (list[NLPArticle]): NLPArticles to pad.
        """

        index_len = len(self.index)
        for nlp_article in nlp_articles:
            padding_len = index_len - len(nlp_article.vector)
            nlp_article.pad_tf_vector(padding_len)

    def get_inv_doc_freq(self, nlp_articles: list[NLPArticle]) -> np.ndarray:
        """Calculate inverse document frequency.

        Args:
            nlp_articles (list[NLPArticle]): Extra NLPArticles to use in
                calculations.
        """

        vector_len = len(self.index)

        doc_freq = np.zeros(vector_len)
        for nlp_article in nlp_articles:
            doc_freq += np.ceil(nlp_article.vector)
        for cluster in self.clusters:
            for nlp_article in cluster.nlp_articles:
                doc_freq += np.ceil(nlp_article.vector)

        doc_count = len(nlp_articles)
        for cluster in self.clusters:
            doc_count += len(cluster.nlp_articles)

        inv_doc_freq = np.zeros(vector_len)
        for i in range(len(doc_freq)):
            num = doc_freq[i]
            if num != 0:
                num = math.log((1 / num) * doc_count)
                inv_doc_freq[i] = num

        return inv_doc_freq

    def add_to_clusters(self, nlp_articles: list[NLPArticle]):
        """Add NLPArticle objects to stored clusters.

        Args:
           nlp_articles (list[NLPArticle]): NLPArticles to add.
        """
        inv_doc_freq = self.get_inv_doc_freq(nlp_articles)
        for nlp_article in nlp_articles:
            closest_dist = 0
            closest_cluster = None

            for cluster in self.clusters:
                new_dist = vector_similarity(
                    np.multiply(nlp_article.vector, inv_doc_freq),
                    np.multiply(cluster.vector, inv_doc_freq))
                if new_dist > self.threshold and new_dist > closest_dist:
                    closest_dist = new_dist
                    closest_cluster = cluster

            if closest_cluster is None:
                new_cluster = Cluster([nlp_article])
                self.clusters.append(new_cluster)
                new_cluster.set_tf_vector(self.index)
            else:
                closest_cluster.nlp_articles.append(nlp_article)
                closest_cluster.set_tf_vector(self.index)


def vector_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between vectors.

    Args:
       a (numpy.ndarray): First numpy vector.
       b (numpy.ndarray): Second numpy vector.

    Returns:
        float: Cosine similarity.
    """

    return (a @ b) / (np.linalg.norm(b) * np.linalg.norm(b))
