# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 08:47:50 2017

@author: kylin
"""
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from from_json_to_dataframe import *
import math
data1 = pd.read_csv("detroit.csv",sep='\t')
#data1 = json_to_dataframe("detroit_food.txt")
#data1.to_csv("detroit.csv", sep='\t', encoding='utf-8')
data2 = pd.read_csv("sf.csv")
data3 =  pd.read_csv("abq.csv")
#data_ = data3
def trace(data_,city):
  data_ = data_[["price","rating","review"]]
  data_ = data_.replace("None",np.nan).apply(pd.to_numeric).dropna()
  data_['review_scale'] = (data_['review'])/np.std(data_['review'])

  hover_text = []
  for index,row in data_.iterrows():
    hover_text.append(('City:{city}<br>' + 
                'Price:{price}<br>'+
                'Rating:{rating}<br>'+
                'Review:{reviews}<br>').format(city = city,
                                        price = row['price'],
                                        rating = row['rating'],
                                        reviews = row['review']))
  #bubble_size.append(10)
  
  trace0 = go.Scatter(
    x = data_['price'],
    y = data_['rating'],
    mode='markers',
    name = city,
    text = hover_text,
    marker=dict(
        symbol='circle',
        sizemode='diameter',
        sizeref=0.85,
        size=data_['review_scale']*10,
        line=dict(
            width=2
        ),
    )
    )
  return trace0

trace0 = trace(data1,"Detroit")
trace1 = trace(data2,"SanFrancisco")
trace2 = trace(data3,"Albuquerque")



data = [trace0,trace1,trace2]
width= 1000
height = 600
layout = go.Layout(
    title='Price vs Rating',
    titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            ),
    width=width,
    height=height,
    xaxis=dict(
        title='price 1:Inexpensive 2: Moderate 3:Pricey 4:Highend ',
        titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            ),
        gridcolor='rgb(255, 255, 255)',
        range=[0,5],
        showline=True,
        zerolinewidth=1,
        ),
    yaxis=dict(
        title='rating',
        titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            ),
        gridcolor='rgb(255, 255, 255)',
        showline = True,
        
    ),
    legend=dict(
        x=0.9,
        y=1,
        traceorder='normal',
        font=dict(
            family='sans-serif',
            size=15,
            color='#000'
        ),
         ),
      
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='price vs rating14')