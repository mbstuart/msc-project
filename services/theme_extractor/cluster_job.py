from services.libs.data_model.article import Article
from services.libs.data_model.article_load import ArticleLoad
from services.libs.data_model.processed_article import ProcessedArticle
from services.libs.data_model.theme import Theme
from services.libs.data_model.theme_article_link import ThemeArticleLink

from .base_job import BaseJob
from .clusterer import Clusterer
from .article_preprocessor import ArticlePreprocessor


from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, desc, and_


from typing import List

from datetime import datetime
from gensim.models import Doc2Vec


class JointArticle:

    def __init__(self, id, publish_date, words, title, title_words):
        self.id = id;
        self.publish_date = publish_date;
        self.words = words;
        self.title = title;
        self.title_words = title_words;

class ClusterJob(BaseJob):

    def __init__(self, model: Doc2Vec, load_id: str):
        super().__init__();

        self.model = model;
        self.load_id = load_id;


    def get_clusters(self, from_scratch=False):
        articles = self.filter_articles();

        clusterer = Clusterer(self.model, articles, self.load_id, from_scratch=from_scratch, min_cluster_size=3, cluster_selection_epsilon=0.1)

        themes, mapping = clusterer.create_themes_and_mapping();

        self.__persist_themes(themes)
        self.__persist_theme_article_map(mapping, articles);

        return themes, mapping

    def __persist_themes(self, themes: List[Theme] ):

        session: Session = self.get_session();

        for theme in themes:
            session.merge(theme)

        session.commit();



    def __persist_theme_article_map(self, theme_mapping, articles):
        session: Session = self.get_session();

        for i, cluster_id in enumerate(theme_mapping):
            article = articles[i];
            theme_article_map = ThemeArticleLink(cluster_id, article.id, self.load_id)
            session.merge(theme_article_map)

        session.commit()

    def filter_articles(self, years = 10):

        session: Session = self.get_session();

        most_recent_date: datetime.datetime = session.query(Article).order_by(desc(Article.publish_date)).first().publish_date;

        n_years_ago = most_recent_date.replace(year = most_recent_date.year - years)

        q = session.query(Article.id, Article.publish_date, ProcessedArticle.words, Article.title, ProcessedArticle.title_words).\
        join(ProcessedArticle, and_(ProcessedArticle.id==Article.id, ProcessedArticle.article_load_id==Article.article_load_id))\
            .filter(Article.publish_date >= n_years_ago)\
            .filter(Article.article_load_id == self.load_id)\
            .order_by(desc(Article.publish_date))
        articles = q.all();

        articles = [JointArticle(art[0], art[1], art[2], art[3], art[4]) for art in articles]

        return articles;

