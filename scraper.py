#!/usr/bin/python

import sys
import requests
import json
import re
from bs4 import BeautifulSoup

# https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure
retry_strategy = requests.packages.urllib3.util.retry.Retry(
    total=10,
    status_forcelist=[403],
    allowed_methods=["GET", "POST"],
    backoff_factor=2
)

adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)
username = sys.argv[1]

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': f'https://cheftap.com/members/{username}/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'cookie': sys.argv[2]
}

data = {
    'cheftap_recipes_search_form': '06b342cf21',
    '_wp_http_referer:': f'/members/{username}/',
    'sort-order': 'new',
    'search-text': ''
}

# Parse optgroup containing the locations
i = 1
# make sure file is empty
open("urls.txt", 'w').close()

while(True):
    data['paged'] = i
    content = http.post(f'https://cheftap.com/members/{username}/', headers=headers, data=data)
    soup = BeautifulSoup(content.text, 'html.parser')

    # get total pages
    span_pages = soup.find('div', class_='list-footer').find('span').text
    pages = int(re.findall(r'Page [0-9]* of ([0-9]*)', span_pages)[0])

    # get recipes
    recipes = soup.find_all('div', class_='post-id')
    for x in recipes:
        recipe = http.get(x.contents[1].get('href'), headers=headers)
        jsonRecipe = re.findall(r'var jsonRecipe =(.*);', recipe.text)

        url = json.loads(jsonRecipe[0])['sourceURL']
        if not url:
            print(f"error getting the source from {x.contents[1].get('href')}")
            continue

        with open("urls.txt", "a") as f:
            f.write(url + '\n')

    i += 1
    if(i > pages):
        break
