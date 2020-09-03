from sqlalchemy import Column, Integer, String, DateTime, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from .article import Article
from .base_model import Base
from .theme import Theme
import uuid

class ProcessedArticle(Base):
    __tablename__ = 'ProcessedArticles'
    __table_args__ = (ForeignKeyConstraint(['Id', 'ArticleLoadId'],
                                           ['DE.Articles.Id', 'DE.Articles.ArticleLoadId']),{'schema':'TE'})


    id = Column('Id', String, primary_key=True)
    article_load_id = Column('ArticleLoadId', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    words = Column('Words', ARRAY(String))
    title_words = Column('TitleWords', ARRAY(String))
    article = relationship(Article)

    def __init__(self, id, article_load_id, words, title_words):
        self.id = id
        self.article_load_id = article_load_id
        self.words = words
        self.title_words = title_words;