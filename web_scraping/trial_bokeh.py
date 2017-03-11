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

# Set up data


#--------------------------------tab 1 for price ------------------------------------------------#
plotly.tools.set_credentials_file(username='uskli', api_key='AwF1GBh7swQ5Cn8LajHT')
# ----------------------------splitting factor plot-------------------------------------------#
# price, reviews and rating splitting by 2 categorical factors




def data_to_node_edge(data):
  #data = json_to_dataframe("detroit_food.txt")
  idx = data['id']
  connect = data[['id','related0','related1','related2','title']]

#palette = brewer["Blues"][9]

  con = [];
  for ii in range(0,len(idx)-1):
    if connect.iloc[ii,1] !=None:
      con.append(" ".join(np.sort([connect.iloc[ii,0],connect.iloc[ii,1]])));
    if connect.iloc[ii,2] !=None:
      con.append(" ".join(np.sort([connect.iloc[ii,0],connect.iloc[ii,2]])));
    if connect.iloc[ii,3] !=None:
      con.append(" ".join(np.sort([connect.iloc[ii,0],connect.iloc[ii,3]])))
  dict_con = dict(Counter(con))
  title_id = connect[['id','title']]

  chord = [];
  for key,value in dict_con.items():
     ids = key.split(" ")
     ids.append(value)
     chord.append(ids)
  chord = pd.DataFrame(chord)
  chord = chord.drop_duplicates()
  chord = chord.rename(columns = {0:"source",1:"target",2:"value"})

# only need nodes with connection > 3
  node1 = [key for key,value in dict(Counter(chord['source'])).items() if value > 3]
  node2 = [key for key,value in dict(Counter(chord['target'])).items() if value > 3]
  filter_=[chord['source'][ii] in node1 or chord['target'][ii] in node2  for ii in range(chord.shape[0])]
    
    

  chord = chord.iloc[filter_]
  node = list(chord['source'])
  for ii in chord['target']:
     node.append(ii)
  node = list(dict(Counter(node)).keys())
  edge = list(zip(chord['source'],chord['target']))
  return dict({"node":node,"edge":edge})

 
def scatter_nodes(pos, labels, color, size, opacity):
    # pos is the dict of node positions
    # labels is a list  of labels of len(pos), to be displayed when hovering the mouse over the nodes
    # color is the color for nodes. When it is set as None the Plotly default color is used
    # size is the size of the dots representing the nodes
    #opacity is a value between [0,1] defining the node color opacity
    trace = Scatter(x=[], y=[],  mode='markers', marker=Marker(size=[],color = [],opacity = []))
    for key,value in pos.items():
        trace['x'].append(value[0])
        trace['y'].append(value[1])
    attrib=dict(name='', text=labels , hoverinfo='text', opacity=opacity) # a dict of Plotly node attributes
    trace=dict(trace, **attrib)# concatenate the dict trace and attrib
    trace['marker']['size']=size
    trace['marker']['color'] = color
    trace['opacity'] = opacity
    return trace       
  
def scatter_edges(G, pos, line_color, line_width=1):
    trace = Scatter(x=[], y=[], mode='lines')
    for edge in G.edges():
        trace['x'] += [pos[edge[0]][0],pos[edge[1]][0], None]
        trace['y'] += [pos[edge[0]][1],pos[edge[1]][1], None]  
        trace['hoverinfo']='none'
        trace['line']['width']=line_width
        if line_color is not None: # when it is None a default Plotly color is used
            trace['line']['color']=line_color
    return trace 

data1 = json_to_dataframe("detroit_food.txt")
data2 = pd.read_csv("sf.csv")
data3 =  pd.read_csv("abq.csv")
def network_trace(data):
  G=nx.Graph()   
  edge_node = data_to_node_edge(data)
  node,edge = edge_node['node'],edge_node['edge']
  G.add_nodes_from(node)
  G.add_edges_from(edge)
  pos1=nx.spring_layout(G)
  labels =node#[re.sub("-"," ",ii) for ii in [re.sub("detroit-?[0-9]?","",ii) for ii in node]]
  trace1=scatter_edges(G, pos1, line_color = "#ff661a")
  trace2=scatter_nodes(pos1, labels=labels,color = "#6666ff",size = 10,opacity = 0.7)
  return [trace1,trace2]

tr1 = network_trace(data1)
tr2 = network_trace(data2)
tr3 = network_trace(data3)
trace1 = tr1[0]
trace2 = tr1[1]
trace3 = tr2[0]
trace4 = tr2[1]
trace5 = tr3[0]
trace6 = tr3[1]















width=1000
height = 1000
axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title='' 
          )
"""layout=Layout(title= 'network graph for cities',  #
    font= Font(),
    showlegend=False,
    autosize=False,
    width=width,
    height=height,
    xaxis=XAxis(axis),
    yaxis=YAxis(axis),
    margin=Margin(
        l=40,
        r=40,
        b=85,
        t=100,
        pad=0,
       
    ),
    hovermode='closest',
    plot_bgcolor='#EFECEA', #set background color            
    )"""
layout = Layout(
    title='network graph for cities',
    font= Font(),
    showlegend=False,
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
                    args=['visible', [True, True, False, False,False,False]],
                    label='Detroit',
                    method='restyle'
                ),
                dict(
                    args=['visible', [False, False, True, True,False,False]],
                    label='San Froncisco',
                    method='restyle'
                ),
                dict(
                    args=['visible', [False, False, False, False,True,True]],
                    label='Abq',
                    method='restyle'
                )
                
            ]),
        )
    ]),
)

data=Data([trace1,trace2,trace3,trace4,trace5,trace6])

fig = Figure(data=data, layout=layout)


py.iplot(fig, filename = "tst6.html")






# restart python con
#show(Column(chord_from_df,dot,text()))

# ----------------------------Connection plot--------------------------------------#

