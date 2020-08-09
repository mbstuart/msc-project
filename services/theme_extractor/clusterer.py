from collections import Counter
from scipy import spatial
from gensim.models import Doc2Vec
import numpy as np
from typing import List
from processed_article import ProcessedArticle
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
import os
from theme import Theme
from article import Article

class Clusterer():

    __CLUSTER_FOLDER = 'clusters'

    __CLUSTER_FILE = 'cluster_data'

    processed_articles: list

    cluster_matrix: np.array

    def __init__(self, model: Doc2Vec, processed_articles: list, load_id: str):
        self.model = model
        self.processed_articles = processed_articles
        self.load_id = load_id

        if self.__model_is_saved():
            self.cluster_matrix = self.__load_cluster_matrix()
        else:
            self.cluster_matrix = self.__create_cluster_matrix()

    def create_themes_and_mapping(self):
        mapping = self.__create_clusters()
        themes = self.__create_themes(mapping);
        return themes, mapping

    def __create_cluster_matrix(self):
        instance_vectors = self.__get_vecs_for_classification();
        return self.__create_agglomerative_clustering_model(instance_vectors);
        
    def __create_clusters(self):
        clusters = fcluster(self.cluster_matrix, 200, criterion='maxclust')
        return clusters;

    def __create_themes(self, clusters):

        cluster_ids = np.unique(clusters);

        themes = []

        for cluster in cluster_ids:
            theme_words = self.__get_class_words_for_label(clusters, cluster)
            theme_model = Theme(int(cluster), 'Cluster-{}'.format(str(cluster)), self.load_id, theme_words)
            themes.append(theme_model)

        return themes

    def __get_vecs_for_classification(self):
        vecs = self.model.docvecs.vectors_docs[:(len(self.processed_articles))]
        
        datetimes = np.array([art.publish_date for art in self.processed_articles])

        max_date = np.amax(datetimes)
        min_date = np.amin(datetimes)

        normalised_datetimes = ((datetimes - min_date) / (max_date - min_date)).reshape((len(datetimes), 1))

        vecs_with_dates = np.append(vecs, normalised_datetimes, axis=1)

        return vecs_with_dates

    def __folder_path(self):
        return '{}/{}'.format(self.__CLUSTER_FOLDER, self.load_id)

    def __file_path(self):
        return '{}/{}.npy'.format(self.__folder_path(), self.__CLUSTER_FILE)

    def __model_is_saved(self):
        return os.path.isfile(self.__file_path());

    def __create_agglomerative_clustering_model(self, vectors: np.array):
        Z = linkage(vectors, metric='cosine', method='complete')
        os.mkdir(self.__folder_path())
        np.save(self.__file_path(), Z)
        return Z;

    def __load_cluster_matrix(self):
        Z = np.load(self.__file_path())
        return Z;


    def __get_class_words_for_label(self, labels: List[str], label: str):
        docs_in_class = np.array(self.processed_articles)[:len(labels)][labels == label]
        vecs = self.model.docvecs.vectors_docs[:len(labels)][labels == label]
        class_words = self.__get_class_words_from_doc_selection(docs_in_class, vecs)
                
        return class_words;
        

    def __get_class_words_for_label_group(self, labels: List[str], label_group: List[str]):
        
        filter_arr = [(label in label_group) for label in labels]

        docs_in_class = np.array(self.processed_articles)[:len(labels)][filter_arr]
        vecs = self.model.docvecs.vectors_docs[:len(labels)][filter_arr]
        
        return self.__get_class_words_from_doc_selection(docs_in_class, vecs)

    def __get_class_words_from_doc_selection(self, docs_in_class: List[ProcessedArticle], vecs):
        doc_dict = {}

        for doc in docs_in_class:
            for word in doc.words:
                if word in doc_dict:
                    doc_dict[word] += 1
                else:
                    doc_dict[word] = 1

        d = Counter(doc_dict)

        top_words = d.most_common(1000)

        word_2_vec_ranking = {}

        for word in top_words:
            
            if(word[0] not in self.model.wv.vocab):
                continue;
            
            word_vec = self.model[word[0]]
            av_vec = np.average(vecs, axis=0)


            similarity = 1 - spatial.distance.cosine(word_vec, av_vec)
            word_2_vec_ranking[word[0]] = similarity

        rank_counter = Counter(word_2_vec_ranking)

        return [w[0] for w in rank_counter.most_common(10)]