from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from .base_model import Base
import uuid
from sqlalchemy.orm import relationship
from dataclasses import dataclass
from typing import List

@dataclass
class Theme(Base):

    __tablename__ = 'Themes'
    __table_args__ = {'schema':'TE'}

    id: int
    name: str
    theme_words: List[str]

    id = Column('ThemeId', Integer, primary_key=True, autoincrement=True)
    article_load_id = Column('ArticleLoadId', UUID(as_uuid=True), primary_key=True, nullable=False)
    name = Column('ThemeName', String, primary_key=True, autoincrement=True)
    theme_words = Column('ThemeWords', ARRAY(String))
    articles = relationship("ThemeArticleLink", backref = "theme")

    def __init__(self, id, name, article_load_id, theme_words):
        self.id = id
        self.name = name
        self.article_load_id = article_load_id
        self.theme_words = theme_words