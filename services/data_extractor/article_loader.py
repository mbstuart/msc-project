from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.libs.data_model.article import Article
from services.libs.data_model.article_load import ArticleLoad
from datetime import datetime

class ArticleLoader:

    db_string = "postgres://theme-extractor:tepassword@localhost:5432/theme-extractor"

    def __init__(self):
        self.engine = create_engine(self.db_string)
        self.get_session = sessionmaker()
        self.get_session.configure(bind=self.engine)

    def create_load_session(self):
        session = self.get_session();
        load = ArticleLoad()
        session.add(load)
        session.commit()
        
        return load.id

    def insert_articles(self, article_list, load_id):
        session = self.get_session();

        for article in article_list:
            article_row = Article(
                article['id'],
                article['body'],
                article['title'],
                article['source_tag'],
                article['publish_date'],
                load_id
            )
            session.merge(article_row);
        session.commit()