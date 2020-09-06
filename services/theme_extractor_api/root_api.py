from flask import Flask
from flask_restplus import Api, Namespace

emerging_themes_ns = Namespace("Emerging Themes",
            path='/api',
           description="Themes data")

articles_ns = Namespace("Articles",
            path='/api',
           description="Articles data")

data_loader_ns = Namespace("Data Loader",
            path='/api',
           description="Data Loader operations")

api = Api(version='1.0', title='Emerging Themes API',
    description='An API for serving the emerging themes content',)

api.add_namespace(emerging_themes_ns)
api.add_namespace(articles_ns)
api.add_namespace(data_loader_ns)