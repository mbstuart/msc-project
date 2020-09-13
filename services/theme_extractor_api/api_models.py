from .root_api import api
from flask_restplus import fields

theme_field = api.model('Theme', {
    'id': fields.Integer(description='The id of the theme', required=True),
    'name': fields.String(description='The name of the theme', required=True),
})

article_field = api.model('Article', {
    'id': fields.String(description='The id of the document', required=True),
    'title': fields.String(description='The title (headline) of the document'),
    'publishDate': fields.DateTime(description='The publication date of the document'),
    'theme': fields.Nested(theme_field)
})

articles_field = api.model('Articles', {
    'articles': fields.List(fields.Nested(article_field))
})

article_load_field = api.model('ArticleLoad', {
    'id': fields.String(description='The id of the article load', required=True),
    'startTime': fields.DateTime(description='The start name of the load', required=True),
})

emerging_theme_field = api.model('EmergingTheme', {
    'id': fields.String(description='The id of the theme', required=True),
    'name': fields.String(description='The name of the theme', required=True),
    'articles': fields.List(fields.Nested(article_field)),
    'keywords': fields.List(fields.String(description='The articles associated with the theme')),
    'articles_published_in_period': fields.Integer(description='The articles associated in the period of the theme'),
    'total_articles_published': fields.Integer(description='The total number of articles associated with the theme'),
})

emerging_themes_field = api.model('EmergingThemes', {
    'themes': fields.List(fields.Nested(emerging_theme_field))
})
