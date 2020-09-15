from services.libs.data_model import Article, ArticleLoad, ProcessedArticle

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, desc, inspect

from .article_preprocessor import ArticlePreprocessor
from services.theme_extractor.base_job import BaseJob

from typing import List

import numpy as np


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
        self.commit_preprocessed_articles_to_database(
            load_id, preprocessed_articles)

    def preprocess_articles_update(self, load_id: str, from_load_id: str):
        articles = self.get_articles_for_update(load_id, from_load_id)
        preprocessed_articles = self.preprocess_raw_articles_update(
            articles, from_load_id, load_id)
        self.clone_preprocessed_articles_to_new_load_id(from_load_id, load_id)
        self.commit_preprocessed_articles_to_database(
            load_id, preprocessed_articles)
        return preprocessed_articles

    def get_articles_for_load(self, load_id: str, max_articles=None) -> List[Article]:
        session: Session = self.get_session()
        query = session.query(Article).filter_by(article_load_id=load_id)
        if max_articles is not None:
            query = query.limit(max_articles)
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

        keys = inspect(ProcessedArticle).columns.keys()

        def get_columns(post): return {key: getattr(post, key) for key in keys}

        process_articles: List[ProcessedArticle] = session.query(
            ProcessedArticle).filter_by(article_load_id=old_load_id).all()

        already_added = frozenset([pa.id for pa in session.query(ProcessedArticle).filter_by(
            article_load_id=new_load_id).all()])

        process_articles_to_add = [
            art for art in process_articles if art.id not in already_added]

        session.bulk_insert_mappings(ProcessedArticle, (get_columns(
            art.clone(new_load_id)) for art in process_articles_to_add))

        # for pa in process_articles:
        #     session.add(pa.clone(new_load_id))

        session.commit()

    def commit_preprocessed_articles_to_database(self, load_id, processed_articles: List[ProcessedArticle]):
        session: Session = self.get_session()

        already_added = frozenset([pa.id for pa in session.query(ProcessedArticle).filter_by(
            article_load_id=load_id).all()])

        process_articles_to_add = [
            art for art in processed_articles if art.id not in already_added]

        session.bulk_save_objects(process_articles_to_add)

        session.commit()
