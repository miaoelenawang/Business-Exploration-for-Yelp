
# coding: utf-8

# In[9]:

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator


# In[113]:
from get_single_page import * # import function which is to extract single page's content
import pandas as pd
import requests
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
# [basic_info('san jose, CA')] + [basic_info('davis, CA')]


import lxml.html as lx

# In[412]:
def parse_html(search_term, search_loc, start_num = '0'):
    urlbase = 'https://www.yelp.com/search'
    dataparams = {'find_desc':search_term, 'l':search_loc, 'start':start_num }
    yelp_req = requests.get(urlbase, params = dataparams)
    yelp_html = yelp_req.text
    html = lx.fromstring(yelp_html)
    return html

def search_num_pages(html):
    num_p = html.xpath('//div[@class="search-pagination"]/div/div/div[@class="page-of-pages arrange_unit arrange_unit--fill"]')
    num_pages = num_p[0].text_content().strip().split(' ')[-1]
    return num_pages

def areas_one_loc(search_term, search_loc, loc_state):
    urlbase = 'https://www.yelp.com/search'
    dataparams = {'find_desc':search_term, 'find_loc':search_loc}
    yelp_req = requests.get(urlbase, params = dataparams)
    yelp_html = yelp_req.text
    html = lx.fromstring(yelp_html)
    
    more_areas = html.xpath('//ul[@class="more place-more"]/div[1]/div/div[@class="filter-group"]/ul[@class="column"]/li')
    return ['p:' + loc_state + ':' + search_loc + '::' + place.text_content().strip().replace(' ', '_') for place in more_areas]

def business_info(html, search_loc):
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
   
        one_business = {'title':title, 'id':one_id,'url':url, 'rating':rating, 'review':review, 'price':price, 'tag':tag, 'area': search_loc}
        pages = extract_single_page(url)
        one_business.update(pages)
        many_business += [one_business]
    return many_business    


def business_many_pages(search_term, search_loc, loc_state):
    more_areas = areas_one_loc(search_term, search_loc, loc_state)
    
    areas_business = []
    for area in more_areas:
        html = parse_html(search_term, area)
        num_pages = search_num_pages(html)
        
        one_area_business = business_info(html, area)
        for page in xrange(1, int(num_pages)):
            start_num = page * 10
            html = parse_html(search_term, area, str(start_num))
            one_area_business += business_info(html, area)
        
        areas_business += one_area_business
    return areas_business



