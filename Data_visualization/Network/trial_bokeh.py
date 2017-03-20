# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 20:39:29 2017

@author: kylin
"""

''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
import pandas as pd
import numpy as np
from from_json_to_dataframe import *
#from bokeh.sampledata.us_counties import data as counties
from  collections import Counter
from from_json_to_dataframe import *
import plotly
import networkx as nx
import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.graph_objs import *
%matplotlib inline
from save_load_dict import *
import re
# Set up data


#--------------------------------tab 1 for price ------------------------------------------------#
plotly.tools.set_credentials_file(username='Rita0309', api_key='RbV4yPU22tIAXPoofTCD')
# ----------------------------splitting factor plot-------------------------------------------#
# price, reviews and rating splitting by 2 categorical factors
data1 = pd.read_csv("detroit.csv",sep = "\t")
data2 = pd.read_csv("sf.csv")
data3 =  pd.read_csv("abq.csv")
tags_ = reload_dic("tags.json")
tags_.keys()

def tag_df(data):
  tags = reload_dic("tags.json")
#process_tag:
  #data = data1
  data['tag'] = data['tag'].replace(np.nan,"None")
  tag_list = [ii.split(",") for ii in data['tag']]
  color_tag = {};col_val = dict(zip(list(tags.keys()),["red","yellow","green","#00FFFF","#7FFF00","	#FF8C00","	#FF1493","#4169E1","#adff2f"]))
  new_tag = {}
  for key,value in tags.items():
    bool_ = [sum([jj in value for jj in ii]) >0 for ii in tag_list]
    col = [];
    for ii in bool_:
      if ii:
        col.append(col_val[key]);
      else:
        col.append("#708090")
    new_tag.update({key:col})
  new_tag = pd.DataFrame(new_tag)
  return new_tag



def data_to_node_edge(data):
  #data = data1
  idx = data['id']
  connect = data[['id','related0','related1','related2','tag','title']]
  connect = connect.replace(np.nan,"None")
  #pd.concat([connect,new_tag],axis = 1)
  #palette = brewer["Blues"][9]

  con = [];
  # concatenate each id with other restraurant, here order matters
  for ii in range(0,len(idx)-1):
    if connect.iloc[ii,1]!= "None":
      con.append(" ".join(np.sort([connect.iloc[ii,0],connect.iloc[ii,1]])));
    if connect.iloc[ii,2]!= "None":
      con.append(" ".join(np.sort([connect.iloc[ii,0],connect.iloc[ii,2]])));
    if connect.iloc[ii,3]!= "None":
      con.append(" ".join(np.sort([connect.iloc[ii,0],connect.iloc[ii,3]])));
  #print("---1")
  # get unique pairs of connection
  dict_con = list(set(con))
  # got all nodes
  node = []; edge = []
  for ii in dict_con:
    pair = ii.split(" ")
    edge.append(pair)
    for jj in pair:
       node.append(jj)
  node = list(set(node))
  # count the connection of each node 
  node_new = []; edge_new = [];
  for ii in range(len(node)):
    val = 0
    for jj in edge:
      if node[ii] in jj:
          val +=1
    if val > 8:
      for jj in edge:
        if node[ii] in jj:
          edge_new.append((jj[0],jj[1]));
          node_new.append(jj[0])
          node_new.append(jj[1])
          #print(jj[1])
    #get color for each node
  #bool_2 = [ii in list(set(node_new)) for ii in connect['id']]
  #colcon = connect.iloc[bool_2,:]
  return dict({"node":list(set(node_new)),"edge":edge_new,"connect":connect})

 
def scatter_nodes(pos, labels, color, tag,size=10, opacity=0.7):
    # pos is the dict of node positions
    # labels is a list  of labels of len(pos), to be displayed when hovering the mouse over the nodes
    # color is the color for nodes. When it is set as None the Plotly default color is used
    # size is the size of the dots representing the nodes
    #opacity is a value between [0,1] defining the node color opacity
    trace = Scatter(x=[], y=[],  mode='markers', marker=Marker(size=[],color = []),name = tag)
    for key,value in pos.items():
      trace['x'].append(value[0])
      trace['y'].append(value[1])
    trace['marker']['color'] = color
    attrib=dict(text=labels , hoverinfo='text', opacity=opacity) # a dict of Plotly node attributes
    trace=dict(trace, **attrib)# concatenate the dict trace and attrib
    trace['marker']['size']=size
    return trace       
  
def scatter_edges(G, pos, line_color,line_width=1):
    trace = Scatter(x=[], y=[], mode='lines')
    for edge in G.edges():
        trace['x'] += [pos[edge[0]][0],pos[edge[1]][0], None]
        trace['y'] += [pos[edge[0]][1],pos[edge[1]][1], None]  
        trace['hoverinfo']='none'
        trace['line']['width']=line_width
        if line_color is not None: # when it is None a default Plotly color is used
            trace['line']['color']=line_color
    return trace 


def network_trace(data):
  #data= data1
  G=nx.Graph()   
  edge_node = data_to_node_edge(data = data)
  node,edge,connect= edge_node['node'],edge_node['edge'],edge_node['connect']
  
  # decide color
  new_tag = tag_df(data)
  connect = pd.concat([connect,new_tag],axis = 1)
  bool_2 = [ii in node for ii in connect['id']]
  colcon = connect.iloc[bool_2,:]
  node_ = pd.DataFrame({"node":node});
  # obtain order and color for each node
  node_ = node_.merge(node_.merge(colcon, how='left',left_on="node", right_on="id",sort=False))
  node_ = node_[['node','tag','Chinese','Alcohol', 'JanpaneseKorean', 'American', 'South American(Mexican)', 'East Asian', 'Indian', 'Europe', 'Dessert']].replace(np.nan,"#708090")
  G.add_nodes_from(node)
  G.add_edges_from(edge)
  pos1 = nx.spring_layout(G)
  labels =node
  tags = ['Chinese','Alcohol', 'JanpaneseKorean', 'American', 'South American(Mexican)', 'East Asian', 'Indian', 'Europe', 'Dessert']
  trace = [scatter_edges(G, pos1,line_color = "#1a8cff")]
  for tag in tags:
     trace.append(scatter_nodes(pos1, labels=labels,tag = tag, color = node_[tag]))
  return trace

#
tr1 = network_trace(data = data1)
tr2 = network_trace(data = data2)
tr3 = network_trace(data = data3)




"""tag_list = []
for ii in list(Counter(data3['tag']).keys()):
  if ii is None:
    ii = "None";
  for jj in ii.split(","):
          tag_list.append(jj)

