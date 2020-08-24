from .base_job import BaseJob
from services.data_extractor.guardian_connector import GuardianConnector

from .logger import logger
from .article_preprocess_job import ArticlePreprocessJob
from .wv_model_job import WVModelJob
from .cluster_job import ClusterJob

class ThemeExtractor(BaseJob):

    def __init__(self):
        super().__init__();

    
    def start_fresh_run(self):
        
        logger.info('Starting full refresh of themes DB.')

        logger.info('Step #1 - loading fresh bulk load of guardian articles')
        guardian_connector = GuardianConnector();
        load_id = guardian_connector.bulk_load_guardian_articles();
        logger.info('Step #1 complete - load id {}'.format(load_id))

        logger.info('Step #2 - preprocess articles')
        article_preprocess_job = ArticlePreprocessJob();
        article_preprocess_job.preprocess_latest_articles();
        logger.info('Step #2 - complete')
        
        logger.info('Step #3 - building Doc2Vec model')
        wv_model_job = WVModelJob();
        model = wv_model_job.create_model_for_run_id(load_id);
        logger.info('Step #3 - complete')

        logger.info('Step #4 - create clusters (themes)')
        cluster_job = ClusterJob(model, load_id);
        cluster_job.get_clusters()
        logger.info('Step #4 - complete')

        logger.info('Full refresh of themes DB complete!')
