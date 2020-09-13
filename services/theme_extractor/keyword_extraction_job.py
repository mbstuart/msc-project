from .keyword_extractor import KeywordExtractor
from .base_job import BaseJob

from typing import List

from services.libs.data_model import Article, Theme, ThemeArticleLink, ProcessedArticle

from sqlalchemy.orm import Session
from sqlalchemy import desc

from gensim.models import Doc2Vec


class JointArticle:

    def __init__(self, id, publish_date, words, title, title_words):
        self.id = id
        self.publish_date = publish_date
        self.words = words
        self.title = title
        self.title_words = title_words


class KeywordExtractionJob(BaseJob):

    def __init__(self):
        super().__init__()

    def extract_keywords_from_articles_and_labels(self, load_id: str, articles: List[Article], mapping: List[int], model: Doc2Vec):
        extractor = KeywordExtractor(model)

        themes = extractor.create_themes(load_id, articles, mapping)

        self.__persist_themes(themes, load_id)

        return themes

    def extract_keywords_from_labels(self, load_id: str, model: Doc2Vec):
        articles, mapping = self.__get_articles_for_load_id(load_id)

        extractor = KeywordExtractor(model)

        themes = extractor.create_themes(load_id, articles, mapping)
        self.__persist_themes(themes, load_id)
        return themes

    def __persist_themes(self, themes: List[Theme], load_id: str):

        theme_dict = {theme.id: theme for theme in themes}

        session: Session = self.get_session()

        for theme in session.query(Theme).filter(Theme.article_load_id == load_id).all():
            theme.name = theme_dict[theme.id].name
            theme.theme_words = theme_dict[theme.id].theme_words

        session.commit()

    def __get_articles_for_load_id(self, load_id: str):
        session: Session = self.get_session()

        q = session.query(Article.id, Article.publish_date, ProcessedArticle.words, Article.title, ProcessedArticle.title_words, Theme.id).\
            join(ProcessedArticle).\
            join(ThemeArticleLink).\
            join(Theme).\
            filter(Article.article_load_id == load_id).\
            order_by(desc(Article.publish_date))
        articles = q.all()

        jarticles = [JointArticle(
            art[0], art[1], art[2], art[3], art[4]) for art in articles]

        mapping = [art[5] for art in articles]

        return jarticles, mapping
