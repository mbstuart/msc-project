from guardian_content import Content
from bs4 import BeautifulSoup
import os
# create content
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
 
print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d-%m-%Y-%H-%M")

dir_name = 'data-run-' + dt_string;

print(dir_name)

os.makedirs(dir_name)

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
                'sectionId': res['sectionId'],
                'headline': headline,
                'webPublicationDate': res['webPublicationDate'],
                'id': res['id']
            })
    

    return html_stripped_results
import time
import json
from math import sqrt, floor, ceil

page = 1
virtual_page = page
date_indent = None

all_articles = []
errors_in_a_row = 0
max_pages = 800
bundle_size = ceil(sqrt(max_pages))

print('{:d} pages, each bundled into a JSON file containing {:d} each.'.format(max_pages, bundle_size))

while(page < max_pages and errors_in_a_row < 5):
    try:  
        all_articles += get_results(virtual_page, date_indent)
        errors_in_a_row = 0
    except:
        print('error downloading - wait then continue')
        time.sleep(5)
        errors_in_a_row += 1
        virtual_page = 0
        date_indent = datetime.strptime(all_articles[-1]['webPublicationDate'] , "%Y-%m-%dT%H:%M:%S%z").strftime('%Y-%m-%d')
        
    if page % bundle_size == 0:
        to_write = {
            'results': all_articles  
        }

        with open(dir_name + '/output_news_raw_{:d}.json'.format(int(page / bundle_size)), 'w', encoding='utf-8') as f:
            json.dump(to_write, f, ensure_ascii=False, indent=4)
        
        all_articles = []
    page += 1
    virtual_page += 1





# actual response

