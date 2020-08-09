
from wv_model_job import WVModelJob
from base_job import BaseJob
from cluster_job import ClusterJob

class ThemeExtractor(BaseJob):

    def get_clusters(self):
        
        load_id = self.get_latest_article_load().id;

        wv_model_job = WVModelJob()

        model = wv_model_job.get_model_from_disk(load_id);

        cluster_job = ClusterJob(model, load_id)

        themes, mapping = cluster_job.get_clusters();

        return themes;

te = ThemeExtractor()

themes = te.get_clusters()

print(themes[:100])