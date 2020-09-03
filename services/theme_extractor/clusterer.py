from collections import Counter
from scipy import spatial
from gensim.models import Doc2Vec
import numpy as np
from typing import List
import os

from services.libs.data_model.processed_article import ProcessedArticle

from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from sklearn.metrics.pairwise import cosine_similarity

from umap import UMAP
from hdbscan import HDBSCAN

from .logger import logger

import en_core_web_sm
nlp = en_core_web_sm.load(disable=['ner', 'parser'])

from services.libs.data_model.theme import Theme
from services.libs.data_model.article import Article

import math 
import itertools

class Clusterer():

    __CLUSTER_FOLDER = 'clusters'

    __CLUSTER_FILE = 'cluster_data_hdbscan'

    __UMAP_FILE = 'cluster_data_umap'

    processed_articles: list

    cluster_matrix: np.array

    def __init__(self, model: Doc2Vec, processed_articles: list, load_id: str, from_scratch=False,min_cluster_size=5, min_samples=2, cluster_selection_epsilon=0.5):
        self.model = model
        self.processed_articles = processed_articles
        self.load_id = load_id

        if self.__model_is_saved() and not(from_scratch):
            logger.info('Loading HDBSCAN model from files')
            self.cluster_matrix = self.__load_hdbscan_clusters()
        else:
            logger.info('Creating HDBSCAN model from scratch')
            self.cluster_matrix = self.__create_hdbscan_clusters(from_scratch, min_cluster_size, min_samples, cluster_selection_epsilon)

    def create_themes_and_mapping(self):
        logger.info('Request to get mapping / themes')
        mapping = self.__create_clusters()
        themes = self.__create_themes(mapping);
        logger.info('Request to get mapping / themes complete')
        return themes, mapping

    def create_mapping(self):
        mapping = self.__create_clusters()
        return mapping;

    def __create_hdbscan_clusters(self, from_scratch, min_cluster_size, min_samples, cluster_selection_epsilon):
        instance_vectors = self.__get_vecs_for_classification();
        return self.__create_hdbscan_model(instance_vectors, from_scratch, min_cluster_size, min_samples, cluster_selection_epsilon);
        
    def __create_clusters(self):
        clusters = self.cluster_matrix
        return clusters;

    def __create_themes(self, clusters):

        cluster_ids = np.unique(clusters);

        themes = []

        ten_pct = math.ceil(len(cluster_ids) / 10)

        print('Extracting keywords for {} themes'.format(len(cluster_ids)))

        for i, cluster in enumerate(cluster_ids):
            theme_words, title = self.__get_class_words_for_label(clusters, cluster)
            theme_model = Theme(int(cluster), title, self.load_id, theme_words)
            themes.append(theme_model)

            if i % ten_pct == 0:
                logger.info('{} / {} themes keywords extracted'.format(i, len(cluster_ids)))

        return themes

    def __get_vecs_for_classification(self):
        vecs = list([self.model.docvecs[doc.id] for doc in self.processed_articles])
        
        # datetimes = np.array([art.publish_date for art in self.processed_articles])

        # max_date = np.amax(datetimes)
        # min_date = np.amin(datetimes)

        # normalised_datetimes = ((datetimes - min_date) / (max_date - min_date)).reshape((len(datetimes), 1))

        # vecs_with_dates = np.append(vecs, normalised_datetimes, axis=1)

        return vecs

    def __folder_path(self):
        return '{}/{}'.format(self.__CLUSTER_FOLDER, self.load_id)

    def __file_path(self):
        return '{}/{}.npy'.format(self.__folder_path(), self.__CLUSTER_FILE)

    def __umap_file_path(self):
        return '{}/{}.npy'.format(self.__folder_path(), self.__UMAP_FILE)

    def __model_is_saved(self):
        return os.path.isfile(self.__file_path());

    def __umap_is_saved(self):
        return os.path.isfile(self.__umap_file_path());

    def __create_hdbscan_model(self, vectors: np.array, from_scratch, min_cluster_size, min_samples, cluster_selection_epsilon, max_number_to_cluster = 50000):
        
        logger.info('Creating HDBSCAN model on {} / {} documents'.format(max_number_to_cluster, len(vectors)))
        
        if self.__umap_is_saved():
            logger.info('Loading UMAP from disk')
            embedding = self.__load_umap()
        else:
            logger.info('Creating UMAP dimension reduction')
            embedding = UMAP(random_state=666, metric='cosine', n_components=100, verbose=True).fit_transform(vectors)
            logger.info('UMAP matrix created. Saving to disk.')
            os.mkdir(self.__folder_path())
            np.save(self.__umap_file_path(), embedding)
        
        max_number_to_cluster = min(max_number_to_cluster, len(vectors))
        
        logger.info('Creating HDBSCAN model')
        clusterer = HDBSCAN(prediction_data=True, metric='euclidean', min_cluster_size=min_cluster_size, min_samples=min_samples, cluster_selection_epsilon=cluster_selection_epsilon)
        clusterer.fit(embedding[:max_number_to_cluster])
        labels = clusterer.labels_;
        num_clusters = labels.max();
        num_unclassified = len(labels[labels == -1])

        biggest_classes = Counter(labels).most_common(5)

        biggest_class_logs = ['class {}, {} documents'.format(cl[0], cl[1]) for cl in biggest_classes]

        logger.info('5 biggest classes: {}'.format('\n'.join(biggest_class_logs)));

        logger.info('HDBSCAN model created. It has detected {} clusters, with {} / {} documents unclassified.'.format(num_clusters, num_unclassified, len(labels)))
        
        if not(self.__model_is_saved):
            np.save(self.__file_path(), labels)
        return labels;

    def __load_cluster_matrix(self):
        Z = np.load(self.__file_path())
        return Z;

    def __load_umap(self):
        Z = np.load(self.__umap_file_path())
        return Z;


    def __load_hdbscan_clusters(self):
        Z = np.load(self.__file_path())
        return Z;


    def __get_class_words_for_label(self, labels: List[str], label: str):

        if label == "-1" or label == -1:
            return [], "Unclassified"

        doc_arr = np.array(self.processed_articles)
        doc_arr_trimmed = doc_arr[:len(labels)]
        docs_in_class = doc_arr_trimmed[labels == label]
        # vecs = self.model.docvecs.vectors_docs[:len(labels)][labels == label]

        vecs = list([self.model.docvecs[doc.id] for doc in docs_in_class])

        class_words = self.__get_class_words_from_doc_selection(docs_in_class, vecs, self.model)

        title = class_words[0];

        class_words = class_words[1:]
                
        return class_words, title;
        

    # def __get_class_words_for_label_group(self, labels: List[str], label_group: List[str]):
        
    #     filter_arr = [(label in label_group) for label in labels]

    #     docs_in_class = np.array(self.processed_articles)[:len(labels)][filter_arr]
    #     vecs = self.model.docvecs.vectors_docs[:len(labels)][filter_arr]
        
    #     return self.__get_class_words_from_doc_selection(docs_in_class, vecs)

    def __get_class_words_from_doc_selection(self, docs_in_class: List[Article], vecs: list, model: Doc2Vec):

        n_grams = []

        for art in docs_in_class:
            words =  art.title_words if len(docs_in_class) > 3 else art.words + art.title_words;
            # n_grams += [[word] for word in words]
            n_grams += self.__generate_ngrams(words, 2)
            n_grams += self.__generate_ngrams(words, 3)
            n_grams += self.__generate_ngrams(words, 4)


        n_grams.sort()
        n_grams = list(n_grams for n_grams,_ in itertools.groupby(n_grams))

        scores = {}
        docvecs = np.array(vecs)

        for i, n_gram in enumerate(n_grams):
            
            p_vec = model.infer_vector(n_gram).reshape(1, 400)

            sim = cosine_similarity(p_vec, docvecs)
            scores[i] = np.min(sim) ##len(sim) / np.sum(1.0/sim)  

        def convert_ngram_to_string(ngram: List[str]):
            return " ".join(ngram).replace("_", " ")

        return [convert_ngram_to_string(n_grams[p[0]]) for p in Counter(scores).most_common(10)]


    # def __get_class_words_from_doc_selection(self, docs_in_class: List[ProcessedArticle], vecs):

    #     d = Counter(sum([doc.words for doc in docs_in_class], []))

    #     top_words = d.most_common(200)

    #     word_2_vec_ranking = {}

    #     for word in top_words:
            
    #         if(word[0] not in self.model.wv.vocab):
    #             continue;
            
    #         word_vec = self.model[word[0]]
    #         av_vec = np.average(vecs, axis=0)


    #         similarity = 1 - spatial.distance.cosine(word_vec, av_vec)
    #         word_2_vec_ranking[word[0]] = similarity

    #     rank_counter = Counter(word_2_vec_ranking)

    #     return [w[0] for w in rank_counter.most_common(10)]

    def __generate_ngrams(self, words_list: List[str], n: int):
        ngrams_list = []
    
        for num in range(0, len(words_list) - (n - 1)):
            ngram = (words_list[num:num + n])
            ngrams_list.append(ngram)
    
        return ngrams_list