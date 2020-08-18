#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, jsonify, request
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, desc
from services.libs.data_model.processed_article import ProcessedArticle
from typing import List
from .emerging_theme_extractor import EmergingThemeExtractor
import jsonpickle

app = Flask(__name__)
@app.route('/documents')
def documents():

    db_string = "postgres://theme-extractor:tepassword@localhost:5432/theme-extractor"

    engine = create_engine(db_string)
    sm = sessionmaker()
    sm.configure(bind=engine)

    session: Session = sm();

    page_size = 10
    if 'page_size' in request.args:
        page_size = int(request.args['page_size'])

    q =  session.query(ProcessedArticle).limit(page_size)

    documents: List[ProcessedArticle] = q.all()

    results = [
            {
                "id": doc.id,
                "words": doc.words
            } for doc in documents
    ];

    return jsonify({'documents':results})

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