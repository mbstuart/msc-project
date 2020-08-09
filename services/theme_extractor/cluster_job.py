from base_job import BaseJob
from clusterer import Clusterer
from article_load import ArticleLoad
from sqlalchemy.orm import sessionmaker, Session
from article import Article
from sqlalchemy import create_engine, desc, and_
from article_preprocessor import ArticlePreprocessor
from typing import List
from processed_article import ProcessedArticle
from datetime import datetime;
from gensim.models import Doc2Vec

class ClusterJob(BaseJob):

    def __init__(self, model: Doc2Vec, load_id: str):
        super().__init__();

        self.model = model;
        self.load_id = load_id;


    def get_clusters(self):
        articles = self.filter_articles()

        clusterer = Clusterer(self.model, articles, self.load_id)

        clusters = self.clusterer.create_clusters();

        return clusters


    def filter_articles(self, years = 2):

        
        session: Session = self.sessionmaker();

        most_recent_date: datetime.datetime = session.query(Article).order_by(desc(Article.publish_date)).first().publish_date;

        n_years_ago = most_recent_date.replace(year = most_recent_date.year - years)

        q = session.query(Article).join(ProcessedArticle, and_(ProcessedArticle.id==Article.id, ProcessedArticle.article_load_id==Article.article_load_id)).filter(Article.publish_date >= n_years_ago)
        articles = q.all();

        return articles;

