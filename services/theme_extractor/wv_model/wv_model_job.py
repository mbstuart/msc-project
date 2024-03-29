from services.libs.data_model import ProcessedArticle


from .wv_model_builder import WVModelBuilder

from typing import List
from uuid import UUID, uuid4
from services.theme_extractor  .base_job import BaseJob
from sqlalchemy.orm import Session
from gensim.models import Doc2Vec
import os


class WVModelJob(BaseJob):

    __MODEL_FOLDER = 'models'

    def __init__(self):

        super().__init__()

        self.wv_model_builder = WVModelBuilder()

        if not(os.path.isdir(self.__MODEL_FOLDER)):
            os.mkdir(self.__MODEL_FOLDER)
        # Something
        #

    def create_model_for_latest_run(self) -> Doc2Vec:
        load_id = self.get_latest_article_load().id
        return self.create_model_for_run_id(load_id)

    def create_model_for_run_id(self, load_id: UUID) -> Doc2Vec:
        articles = self.__get_processed_articles_for_run_id(load_id)
        model = self.create_wv_model_for_processed_articles(articles)
        self.__persist_model(model, load_id)
        return model

    def update_model_for_run_id(self, new_articles: List[ProcessedArticle], old_load_id: UUID, load_id: UUID) -> Doc2Vec:
        old_model = self.get_model_from_disk(old_load_id)

        model = self.update_wv_model_for_processed_articles(
            old_model, new_articles)
        self.__persist_model(model, load_id)
        return model

    def get_model_from_disk(self, load_id: UUID) -> Doc2Vec:
        model_dir = "{}/{}".format(self.__MODEL_FOLDER, load_id)
        model = Doc2Vec.load(os.path.join(model_dir, "doc.model"))
        return model

    def create_wv_model_for_processed_articles(self, processed_articles: List[ProcessedArticle]):
        model = self.wv_model_builder.build_wv_model(processed_articles)
        return model

    def update_wv_model_for_processed_articles(self, old_model: Doc2Vec, processed_articles: List[ProcessedArticle]):
        model = self.wv_model_builder.update_wv_model(
            old_model, processed_articles)
        return model

    def __get_processed_articles_for_run_id(self, load_id: UUID) -> List[ProcessedArticle]:
        session: Session = self.get_session()
        query = session.query(ProcessedArticle).filter_by(
            article_load_id=load_id)
        articles = query.all()
        return articles

    def __persist_model(self, model: Doc2Vec, load_id: UUID):
        dir_name = "{}/{}".format(self.__MODEL_FOLDER, load_id)
        os.mkdir(dir_name)
        model.save("{}/doc.model".format(dir_name))
