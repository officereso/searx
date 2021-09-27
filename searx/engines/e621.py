"""
 DuckDuckGo (Images)

 @website     https://duckduckgo.com/
 @provide-api yes (https://duckduckgo.com/api),
              but images are not supported

 @using-api   no
 @results     JSON (site requires js to get images)
 @stable      no (JSON can change)
 @parse       url, title, img_src

 @todo        avoid extra request
"""

from json import loads
from urllib.parse import urlencode
from searx.exceptions import SearxEngineAPIException
from searx.network import get

# engine dependent config
categories = ['images']
paging = True
language_support = True
safesearch = True

# search-url
base_url = 'https://e621.net/'
search_string = 'posts.json?{tags}+{rating}&{page}&limit=100'

# run query in site to get vqd number needed for requesting images
# TODO: find a way to get this number without an extra request (is it a hash of the query?)

# do search-request
def request(query, params):
    # to avoid running actual external requests when testing
    rating = ''
    if params['safesearch'] == 1:
        rating = '-rating%3Ae'
    elif params['safesearch'] == 2:
        rating = 'rating%3As'
    
    search_path = search_string.format(
            tags=urlencode({'tags': query}),
            rating=rating,
            page=urlencode({'page': str(params['pageno'])}))


    params['url'] = base_url+search_path

    return params


# get response from search-request
def response(resp):
    results = []


    content = resp.text
    res_json = loads(content)


    # parse results
    for result in res_json['posts']:
        title = str(result['id'])+' : '+result['description']
        url = base_url+'/posts/'+str(result['id'])
        thumbnail = result['preview']['url']
        image = result['file']['url']
        
        if thumbnail == None:
            continue
        if image == None:
            continue

        # append result
        results.append({'template': 'images.html',
                        'title': title,
                        'content': '',
                        'thumbnail_src': thumbnail,
                        'img_src': image,
                        'url': url})

    return results
