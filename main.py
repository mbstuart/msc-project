# import services.theme_extractor_api.main
from services.theme_extractor.cluster_job import ClusterJob
from services.theme_extractor.wv_model_job import WVModelJob

wvm = WVModelJob()

al = wvm.get_latest_article_load()

model = wvm.get_model_from_disk(al.id)

cj = ClusterJob(model, al.id)

cj.get_clusters()

