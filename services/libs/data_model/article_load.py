from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from base_model import Base
import uuid
from datetime import datetime

class ArticleLoad(Base):
    __tablename__ = 'ArticleLoad'
    __table_args__ = {'schema':'DE'}


    id = Column('Id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    start_time = Column('StartTime', DateTime, default=datetime.now)

