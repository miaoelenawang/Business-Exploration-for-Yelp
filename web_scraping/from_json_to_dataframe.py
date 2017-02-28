# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 06:32:51 2017

@author: kylin
"""

from save_load_dict import *
import re
import Pandas as pd


def clean_tag(tag):
    try:
        new_tag = "".join(tag.split())
    except:
        #possible NaN and none
        new_tag = tag
    return(new_tag)
        

def clean_review(review):
    try:
        new_review = re.sub(" reviews","",review)
    except:
        new_review = review
    return(new_review)

def clean_rating(rating):
    try:
        new_rating= float(re.sub("[:A-z:]","",rating).strip())
    except:
        new_rating= rating
    return(new_rating)

def clean_price(price,price_dict):
    # if it contains any other string than "$"
    try:
       new_price = price_dict[price]
    except:
       new_price = price
    return(new_price)
    

def clean_area(area):
    try:
        new_area = " ".join([ii for ii in area.split(":") if ii not in ['p',""]])
    except:
        new_area = area
    return(new_area)

def bool_value(val,bool_dict):
    try:
        new_val = bool_dict[val]
    except:
        new_val = val
    return(new_val)
        


def json_to_dataframe(json_file):
    price_dict = {"$":1,"$$":2,"$$$":3,"$$$$":4}
    #bool_dict = {"Yes":1,"No":0}
    # load the data as json
    data = reload_dic(json_file)
    for ii in data:
        new_tag = clean_tag(ii['tag'])
        new_review = clean_review(ii['review'])
        new_rate = clean_rating(ii['rating'])
        new_price = clean_price(ii['price'],price_dict)
        new_area = clean_area(ii['area'])
        ii.update({'tag':new_tag,
               'review':new_review,
               'rating':new_rate,
               'price':new_price,
               'area':new_area
               })
    data = pd.DataFrame(data)
    more_info = pd.DataFrame([ii for ii in data['more information']])
    newdata = pd.concat((data,more_info),axis = 2)
    newdata = newdata.drop('more information', 1)
    return(newdata)
print(json_to_dataframe("data_san_joes_one_page.txt"))