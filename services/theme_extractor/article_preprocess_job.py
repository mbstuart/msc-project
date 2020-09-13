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
        latest_load = self.get_latest_article_load()
        return self.preprocess_articles_for_load(latest_load.id)

    def preprocess_articles_for_load(self, load_id: str):
        articles = self.get_articles_for_load(load_id)
        preprocessed_articles = self.preprocess_raw_articles(articles, load_id)
        self.commit_preprocessed_articles_to_database(preprocessed_articles)

    def preprocess_articles_update(self, load_id: str, from_load_id: str):
        articles = self.get_articles_for_update(load_id, from_load_id)
        preprocessed_articles = self.preprocess_raw_articles_update(
            articles, from_load_id, load_id)
        self.clone_preprocessed_articles_to_new_load_id(from_load_id, load_id)
        self.commit_preprocessed_articles_to_database(preprocessed_articles)
        return preprocessed_articles

    def get_articles_for_load(self, load_id: str) -> List[Article]:
        session: Session = self.get_session()
        query = session.query(Article).filter_by(article_load_id=load_id)
        articles = query.all()
        return articles

    def get_articles_for_update(self, load_id: str, from_load_id: str) -> List[Article]:
        session: Session = self.get_session()
        from_article: Article = session.query(Article).filter_by(
            article_load_id=from_load_id).order_by(desc(Article.publish_date)).first()
        print(from_article)
        print(from_article.id)
        print(from_article.publish_date)
        query = session.query(Article).filter_by(article_load_id=load_id).filter(
            Article.publish_date > from_article.publish_date)
        articles = query.all()
        print(len(articles))
        return articles

    def preprocess_raw_articles(self, raw_articles: List[Article], load_id: str):
        preprocessed_articles = self.preprocessor.preprocess_articles(
            raw_articles, load_id)
        return preprocessed_articles

    def preprocess_raw_articles_update(self, raw_articles: List[Article], old_load_id: str, new_load_id: str):
        preprocessed_articles = self.preprocessor.preprocess_articles_update(
            raw_articles, old_load_id, new_load_id)
        return preprocessed_articles

    def clone_preprocessed_articles_to_new_load_id(self, old_load_id: str, new_load_id: str):
        session: Session = self.get_session()

        process_articles: List[ProcessedArticle] = session.query(
            ProcessedArticle).filter_by(article_load_id=old_load_id).all()

        cloned_articles: List[ProcessedArticle] = [
            pa.clone(new_load_id) for pa in process_articles]

        session.commit()

    def commit_preprocessed_articles_to_database(self, processed_articles: List[ProcessedArticle]):
        session: Session = self.get_session()

        session.bulk_save_objects(processed_articles)

        session.commit()
