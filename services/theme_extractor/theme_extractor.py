from .base_job import BaseJob
from services.data_extractor.guardian_connector import GuardianConnector

from services.libs.data_model import ArticleLoad

from services.libs.utils import logger
from services.theme_extractor.preprocessing import ArticlePreprocessJob
from services.theme_extractor.wv_model import WVModelJob
from services.theme_extractor.clustering import ClusterJob
from services.theme_extractor.keyword_extraction import KeywordExtractionJob

from typing import List

from sqlalchemy.orm import Session


class ThemeExtractor(BaseJob):

    def __init__(self):
        super().__init__()

    def start_fresh_run(self, from_stage=0, load_id=None, max_pages=None):

        if from_stage == 0:
            logger.info('Starting full refresh of themes DB.')
        else:
            if load_id is None:
                raise ValueError(
                    'load_id was none, must be specified if running from a stage')
            logger.info('Starting refresh of themes DB from stage #{} for load_id {}.'.format(
                from_stage, load_id))

        if from_stage < 2:
            logger.info(
                'Step #1 - loading fresh bulk load of guardian articles')
            load_id = self.__get_articles(max_pages)
            logger.info('Step #1 complete - load id {}'.format(load_id))

        if from_stage < 3:
            logger.info('Step #2 - preprocess articles')
            self.__preprocess_articles(load_id)
            logger.info('Step #2 - complete')

        model = None

        if from_stage < 4:
            logger.info('Step #3 - building Doc2Vec model')
            model = self.__create_wv_model(load_id)
            logger.info('Step #3 - complete')

        mapping: List[int] = None

        if from_stage < 5:

            if model is None:
                model = self.__load_wv_model(load_id)

            logger.info('Step #4 - create clusters (themes)')
            mapping = self.__create_themes(load_id, model, True)
            logger.info('Step #4 - complete')

        if from_stage < 6:
            logger.info('Step #5 - extracting theme keywords')
            self.__get_theme_keywords(load_id, model)
            logger.info('Step #5 - extracting theme keywords complete')
        logger.info('Full refresh of themes DB complete!')

        self.__activate_run(load_id)

    def update_run(self, from_load_id):

        logger.info('Starting update on {}'.format(from_load_id))

        logger.info('Step #1 - loading fresh bulk load of guardian articles')
        load_id = self.__update_articles(from_load_id)
        print(load_id)
        logger.info('Step #1 complete - load id {}'.format(load_id))

        logger.info('Step #2 - preprocess articles')
        self.__preprocess_articles_update(
            from_load_id, load_id)
        logger.info('Step #2 - complete')

        logger.info('Step #3 - building Doc2Vec model')
        model = self.__create_wv_model(load_id)
        logger.info('Step #3 - complete')

        logger.info('Step #4 - create clusters (themes)')
        self.__create_themes(load_id, model, True)
        logger.info('Step #4 - complete')

        logger.info('Step #5 - extracting theme keywords')
        self.__get_theme_keywords(load_id, model)
        logger.info('Step #5 - extracting theme keywords complete')

        logger.info('Full refresh of themes DB complete!')

        self.__activate_run(load_id)

    def update_latest(self):
        load_id = self.get_latest_article_load().id

        return self.update_run(load_id)

    def __get_articles(self, max_pages=None):
        guardian_connector = GuardianConnector()
        max_pages = 800 if max_pages is None else max_pages
        load_id = guardian_connector.bulk_load_guardian_articles(max_pages)
        return load_id

    def __update_articles(self, copy_load_id):
        guardian_connector = GuardianConnector()
        load_id = guardian_connector.update_guardian_articles(copy_load_id)
        return load_id

    def __preprocess_articles_update(self, from_load_id, to_load_id):
        article_preprocess_job = ArticlePreprocessJob()
        return article_preprocess_job.preprocess_articles_update(
            to_load_id, from_load_id)

    def __preprocess_articles(self, load_id):
        article_preprocess_job = ArticlePreprocessJob()
        article_preprocess_job.preprocess_articles_for_load(load_id)

    def __create_wv_model(self, load_id):
        wv_model_job = WVModelJob()
        model = wv_model_job.create_model_for_run_id(load_id)
        return model

    def __load_wv_model(self, load_id):
        wv_model_job = WVModelJob()
        model = wv_model_job.get_model_from_disk(load_id)
        return model

    def __create_themes(self, load_id, model, from_scratch=False):
        cluster_job = ClusterJob(model, load_id)
        return cluster_job.get_clusters(from_scratch=from_scratch)

    def __get_theme_keywords(self, load_id, model):
        kej = KeywordExtractionJob()
        kej.extract_keywords_from_labels(load_id, model)

    def __activate_run(self, load_id):
        sess: Session = self.get_session()

        load: ArticleLoad = sess.query(ArticleLoad).filter(
            ArticleLoad.id == load_id).first()

        load.active = True

        sess.commit()
