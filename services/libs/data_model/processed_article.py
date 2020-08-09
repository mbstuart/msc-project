from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from base_model import Base
import uuid

class ProcessedArticle(Base):
    __tablename__ = 'ProcessedArticles'
    __table_args__ = {'schema':'TE'}


    id = Column('Id', String, primary_key=True)
    article_load_id = Column('ArticleLoadId', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    words = Column('Words', ARRAY(String))

    def __init__(self, id, article_load_id, words):
        self.id = id
        self.article_load_id = article_load_id
        self.words = words