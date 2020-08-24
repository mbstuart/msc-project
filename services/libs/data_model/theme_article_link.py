from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from .base_model import Base
import uuid

class ThemeArticleLink(Base):

    __tablename__ = 'ThemeArticleMapping'
    __table_args__ = (ForeignKeyConstraint(['ThemeId', 'ArticleLoadId'],
                                           ['TE.Themes.ThemeId', 'TE.Themes.ArticleLoadId']),
                    ForeignKeyConstraint(['ArticleLoadId', 'ArticleId'],
                                           ['TE.ProcessedArticles.ArticleLoadId', 'TE.ProcessedArticles.Id']), {'schema':'TE'});

    theme_id = Column('ThemeId', Integer, primary_key=True,)
    article_id = Column('ArticleId', String, primary_key=True)
    article_load_id = Column('ArticleLoadId', UUID(as_uuid=True), primary_key=True)
    article = relationship('ProcessedArticle', backref = "theme_article_link")

    def __init__(self, theme_id, article_id, article_load_id):
        self.theme_id = int(theme_id)
        self.article_id = article_id
        self.article_load_id = article_load_id
