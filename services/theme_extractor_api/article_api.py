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

from .root_api import articles_ns as api
from .api_models import articles_field

@api.route('/articles')
class ArticleApi(Resource, BaseJob):

    
    @api.marshal_with(articles_field)
    def get(self):

        load_id = self.get_latest_article_load().id;

        session: Session = self.get_session();

        q = session.query(ProcessedArticle).\
            join(Article).\
            filter_by(article_load_id = load_id).\
            order_by(desc(Article.publish_date)).\
            limit(10)

        documents =  q.all()

        results = [
            {
                "id": doc.id,
                "title": doc.article.title,
                "publishDate": doc.article.publish_date,
                "theme": {
                    "id": doc.theme_article_link[0].theme.id,
                    "name": doc.theme_article_link[0].theme.name,
                }
            } for doc in documents
        ];

        return {'articles':results}