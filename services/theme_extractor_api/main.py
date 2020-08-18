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

    theme =  ete.get_emerging_themes()



    return jsonify({
        'themes': theme
        })

app.run()