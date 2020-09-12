from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .base_model import Base
import uuid

class Article(Base):
    __tablename__ = 'Articles'
    __table_args__ = {'schema':'DE'}


    id = Column('Id', String, primary_key=True)
    body = Column('Body', String)
    title = Column('Title', String)
    source_tag = Column('SourceTag', String)
    publish_date = Column('PublishDate', DateTime)
    article_load_id = Column('ArticleLoadId', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    def __init__(self, id, body, title, source_tag, publish_date, article_load_id):
        self.id = id
        self.body = body
        self.title = title
        self.source_tag = source_tag
        self.publish_date = publish_date
        self.article_load_id = article_load_id

    def clone(self, load_id = None):

        load_id = load_id if load_id is not None else self.article_load_id;
        return Article(self.id, self.body, self.title, self.source_tag, self.publish_date, load_id)