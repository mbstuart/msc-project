import os
from typing import List
from math import ceil
from gensim.models.phrases import Phrases, Phraser
from gensim.utils import simple_preprocess
import en_core_web_sm
from services.libs.data_model import Article, ArticleLoad, ProcessedArticle

from services.libs.utils import logger

from bs4 import BeautifulSoup

import nltk
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

nlp = en_core_web_sm.load(disable=['ner', 'parser'])

RUN_LEMMATIZATION = 'lemmatize'
RUN_STOPWORDS = 'stopwords'
RUN_POS_TAGGING = 'postag'
RUN_PHRASING = 'phrasing'

RUN_OPTIONS = [
    RUN_LEMMATIZATION,
    RUN_POS_TAGGING,
    RUN_PHRASING
]


class ArticlePreprocessor:

    __PREPROCESS_FOLDER = 'preprocess'

    __PHRASER_FILE = 'phrases'

    def __init__(self, steps=RUN_OPTIONS, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV', 'PROPN']):
        self.steps = steps
        self.allowed_postags = allowed_postags

        if not(os.path.isdir(self.__PREPROCESS_FOLDER)):
            os.mkdir(self.__PREPROCESS_FOLDER)

    def preprocess_articles(self, articles: List[Article], load_id: str) -> List[ProcessedArticle]:
        return self.__get_tagged_data_fresh(articles, load_id)

    def preprocess_articles_update(self, articles: List[Article], old_load_id: str, new_load_id: str) -> List[ProcessedArticle]:
        return self.__get_tagged_data_update(articles, old_load_id, new_load_id)

    def __lemmatization(self, text: List[str], allowed_postags: List[str]) -> List[str]:
        texts_out = []
        doc = nlp(" ".join(text))
        texts_out.append(
            [token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out

    def __get_tagged_data_fresh(self, articles: List[Article], load_id: str) -> List[ProcessedArticle]:
        return self.__get_tagged_data(articles, load_id)

    def __get_tagged_data_update(self, articles: List[Article], old_load_id: str, new_load_id: str):
        return self.__get_tagged_data(articles, new_load_id, old_load_id=old_load_id)

    def __get_tagged_data(self, articles: List[Article], new_load_id: str, old_load_id: str = None):
        logger.info('Getting tagged data')
        self.texts = [self.__extract_text_from_html(
            res.body) for res in articles]
        self.titles = [art.title for art in articles]

        logger.info('Extracted from HTML')
        self.preprocessed_docs = self.__pos_tag_docs(self.texts, allowed_postags=self.allowed_postags, lemmatize=(
            RUN_LEMMATIZATION in self.steps), postag=(RUN_POS_TAGGING in self.steps))
        logger.info('Docs preprocessed and tokenized')
        self.preprocessed_titles = self.__pos_tag_docs(self.titles, allowed_postags=self.allowed_postags, lemmatize=(
            RUN_LEMMATIZATION in self.steps), postag=(RUN_POS_TAGGING in self.steps))
        logger.info('Titles preprocessed and tokenized')
        if RUN_PHRASING in self.steps:
            if old_load_id is None:
                self.phrase_texts, self.phrase_titles = self.__build_phrases(
                    self.preprocessed_docs, self.preprocessed_titles, new_load_id)
            else:
                self.phrase_texts, self.phrase_titles = self.__build_phrases_update(
                    self.preprocessed_docs, self.preprocessed_titles, old_load_id, new_load_id)
            logger.info('Phrases built for docs + titles')
        else:
            self.phrase_texts = self.preprocessed_docs
            self.phrase_titles = self.preprocessed_titles
            logger.info('Phrases step skipped')
        self.processed_articles: List[ProcessedArticle] = []
        for i, article in enumerate(articles):
            pa = ProcessedArticle(
                article.id, article.article_load_id, self.phrase_texts[i], self.phrase_titles[i])
            self.processed_articles.append(pa)
        return self.processed_articles

    def __extract_text_from_html(self, res: str) -> str:
        soup = BeautifulSoup(res, features="lxml")

        for f in soup.find_all('figure'):
            f.decompose()

        text = soup.get_text().lower()

        return text

    def __pos_tag_docs(self, results: List[str], allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV', 'PROPN'], lemmatize=True, postag=True):

        out = []

        l = len(results)

        step = ceil(l / 20)

        def pick_token(token):
            return (token.pos_ in allowed_postags and len(token.lemma_) > 1) if postag else True

        i = 0

        for res in nlp.pipe(results):

            if lemmatize:
                out.append(
                    [token.lemma_ for token in res if pick_token(token)])
            else:
                out.append(
                    [token.lemma_ for token in res if pick_token(token)])

            i += 1
            if i % step == 0:
                logger.info(
                    'Preprocess - {:d}% completed'.format(ceil(100 * i / l)))

        return out

    def __build_phrases(self, tokenized_texts, tokenized_titles, load_id):

        phrases = Phrases(tokenized_texts + tokenized_titles,
                          scoring='npmi', threshold=0.2, min_count=50, progress_per=1000)
        self.__save_phrase_model(phrases, load_id)

        return [phrases[phrases[tokens]] for tokens in tokenized_texts], [phrases[phrases[tokens]] for tokens in tokenized_titles]

    def __build_phrases_update(self, tokenized_texts, tokenized_titles, old_load_id: str, new_load_id: str):

        phrases: Phrases = None

        phrases = self.__get_phrase_model(old_load_id)
        phrases.add_vocab(tokenized_texts + tokenized_titles)
        self.__save_phrase_model(phrases, new_load_id)

        return [phrases[phrases[tokens]] for tokens in tokenized_texts], [phrases[phrases[tokens]] for tokens in tokenized_titles]

    def __get_phrase_model(self, load_id):
        return Phrases.load(self.__phrase_model_path(load_id))

    def __save_phrase_model(self, phrase: Phrases, load_id: str):
        os.mkdir(self.__folder_path(load_id))
        phrase.save(self.__phrase_model_path(load_id))

    def __folder_path(self, load_id: str):
        return '{}/{}'.format(self.__PREPROCESS_FOLDER, load_id)

    def __phrase_model_path(self, load_id):
        return '{}/{}.pkl'.format(self.__folder_path(load_id), self.__PHRASER_FILE)
