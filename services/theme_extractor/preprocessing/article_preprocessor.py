from services.theme_extractor.preprocessing.transformation import HTMLStripper, PosLemma, PhraseExtractor
import os
from typing import List
from math import ceil
from gensim.models.phrases import Phrases, Phraser
from gensim.utils import simple_preprocess
from services.libs.data_model import Article, ArticleLoad, ProcessedArticle

from services.libs.utils import logger


RUN_LEMMATIZATION = 'lemmatize'
RUN_POS_TAGGING = 'postag'
RUN_PHRASING = 'phrasing'

RUN_OPTIONS = [
    RUN_LEMMATIZATION,
    RUN_POS_TAGGING,
    RUN_PHRASING
]


class ArticlePreprocessor:
    """
    Class responsible for preprocessing the articles. 

    Takes the following parameters:
    - steps: the number of steps to run. By default runs HTML tagging, lemmatization, pos tag filtering and phrasing.
    - allowed_pos_tags: the POS tags to filter by 
    - html_stripper: the HTML stripper object to use. Used for DI/unit testing
    - pos_lemma: the POS tagger / lemmatizer object to use. Used for DI/unit testing
    - phrase_extractor: the Phrase extractor object to use. Used for DI/unit testing
    """

    def __init__(self, steps=RUN_OPTIONS, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV', 'PROPN'], html_stripper=None, pos_lemma=None, phrase_extractor=None):
        self.steps = steps
        self.allowed_postags = allowed_postags

        self.html_stripper = HTMLStripper() if html_stripper is None else html_stripper
        self.pos_lemma = PosLemma() if pos_lemma is None else pos_lemma
        self.phrase_extractor = PhraseExtractor(
        ) if phrase_extractor is None else phrase_extractor

    def preprocess_articles(self, articles: List[Article], load_id: str) -> List[ProcessedArticle]:
        return self.__get_preprocessed_articles_fresh(articles, load_id)

    def preprocess_articles_update(self, articles: List[Article], old_load_id: str, new_load_id: str) -> List[ProcessedArticle]:
        return self.__get_preprocessed_articles_update(articles, old_load_id, new_load_id)

    def __get_preprocessed_articles_fresh(self, articles: List[Article], load_id: str) -> List[ProcessedArticle]:
        return self.__get_preprocessed_articles(articles, load_id)

    def __get_preprocessed_articles_update(self, articles: List[Article], old_load_id: str, new_load_id: str):
        return self.__get_preprocessed_articles(articles, new_load_id, old_load_id=old_load_id)

    def __get_preprocessed_articles(self, articles: List[Article], new_load_id: str, old_load_id: str = None):
        """
        Takes in articles as a parameter and runs preprocessing on them, returning the processed versions
        Parameters:
        - articles - the list of articles (titles + bodies)
        - new_load_id - the load_id for this run
        - old_load_id - their previous load_id, in case this is an update run

        """
        logger.info('Stripping HTML tags from the article bodies.')
        self.texts = self.html_stripper.strip_html(articles)
        self.titles = [art.title for art in articles]
        logger.info('Extracted from HTML')

        logger.info(
            'Applying POS-tag filtering and lemmatization to the documents')
        self.preprocessed_docs = self.pos_lemma.pos_tag_docs(self.texts, allowed_postags=self.allowed_postags, lemmatize=(
            RUN_LEMMATIZATION in self.steps), postag=(RUN_POS_TAGGING in self.steps))
        logger.info('Docs preprocessed and tokenized')
        self.preprocessed_titles = self.pos_lemma.pos_tag_docs(self.titles, allowed_postags=self.allowed_postags, lemmatize=(
            RUN_LEMMATIZATION in self.steps), postag=(RUN_POS_TAGGING in self.steps))
        logger.info('Titles preprocessed and tokenized')
        if RUN_PHRASING in self.steps:
            if old_load_id is None:
                self.phrase_texts, self.phrase_titles = self.phrase_extractor.build_phrases(
                    self.preprocessed_docs, self.preprocessed_titles, new_load_id)
            else:
                self.phrase_texts, self.phrase_titles = self.phrase_extractor.build_phrases_update(
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
