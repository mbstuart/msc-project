#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restplus import Api, Resource, fields

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, desc
from services.libs.data_model.processed_article import ProcessedArticle
from typing import List


from .root_api import api

from .theme_api import Theme
from .emerging_theme_api import EmergingThemes
from .data_loader_api import DataLoader
from .article_api import ArticleApi
from .load_api import LoadApi

import jsonpickle

app = Flask(__name__)
CORS(app)
api.init_app(app)


if __name__ == 'services.theme_extractor_api.main':
    app.run(debug=False, use_reloader=False)
