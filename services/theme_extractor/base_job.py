from services.libs.data_model.article import Article
from services.libs.data_model.article_load import ArticleLoad
from services.libs.data_model.processed_article import ProcessedArticle

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, desc

from services.libs.db_connection.session import get_session

from typing import List

class BaseJob:

    session: Session

    made_session: False

    def __init__(self, session = None):

        self.session = session;
        if session is None:
            self.made_session = True
            self.session = get_session();

    def get_session(self):

        if not hasattr(self, 'session'):
            self.made_session = True
            self.session = get_session(); 

        session = self.session
        return session;
    
    def get_latest_article_load(self) -> ArticleLoad:
        session: Session = self.get_session();
        res = session.query(ArticleLoad).filter(active=True).order_by(desc(ArticleLoad.start_time)).first() 
        return res; 

    def __del__(self):
        print('in destructor');
        if self.made_session:
            print('deleting session');
            self.session.close()

