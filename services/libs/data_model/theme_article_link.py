from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from base_model import Base
import uuid

class ThemeArticleLink(Base):

    __tablename__ = 'ThemeArticleMapping'
    __table_args__ = {'schema':'TE'}

    theme_id = Column('ThemeId', Integer, ForeignKey('TE.Themes.ThemeId'), primary_key=True,)
    article_id = Column('ArticleId', String, ForeignKey('TE.ProcessedArticles.Id'), primary_key=True)
    article_load_id = Column('ArticleLoadId', UUID(as_uuid=True), ForeignKey('TE.ProcessedArticles.ArticleLoadId'), primary_key=True)
    

    def __init__(self, theme_id, article_id, article_load_id):
        self.theme_id = int(theme_id)
        self.article_id = article_id
        self.article_load_id = article_load_id
