from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.dialects.postgresql import UUID

from services.libs.data_model.base_model import Base

import uuid
import os
import base64

class WVModel(Base):
    __tablename__ = 'WVModel'
    __table_args__ = {'schema':'TE'}


    article_load_id = Column('ArticleLoadId', UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    file_name = Column('FileName', String, primary_key=True)
    file_content = Column('FileContent', LargeBinary)
    
    def __init__(self, article_load_id, file_name, file_content):
        self.file_name = file_name
        self.article_load_id = article_load_id
        self.file_content = file_content
