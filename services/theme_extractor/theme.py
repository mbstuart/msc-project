from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from base_model import Base
import uuid

class Theme(Base):

    __tablename__ = 'Themes'
    __table_args__ = {'schema':'TE'}


    id = Column('ThemeId', Integer, primary_key=True, autoincrement=True)
    article_load_id = Column('ArticleLoadId', UUID(as_uuid=True), primary_key=True, nullable=False)
    name = Column('ThemeName', String, primary_key=True, autoincrement=True)
    theme_words = Column('ThemeWords', ARRAY(String))

    def __init__(self, id, name, article_load_id, theme_words):
        self.id = id
        self.name = name
        self.article_load_id = article_load_id
        self.theme_words = theme_words