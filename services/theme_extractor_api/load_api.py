from flask import Flask, request, jsonify
from flask_restplus import Resource, Api, fields

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import extract
from sqlalchemy import func, desc

from services.theme_extractor.base_job import BaseJob
from services.libs.data_model.article import Article
from services.libs.data_model.article_load import ArticleLoad
from services.libs.data_model.processed_article import ProcessedArticle
from services.libs.data_model.theme import Theme
from services.libs.data_model.theme_article_link import ThemeArticleLink

from .root_api import article_load_ns as api
from .api_models import article_load_field


@api.route('/article-load')
class LoadApi(Resource, BaseJob):

    @api.marshal_with(article_load_field)
    def get(self):
        load = self.get_latest_article_load()

        return {
            "id": load.id,
            "startTime": load.start_time
        }
