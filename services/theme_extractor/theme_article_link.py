from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from base_model import Base
import uuid

class ThemeArticleLink(Base):

    __tablename__ = 'ThemeArticleMapping'
    __table_args__ = {'schema':'TE'}

    theme_id = Column(Integer, ForeignKey('Themes.Id'), primary_key=True)
    article_id = Column(String, ForeignKey('ProcessedArticles.Id'), primary_key=True)
    article_load_id = Column(UUID(as_uuid=True), ForeignKey('ProcessedArticles.ArticleLoadId'), primary_key=True)
    
    child = relationship("ProcessedArticle")

    def __init__(self, id, article_id, article_load_id):
        self.id = id
        self.article_id = article_id
        self.article_load_id = article_load_id
