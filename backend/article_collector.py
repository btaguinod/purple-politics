import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import string
import math

nltk.download('stopwords')
nltk.download('punkt')

with open('articles.json', 'r', encoding='utf-8') as f:
    articles = json.loads(f.read())


def preprocess_string(text: str) -> str:
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
    return filtered_tokens


def vectorize(processed_text:list, index:list[str]=[]) -> (np.ndarray, list):
    unique_words = set(processed_text)

    text_freq_dict = {word: 0 for word in unique_words}
    for word in processed_text:
        text_freq_dict[word] += 1

    if index == []:
        index = list(unique_words)
    else:
        index += [word for word in unique_words if word not in index]
    
    text_freq = []
    for word in index:
        text_freq.append(text_freq_dict[word] if word in unique_words else 0)
    vector = np.array(text_freq) / len(processed_text)
    return np.array(text_freq) / len(processed_text), index


def similarity(a:np.ndarray, b:np.ndarray) -> float:
    cos_similarity = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return cos_similarity


def add_to_cluster(new_article:dict, index:list, clusters:list=[], threshold:float=0.4) -> list:
    new_clusters = []

    for cluster in clusters:
        padding_len = len(index) - len(cluster['vector'])
        new_clusters.append({
            'vector': np.pad(cluster['vector'], (0, padding_len)),
            'articles': cluster['articles']
        })
        for article in cluster['articles']:
            article['vector'] = np.pad(article['vector'], (0, padding_len))
            
    document_freq = np.ceil(new_article['vector'])
    for cluster in new_clusters:
        for article in cluster['articles']:
            document_freq += np.ceil(article['vector'])

    inv_document_freq = np.zeros(len(document_freq))
    document_count = sum([sum([1 for article in cluster['articles']]) for cluster in new_clusters]) + 1
    for i in range(len(document_freq)):
        num = document_freq[i]
        if num != 0:
            num = math.log((1 / num) * document_count)
            inv_document_freq[i] = num

    closest_dist = 0
    closest_cluster = None

    for cluster in new_clusters:
        new_dist = similarity(np.multiply(new_article['vector'], inv_document_freq), np.multiply(cluster['vector'], inv_document_freq))
        if new_dist < threshold:
            continue
        if new_dist > closest_dist:
            closest_dist = new_dist
            closest_cluster = cluster
    
    if closest_cluster == None:
        new_clusters.append({
            'vector': new_article['vector'],
            'articles': [new_article]
        })
    else: 
        closest_cluster['articles'].append(new_article)
        closest_cluster['vector'] = sum([closest_article['vector'] for closest_article in closest_cluster['articles']]) / len(closest_cluster['articles'])
    return new_clusters
    

class NewsClusterer:
    def __init__(self, threshold:float=0.4, current_clusters:list=[], word_index:list=[]):
        self.clusters = current_clusters
        self.word_index = word_index
        self.threshold = threshold

    def add(self, new_articles:list[dict]) -> list:
        for article in new_articles:
            text = article['title'] + ' ' + article['description']
            processed = preprocess_string(text)
            article['vector'], self.word_index = vectorize(processed, self.word_index)
            self.clusters = add_to_cluster(article, self.word_index, self.clusters, self.threshold)
        return self.clusters


article_dicts = []
for article in articles:
    article_dicts.append({
        'company': article['company'],
        'title': article['title'],
        'description': article['description'],
        'vector': None
    })
    
    
clusterer = NewsClusterer(0.2)
clusters = clusterer.add(article_dicts)


for i, cluster in enumerate(sorted(clusters, reverse=True, key=lambda x: len(x['articles']))):
    if len(cluster['articles']) == 1:
        continue
    print('Cluster ', i + 1, ': ')
    for article in cluster['articles']:
        print('\t', article['company'] if 'company' in article else '?', ': ',  article['title'])


def create_cluster(articles:list[dict], index:list, threshold:float=0.4) -> list:
    for article in articles:
        padding_len = len(index) - len(article['vector'])
        article['vector'] = np.pad(article['vector'], (0, padding_len))
            
    document_freq = np.zeros(len(index))
    for article in articles:
        document_freq += np.ceil(article['vector'])

    inv_document_freq = np.zeros(len(document_freq))
    document_count = len(articles)
    for i in range(len(document_freq)):
        num = document_freq[i]
        if num != 0:
            num = math.log((1 / num) * document_count)
            inv_document_freq[i] = num

    new_clusters = []

    for article in articles:
        closest_dist = 0
        closest_cluster = None

        for cluster in new_clusters:
            new_dist = similarity(np.multiply(article['vector'], inv_document_freq), np.multiply(cluster['vector'], inv_document_freq))
            if new_dist < threshold:
                continue
            if new_dist > closest_dist:
                closest_dist = new_dist
                closest_cluster = cluster
        
        if closest_cluster == None:
            new_clusters.append({
                'vector': article['vector'],
                'articles': [article]
            })
        else: 
            closest_cluster['articles'].append(article)
            closest_cluster['vector'] = sum([closest_article['vector'] for closest_article in closest_cluster['articles']]) / len(closest_cluster['articles'])
    return new_clusters


class NewNewsClusterer(NewsClusterer):
    def create(self, new_articles:list[dict]) -> list:
        for article in new_articles:
            text = article['title'] + ' ' + article['description']
            processed = preprocess_string(text)
            article['vector'], self.word_index = vectorize(processed, self.word_index)
        self.clusters = create_cluster(new_articles, self.word_index, self.threshold)
        return self.clusters


new_clusterer = NewNewsClusterer(0.2)
new_clusters = new_clusterer.create(article_dicts)

for i, cluster in enumerate(sorted(new_clusters, reverse=True, key=lambda x: len(x['articles']))):
    if len(cluster['articles']) == 1:
        continue
    print('Cluster ', i + 1, ': ')
    for article in cluster['articles']:
        print('\t', article['company'] if 'company' in article else '?', ': ',  article['title'])
