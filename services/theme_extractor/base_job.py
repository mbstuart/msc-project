from article_load import ArticleLoad
from sqlalchemy.orm import sessionmaker, Session
from article import Article
from sqlalchemy import create_engine, desc
from article_preprocessor import ArticlePreprocessor
from typing import List
from processed_article import ProcessedArticle

class BaseJob:

    db_string = "postgres://theme-extractor:tepassword@localhost:5432/theme-extractor"

    sessionmaker: sessionmaker

    def __init__(self):
        self.engine = create_engine(self.db_string)
        self.sessionmaker = sessionmaker()
        self.sessionmaker.configure(bind=self.engine)
    
    def get_latest_article_load(self) -> ArticleLoad:
        session = self.sessionmaker();
        res = session.query(ArticleLoad).order_by(desc(ArticleLoad.start_time)).first() 
        return res; 