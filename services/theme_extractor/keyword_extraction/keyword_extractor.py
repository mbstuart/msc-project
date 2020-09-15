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

    def __init__(self, model: Doc2Vec):
        self.model = model

    def create_themes(self, load_id: str, articles: List[Article], labels: List[int]):

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

        if label == "-1" or label == -1:
            return [], "Unclassified"

        doc_arr = np.array(articles)
        doc_arr_trimmed = doc_arr[:len(labels)]
        docs_in_class = doc_arr_trimmed[labels == label]

        vecs = list([self.model.docvecs[doc.id] for doc in docs_in_class])

        class_words = self.__get_class_words_from_doc_selection(
            docs_in_class, vecs, self.model)

        title = class_words[0]

        class_words = class_words[1:]

        return class_words, title

    def __get_class_words_from_doc_selection(self, docs_in_class: List[Article], vecs: list, model: Doc2Vec):

        n_grams = []

        for art in docs_in_class:
            words = art.title_words if len(
                docs_in_class) > 3 else art.words + art.title_words
            # n_grams += [[word] for word in words]
            n_grams += self.__generate_ngrams(words, 2)
            n_grams += self.__generate_ngrams(words, 3)
            n_grams += self.__generate_ngrams(words, 4)

        n_grams.sort()
        n_grams = list(n_grams for n_grams, _ in itertools.groupby(n_grams))

        scores = {}
        docvecs = np.array(vecs)

        for i, n_gram in enumerate(n_grams):

            p_vec = model.infer_vector(n_gram).reshape(1, 400)

            sim = cosine_similarity(p_vec, docvecs)
            scores[i] = np.min(sim)  # len(sim) / np.sum(1.0/sim)

        def convert_ngram_to_string(ngram: List[str]):
            return " ".join(ngram).replace("_", " ")

        return [convert_ngram_to_string(n_grams[p[0]]) for p in Counter(scores).most_common(10)]

    def __generate_ngrams(self, words_list: List[str], n: int):
        ngrams_list = []

        for num in range(0, len(words_list) - (n - 1)):
            ngram = (words_list[num:num + n])
            ngrams_list.append(ngram)

        return ngrams_list
