#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, desc
from services.libs.data_model.processed_article import ProcessedArticle
from typing import List
from services.libs.data_model.article import Article

from .emerging_theme_extractor import EmergingThemeExtractor
from .article_service import ArticleService

import jsonpickle

app = Flask(__name__)
CORS(app)
@app.route('/articles')
def documents():

    article_service = ArticleService()

    documents: List[ProcessedArticle] = article_service.get_articles()

    

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

    return jsonify({'articles':results})

@app.route('/emerging-themes')
def emerging_themes():
    ete = EmergingThemeExtractor()

    frequency = 'month'


    if 'frequency' in request.args:
        frequency = request.args['frequency']

    theme =  ete.get_emerging_themes(frequency=frequency)



    return jsonify({
        'themes': theme
        })

@app.route('/themes/<theme_id>')
def get_single_theme(theme_id: str):
    ete = EmergingThemeExtractor()

    # theme_id = request.view_args['theme_id']

    theme =  ete.get_theme([theme_id])

    return jsonify(theme[0])


app.run()