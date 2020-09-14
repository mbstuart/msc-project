from sqlalchemy import create_engine, desc, inspect
from sqlalchemy.orm import sessionmaker, Session
from services.libs.data_model.article import Article
from services.libs.data_model.article_load import ArticleLoad
from datetime import datetime

from services.libs.utils import logger


class ArticleLoader:

    db_string = "postgres://theme-extractor:tepassword@localhost:5432/theme-extractor"

    def __init__(self):
        self.engine = create_engine(self.db_string)
        self.get_session = sessionmaker()
        self.get_session.configure(bind=self.engine)

    def create_load_session(self) -> str:
        session = self.get_session()
        load = ArticleLoad()
        session.add(load)
        session.commit()

        return load.id

    def insert_articles(self, article_list, load_id):
        session = self.get_session()

        for article in article_list:
            article_row = Article(
                article['id'],
                article['body'],
                article['title'],
                article['source_tag'],
                article['publish_date'],
                load_id
            )
            session.merge(article_row)
        session.commit()

    def copy_load_session(self, from_load_id):

        session: Session = self.get_session()

        articles = session.query(Article).filter_by(
            article_load_id=from_load_id).order_by(desc(Article.publish_date)).all()

        from_date = articles[0].publish_date

        to_load_id = self.create_load_session()

        print('starting load session')

        keys = inspect(Article).columns.keys()

        def get_columns(post): return {key: getattr(post, key) for key in keys}

        session.bulk_insert_mappings(Article, (get_columns(
            art.clone(load_id=to_load_id)) for art in articles))

        # for i, art in enumerate(articles):

        #     if i % 500 == 0:
        #         logger.info('{} articles copied from {} to {}'.format(
        #             i, from_load_id, to_load_id))
        #         session.commit()

        #     cloned_art = art.clone(load_id=to_load_id)
        #     session.merge(cloned_art)

        session.commit()

        return to_load_id, from_date
