import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, date

CACHE_FNAME = "dataall_cache.json"

try:
    cache_file = open(CACHE_FNAME, "r")
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def unique_i(url):
    timestamp = str(date.today())
    print(timestamp)
    return url + timestamp

def get_page_cache():
    url = 'https://www.billboard.com/charts/hot-100'
    unique_ident = unique_i(url)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        page_text = requests.get(url).text
        CACHE_DICTION[unique_ident] = page_text
        fw = open(CACHE_FNAME, "w")
        fw.write(str(CACHE_DICTION))
        fw.close()
        return CACHE_DICTION[unique_ident]

def get_data(page_text):
    soup = BeautifulSoup(page_text, 'html.parser')
    content_div = soup.find('main', class_='page-content').find_all('div', class_ = "chart-row__main-display")
    title_list = []
    for ele in content_div:
        title = ele.find('div', class_='chart-row__container').find('h2', class_ = 'chart-row__song').text
        title_list.append(title)
    return title_list

# page_text = get_page_cache()
# title_list = get_umsi_data(page_text)
# print(title_list)
