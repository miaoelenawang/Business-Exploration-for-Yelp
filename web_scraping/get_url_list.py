
# coding: utf-8

# In[9]:

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator


# In[113]:

import pandas as pd
import numpy as np
import requests_cache
requests_cache.install_cache('yelp_cache')


# In[3]:

auth = Oauth1Authenticator(
    consumer_key = 'your_key',
    consumer_secret = 'your_secret',
    token = 'your token',
    token_secret = 'your token secret'
)

client = Client(auth)


# In[87]:

def basic_info(search_loc):
    params = {
        'term': 'food'
        #'lang': 'en'
    }
    response = client.search(search_loc, **params)
    
    total_business = response.total
    center_lat = response.region.center.latitude
    center_long = response.region.center.longitude
    span_lat = response.region.span.latitude_delta
    span_long = response.region.span.longitude_delta
    return {'search_location': search_loc, 'total_business': total_business, 'center_latitude': center_lat,
           'center_longitude': center_long, 'span_latitude': span_lat, 'span_longitude': span_long}


# In[88]:
#test the function
[basic_info('san jose, CA')] + [basic_info('davis, CA')]


import lxml.html as lx

# In[412]:

def business_info(search_term, search_loc, start_num):
    urlbase = 'https://www.yelp.com/search'
    dataparams = {'find_desc':search_term, 'find_loc':search_loc, 'start':start_num }
    yelp_req = requests.get(urlbase, params = dataparams)
    yelp_html = yelp_req.text
    html = lx.fromstring(yelp_html)
    
    research_results = html.xpath('//div[@class="search-results-content"]/ul/li[@class="regular-search-result"]')
    
    many_business = []
    for i in xrange(0, len(research_results)):
        t = research_results[i].xpath('div/div[1]/div[1]/div/div[@class="media-story"]/h3/span/a/span')
        u = research_results[i].xpath('div/div[1]/div[1]/div/div[@class="media-story"]/h3/span/a')
        r = research_results[i].xpath('div/div[1]/div[1]/div/div[@class="media-story"]/div/div')
        re = research_results[i].xpath('div/div[1]/div[1]/div/div[@class="media-story"]/div/span[@class="review-count rating-qualifier"]')
        p = research_results[i].xpath('div/div[1]/div[1]/div/div[2]/div[2]/span/span[@class="business-attribute price-range"]')
        tags = research_results[i].xpath('div/div[1]/div[1]/div/div[2]/div[2]/span[@class="category-str-list"]')
    
        title = t[0].text_content()
    
        baseurl = "https://www.yelp.com"
        url = baseurl + u[0].get('href')

        the_id = u[0].get('href').split('/')[-1]
        one_id = the_id.split('?')[0]

        if len(r) == 0:
            rating = None
        else:
            rating = r[0].get("title")

        if len(re) == 0:
            review = None
        else:
            review = re[0].text_content().strip()

        if len(p) == 0:
            price = None
        else:
            price = p[0].text_content().strip()

        if len(tags) == 0:
            tag = None
        else:
            tag = tags[0].text_content().strip()
   
        one_business = {'title':title, 'id':one_id,'url':url, 'rating':rating, 'review':review, 'price':price, 'tag':tag}
        many_business += [one_business]
    return many_business    


# In[415]:
#test the function
business_info('food', 'san jose, CA', str(1000))

# In[410]:
max_page = 100
business_pages = []
for page in xrange(0, max_page):
    start_num = page * 10
    business_pages = business_pages + business_info('food', 'san jose, CA', str(start_num))
business_pages


# In[422]:
business_pages_df = pd.DataFrame(business_pages)
business_pages_df

