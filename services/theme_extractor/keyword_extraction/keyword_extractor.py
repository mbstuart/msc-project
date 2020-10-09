import numpy as np
import itertools
import math

from collections import Counter

from gensim.models import Doc2Vec

from typing import List

from services.libs.data_model import ProcessedArticle, Article, Theme

from services.libs.utils import logger

from sklearn.metrics.pairwise import cosine_similarity


class KeywordExtractor:
    """
    Class responsible for extracting the keywords to associate with each theme
    Parameters:
    - model: trained Doc2Vec model
    """

    def __init__(self, model: Doc2Vec):
        self.model = model

    def create_themes(self, load_id: str, articles: List[Article], labels: List[int]):
        """
        Method for building the themes based on the mapping from articles to cluster ids
        Params: 
        - load_id: load_id of the articles 
        - articles: list of articles
        - labels: the mapping of articles -> labels. Should be the same length as the list of articles

        """
        label_ids = np.unique(labels)

        themes = []

        ten_pct = math.ceil(len(label_ids) / 10)

        print('Extracting keywords for {} themes'.format(len(label_ids)))

        for i, label in enumerate(label_ids):
            theme_words, title = self.__get_class_words_for_label(
                articles, labels, label)
            theme_model = Theme(int(label), title, load_id, theme_words)
            themes.append(theme_model)

            if i % ten_pct == 0:
                logger.info(
                    '{} / {} themes keywords extracted'.format(i, len(label_ids)))

        return themes

    def __get_class_words_for_label(self, articles: List[Article], labels: List[str], label: str):

        # unclassified has label -1 - we don't map this so we just return unclassified
        if label == "-1" or label == -1:
            return [], "Unclassified"

        doc_arr = np.array(articles)
        doc_arr_trimmed = doc_arr[:len(labels)]
        docs_in_class = doc_arr_trimmed[labels == label]

        # get the document vectors for each of the documents
        vecs = list([self.model.docvecs[doc.id] for doc in docs_in_class])

        # get the keywords for the theme
        class_words = self.__get_class_words_from_doc_selection(
            docs_in_class, vecs, self.model)

        # set the title as the first keyword
        title = class_words[0]

        class_words = class_words[1:]

        return class_words, title

    def __get_class_words_from_doc_selection(self, docs_in_class: List[Article], vecs: list, model: Doc2Vec):

        n_grams = []

        # for each article associated with the theme, get the ngrams where n in (2,3,4) for the titles (and if there are 3 or fewer - then get ngrams from the body too)
        for art in docs_in_class:
            words = art.title_words if len(
                docs_in_class) > 3 else art.words + art.title_words
            n_grams += self.__generate_ngrams(words, 2)
            n_grams += self.__generate_ngrams(words, 3)
            n_grams += self.__generate_ngrams(words, 4)

        n_grams.sort()
        # remove the duplicates from the list
        n_grams = list(n_grams for n_grams, _ in itertools.groupby(n_grams))

        scores = {}
        docvecs = np.array(vecs)

        for i, n_gram in enumerate(n_grams):

            # use the model to infer the vector for a document containing just that ngram
            p_vec = model.infer_vector(n_gram).reshape(1, 400)

            # get the similarity of this vector to the docvecs
            sim = cosine_similarity(p_vec, docvecs)

            # use the minimum similarity as the score for this ngram
            scores[i] = np.min(sim)  # len(sim) / np.sum(1.0/sim)

        def convert_ngram_to_string(ngram: List[str]):
            return " ".join(ngram).replace("_", " ")
        # return the top 10, ranked by the score
        return [convert_ngram_to_string(n_grams[p[0]]) for p in Counter(scores).most_common(10)]

    def __generate_ngrams(self, words_list: List[str], n: int):
        ngrams_list = []

        for num in range(0, len(words_list) - (n - 1)):
            ngram = (words_list[num:num + n])
            ngrams_list.append(ngram)

        return ngrams_list
