from guardian_content import Content
from bs4 import BeautifulSoup
from datetime import datetime
from article_loader import ArticleLoader
import time
import json
from math import sqrt, floor, ceil

apikey = "2837a5d9-315a-4dd7-a769-81b60c8be2f6"

def get_results(page=1, date_indent=None):
    url = "https://content.guardianapis.com/search?tag={}&page={}&type=article&page-size={}".format("type/article,tone/news", page, 200)
    if date_indent != None:
        url = "{}&to-date={}".format(url, date_indent)
    content = Content(api=apikey, url=url)

    # gets raw_response
    raw_content = content.get_request_response()
    print("Request Response status code {status}.".format(status=raw_content.status_code))

    if (raw_content.status_code != 200):
        print("Error in request!")
        print(content.get_content_response())
        print(url)

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


page = 1
virtual_page = page
date_indent = None
all_articles = []
errors_in_a_row = 0
max_pages = 800
bundle_size = 1 ##ceil(sqrt(max_pages))
reporting_bundle_size = 40
loader = ArticleLoader()

load_session_id = loader.create_load_session()

last_time = None

while(page < max_pages and errors_in_a_row < 5):
    try:  
        all_articles += get_results(virtual_page, date_indent)
        errors_in_a_row = 0
    except:
        print('error downloading - wait then continue')
        time.sleep(5)
        errors_in_a_row += 1
        virtual_page = 0
        date_indent = datetime.strptime(last_time, "%Y-%m-%dT%H:%M:%S%z").strftime('%Y-%m-%d')
        
    if len(all_articles) > 0:
        last_time = all_articles[-1]['publish_date']

    
    if page % bundle_size == 0:
        to_write = {
            'results': all_articles  
        }

        loader.insert_articles(all_articles, load_session_id);

        all_articles = []


    page += 1
    if page % reporting_bundle_size == 0:
        print('{} articles downloaded!'.format(str(200 * page)))
    virtual_page += 1





# actual response

