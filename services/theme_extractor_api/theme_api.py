from flask import Flask, request, jsonify
from flask_restplus import Resource, Api

from .root_api import emerging_themes_ns as api
from .theme_base import ThemeBase

@api.route('/themes/<string:theme_id>')
class Theme(ThemeBase, Resource):

    def __init__(self, theme_id: str):
        super().__init__()
    
    def get(self, theme_id):
        
        theme =  self.get_theme_information_from_db([theme_id])

        return jsonify(theme[0])
