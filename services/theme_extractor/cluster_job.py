from services.libs.data_model.article import Article
from services.libs.data_model.article_load import ArticleLoad
from services.libs.data_model.processed_article import ProcessedArticle
from services.libs.data_model.theme import Theme
from services.libs.data_model.theme_article_link import ThemeArticleLink

from base_job import BaseJob
from clusterer import Clusterer


from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, desc, and_

from article_preprocessor import ArticlePreprocessor

from typing import List

from datetime import datetime;
from gensim.models import Doc2Vec


class JointArticle:

    def __init__(self, id, publish_date, words):
        self.id = id;
        self.publish_date = publish_date;
        self.words = words;

class ClusterJob(BaseJob):

    def __init__(self, model: Doc2Vec, load_id: str):
        super().__init__();

        self.model = model;
        self.load_id = load_id;


    def get_clusters(self):
        articles = self.filter_articles()

        clusterer = Clusterer(self.model, articles, self.load_id)

        themes, mapping = clusterer.create_themes_and_mapping();

        self.__persist_themes(themes)
        self.__persist_theme_article_map(mapping, articles);

        return themes, mapping

    def __persist_themes(self, themes: List[Theme] ):

        session: Session = self.sessionmaker();

        for theme in themes:
            session.merge(theme)

        session.commit();



    def __persist_theme_article_map(self, theme_mapping, articles):
        session: Session = self.sessionmaker();

        for i, cluster_id in enumerate(theme_mapping):
            article = articles[i];
            theme_article_map = ThemeArticleLink(cluster_id, article.id, self.load_id)
            session.merge(theme_article_map)

        session.commit()

    def filter_articles(self, years = 1):

        
        session: Session = self.sessionmaker();

        most_recent_date: datetime.datetime = session.query(Article).order_by(desc(Article.publish_date)).first().publish_date;

        n_years_ago = most_recent_date.replace(year = most_recent_date.year - years)

        q = session.query(Article.id, Article.publish_date, ProcessedArticle.words).join(ProcessedArticle, and_(ProcessedArticle.id==Article.id, ProcessedArticle.article_load_id==Article.article_load_id)).filter(Article.publish_date >= n_years_ago)
        articles = q.all();

        articles = [JointArticle(art[0], art[1], art[2]) for art in articles]

        return articles;