dict(Counter(tag_list)).keys()
eu_dessert_tag = {"Europe":
 ['ModernEuropean','French','Fish&Chips', 'Greek','Salvadoran','Tapas/SmallPlates','Belgian','Mediterranean','Spanish','TapasBars','Turkish','Brasseries','Czech','German','Catalan','Basque','Irish','British','Polish','Fondue','IrishPub',
'Portuguese','Hungarian','Sardinian','Tuscan','Italian','Poutineries','Dominican'],
"Desert":
['Bakeries','Desserts','Donuts','IceCream&FrozenYogurt','JuiceBars&Smoothies','CustomCakes','Creperies','Kombucha','BubbleTea','Patisserie','Gelato','Waffles','Cupcakes','ShavedIce','Pretzels',
'Macarons','Waffles']}
from save_load_dic.py import *"""



#np.repeat(False,30)





width=1000
height = 1000
axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title='' 
          )
layout=Layout(title= 'network graph for Detroit',  #
    font= Font(),
    args=['visible', [True, True, True, True, True, True, True, True, True, True]],
    showlegend=True,
    autosize=False,
    width=width,
    height=height,
    xaxis=XAxis(axis),
    yaxis=YAxis(axis),
    legend=dict(
        x=0.9,
        y=1,
        traceorder='normal',
        font=dict(
            family='sans-serif',
            size=12,
            color='#000'
        ),
       ),
    margin=Margin(
        l=40,
        r=40,
        b=85,
        t=100,
        pad=0,
       
    ),
    hovermode='closest',
    plot_bgcolor='#EFECEA', #set background color            
    )
    
"""
layout = Layout(
    title='network graph for cities',
    font= Font(),
    showlegend=True,
    autosize=False,
    width=width,
    height=height,
    xaxis=XAxis(axis),
    yaxis=YAxis(axis),
    hovermode='closest',
    plot_bgcolor='#EFECEA', #set background color   
    updatemenus=list([
        dict(
            x=-0.05,
            y=1,
            yanchor='top',
            buttons=list([
                dict(
                    args=['visible', [True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]],
                    label='Detroit',
                    method='restyle'
                ),
                dict(
                    args=['visible', [ False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False]],
                    label='San Francisco',
                    method='restyle'
                ),
                dict(
                    args=['visible', [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,True, True, True, True, True, True, True, True, True, True,]],
                    label='Albuquerque',
                    method='restyle'
                )
                
            ]),
             
        )
    ]),
)
"""
tr = [tr1,tr2,tr3]
dt = []
for ii in tr:
  for jj in ii:
    dt.append(jj)
    
data_=Data(tr1)

fig = Figure(data=data_, layout=layout)


py.iplot(fig, filename = "Detroit.html")

data2

