from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
#from get_single_page import * # import function which is to extract single page's content
import pandas as pd
import requests
import numpy as np
import requests_cache
import time
requests_cache.install_cache('yelp_cache_state')


# In[3]:

auth = Oauth1Authenticator(
    consumer_key = '8LA2L-zp1cPUEa_w-fDzuQ', 
    consumer_secret = 'FqzMZU0eazyCy5rhnpIEa9jOknk',
    token = 's4QGIk557xqnG-KvL___4H3JU3Q0pgU_',
    token_secret = 'od_c3ygRuXBf2ECp6laWUlF7oFg'
)

client = Client(auth)


def number_of_res(search_city, search_state):
    params = {
        'term': 'food'
        #'lang': 'en'
    }
    search_loc = search_city + "," + search_state
    response = client.search(search_loc, **params)
    
    total_business = response.total
    
    return {'total_business': total_business, "State":search_state, "City":search_city}
""""
num = []
cities = pd.read_csv('cities.csv')
City = cities["City"]
State = cities["State"]
for i in range(20000, 29868):
    new = number_of_res(City[i],cities["State"][i])
    num.append(new)
    print i
