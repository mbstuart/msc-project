
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import extract
from sqlalchemy import func, desc

from services.theme_extractor.base_job import BaseJob
from services.libs.data_model.article import Article
from services.libs.data_model.article_load import ArticleLoad
from services.libs.data_model.processed_article import ProcessedArticle
from services.libs.data_model.theme import Theme
from services.libs.data_model.theme_article_link import ThemeArticleLink

class ArticleService(BaseJob):

    def __init__(self): 
        super().__init__()
    
    def get_articles(self):

        load_id = self.get_latest_article_load().id;

        session: Session = self.get_session();

        q = session.query(ProcessedArticle).\
            join(Article).\
            filter_by(article_load_id = load_id).\
            order_by(desc(Article.publish_date)).\
            limit(10)

        res =  q.all()

        return res;