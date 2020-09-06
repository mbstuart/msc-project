from flask import Flask, request, jsonify
from flask_restplus import Resource, Api

from .root_api import data_loader_ns as api
from .theme_base import ThemeBase

from services.theme_extractor.theme_extractor import ThemeExtractor

@api.route('/data-load')
@api.param('stage')
@api.param('load-id')
@api.param('max-pages')
class DataLoader(Resource):

    def get(self):
        
        theme_extractor = ThemeExtractor()

        from_stage = 0

        load_id = None;

        if 'stage' in request.args:
            from_stage = int(request.args['stage'])

        if 'load-id' in request.args:
            load_id = request.args['load-id']

        max_pages = None;

        if 'max-pages' in request.args:
            max_pages = request.args['max-pages']


        theme_extractor.start_fresh_run(from_stage, load_id, max_pages)

        return jsonify({
            'success': True
        })
