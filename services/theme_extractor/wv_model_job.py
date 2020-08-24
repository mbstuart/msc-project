from services.libs.data_model.processed_article import ProcessedArticle
from services.libs.data_model.wv_model import WVModel


from .wv_model_builder import WVModelBuilder

from typing import List 
from uuid import UUID, uuid4
from .base_job import BaseJob
from sqlalchemy.orm import Session
from gensim.models import Doc2Vec
import os 
class WVModelJob(BaseJob):

    def __init__(self):
        
        super().__init__()

        self.wv_model_builder = WVModelBuilder()

        ##Something
        # 

    def create_model_for_latest_run(self) -> Doc2Vec:
        load_id = self.get_latest_article_load().id
        return self.create_model_for_run_id(load_id)

    def create_model_for_run_id(self, load_id: UUID) -> Doc2Vec:
        articles = self.__get_processed_articles_for_run_id(load_id)
        model = self.create_wv_model_for_processed_articles(articles)
        self.__persist_model(model, load_id)
        return model;

    def get_model_from_disk(self, load_id: UUID) -> Doc2Vec:
        model_dir = "models/{}".format(load_id);
        model = Doc2Vec.load(os.path.join(model_dir, "doc.model"))
        return model;

    def create_wv_model_for_processed_articles(self, processed_articles: List[ProcessedArticle]):
        model = self.wv_model_builder.build_wv_model(processed_articles);
        return model

    def __get_processed_articles_for_run_id(self, load_id: UUID) -> List[ProcessedArticle]:
        session: Session = self.get_session();
        query = session.query(ProcessedArticle).filter_by(article_load_id = load_id)
        articles = query.all();
        return articles

    def __persist_model(self, model: Doc2Vec, load_id: UUID):
        dir_name = "models/{}".format(load_id)
        os.mkdir(dir_name)
        model.save("{}/doc.model".format(dir_name))
  