from services.libs.data_model.article import Article
from services.libs.data_model.article_load import ArticleLoad
from services.libs.data_model.processed_article import ProcessedArticle

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, desc

from .article_preprocessor import ArticlePreprocessor
from .base_job import BaseJob

from typing import List


class ArticlePreprocessJob(BaseJob):

    def __init__(self):
        super().__init__()

        self.preprocessor = ArticlePreprocessor()

    def preprocess_latest_articles(self):
        articles = self.get_articles_for_latest_load()
        preprocessed_articles = self.preprocess_raw_articles(articles);
        self.commit_preprocessed_articles_to_database(preprocessed_articles)

    def preprocess_latest_articles_for_load(self, load_id: str):
        articles = self.get_articles_for_latest_load()
        preprocessed_articles = self.preprocess_raw_articles(articles);
        self.commit_preprocessed_articles_to_database(preprocessed_article);

    def get_articles_for_latest_load(self):
        latest_load = self.get_latest_article_load()
        return self.get_articles_for_load(latest_load.id);
        
    def get_articles_for_load(self, load_id: str) -> List[Article]:
        session: Session = self.get_session();
        query = session.query(Article).filter_by(article_load_id = load_id)
        articles = query.all();
        return articles

    def preprocess_raw_articles(self, raw_articles: List[Article]):
        preprocessed_articles = self.preprocessor.preprocess_articles(raw_articles);
        return preprocessed_articles;

    def commit_preprocessed_articles_to_database(self, processed_articles: List[ProcessedArticle]):
        session: Session = self.get_session();

        session.bulk_save_objects(processed_articles);

        session.commit()