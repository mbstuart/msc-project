from bs4 import BeautifulSoup
from datetime import datetime

from .guardian_content import Content
from .article_loader import ArticleLoader

import time
import json
from math import sqrt, floor, ceil

class GuardianConnector:

    apikey = "2837a5d9-315a-4dd7-a769-81b60c8be2f6"

    '''
    This method loads a history of guardian articles, and produces a new load id 
    '''
    def bulk_load_guardian_articles(self, max_pages=800):

        loader = ArticleLoader()

        load_session_id = loader.create_load_session()

        self.__load_articles(load_session_id, loader, max_pages=max_pages)
        
        return load_session_id;

    def update_guardian_articles(self, copy_load_id: str):

        loader = ArticleLoader()

        load_session_id, from_date = loader.copy_load_session(copy_load_id)

        return self.__load_articles(load_session_id, loader, from_date)

        
    def __load_articles(self, load_session_id, loader: ArticleLoader, from_date=None, max_pages=800):
        page = 1
        virtual_page = page
        date_indent = None
        all_articles = []
        errors_in_a_row = 0
        bundle_size = 1 ##ceil(sqrt(max_pages))

        last_time = None

        stop = False;

        while(page < max_pages and errors_in_a_row < 5 and not stop):
            
            try:  
                all_articles += self.get_results(virtual_page, date_indent)
                errors_in_a_row = 0
            except:
                time.sleep(5)
                errors_in_a_row += 1
                virtual_page = 0
                date_indent = datetime.strptime(last_time, "%Y-%m-%dT%H:%M:%S%z").strftime('%Y-%m-%d')
                
            if len(all_articles) > 0:
                last_time = all_articles[-1]['publish_date']
                if from_date is not None and last_time < from_date:
                    stop = True;

            
            if page % bundle_size == 0:
 
                loader.insert_articles(all_articles, load_session_id);

                all_articles = []


            page += 1

            virtual_page += 1

        return load_session_id;

    def get_results(self, page=1, date_indent=None):
        url = "https://content.guardianapis.com/search?tag={}&page={}&type=article&page-size={}".format("type/article,tone/news", page, 200)
        if date_indent != None:
            url = "{}&to-date={}".format(url, date_indent)
        content = Content(api=self.apikey, url=url)

        # gets raw_response
        raw_content = content.get_request_response()

        raw_content.json()
        # get all results of a page
        json_content = content.get_content_response()
        all_results = content.get_results(json_content)

        html_stripped_results = []

        for res in all_results:
            body = (res['fields']['body'])
            headline = res['webTitle']

            if len(body) > 100:
                html_stripped_results.append({
                    'body': body,
                    'source_tag': res['sectionId'],
                    'title': headline,
                    'publish_date': res['webPublicationDate'],
                    'id': res['id']
                })
        

        return html_stripped_results



