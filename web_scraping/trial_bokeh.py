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
from bokeh.layouts import layout
from bokeh.sampledata.les_mis import data
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, Column, gridplot
from bokeh.models import ColumnDataSource,Paragraph, HoverTool, Div, GeoJSONDataSource,LogColorMapper
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure
from bokeh.charts import Histogram, output_file, show
from bokeh.palettes import Viridis6 as palette
from bokeh.sampledata.us_counties import data as counties
from  collections import Counter

# Set up data
#out_put

#--------------------------------tab 1 for price ------------------------------------------------#
def text():
    return(Div(text = "This is the plot for price distribution in Detroit, we can see that "))
output_file("detroit.html")
data = json_to_dataframe("detroit_food.txt")
data = data.drop_duplicates('id')
dic = dict(Counter(data['price']))
factors = list(dic.keys())
factors[2] = "None"
x =  list(dic.values())

source = ColumnDataSource(data=dict(factors = factors,x = x))
hover = HoverTool(tooltips=[
    ("price level", "@factors"),
    ("count", "@x")
    
])
dot = figure(title="Categorical Dot Plot", tools=[hover], toolbar_location=None,
            y_range=factors, x_range=[0,2000])


dot.segment(0, factors, x, factors, line_width=2, line_color="green", )
dot.circle(x = "x", y = "factors", source = source,size=15, fill_color="#A9A9F5", line_color="#A9F5E1", line_width=3)

show(dot)

# ----------------------------splitting factor plot-------------------------------------------#
# price, reviews and rating splitting by 2 categorical factors
idx = data['id']
connect = data[['id','related0','related1','related2','title']]
from bokeh.palettes import brewer
palette = brewer["Blues"][9]

con = [];
for ii in range(0,len(idx)-1):
    if connect.iloc[ii,1] !=None:
        con.append(" ".join(np.sort([connect.iloc[ii,0],connect.iloc[ii,1]])));
    if connect.iloc[ii,2] !=None:
        con.append(" ".join(np.sort([connect.iloc[ii,0],connect.iloc[ii,2]])));
    if connect.iloc[ii,3] !=None:
        con.append(" ".join(np.sort([connect.iloc[ii,0],connect.iloc[ii,3]])))
dict_con = dict(Counter(con))

chord = [];
for key,value in dict_con.items():
     ids = key.split(" ")
     ids.append(value)
     chord.append(ids)
chord = pd.DataFrame(chord)
chord = chord.rename(columns = {0:"source",1:"target",2:"value"})
chord = chord[chord['value'] >1]
chord_from_df = Chord(chord, source="source", target="target", value="value",width=1000, height=1000,palette = palette)


output_file('chord_from_df.html', mode="inline")
show(chord_from_df)

# ----------------------------Connection plot--------------------------------------#

from bokeh.sampledata.sample_geojson import geojson

geo_source = GeoJSONDataSource(geojson=geojson)

p1= figure()
p1.circle(x='x', y='y', alpha=0.9, source=geo_source)
output_file("geojson.html")
show(p1)










plot.api_key = "GOOGLE_API_KEY"

source = ColumnDataSource(
    data=dict(
        lat=data['latitude'],
        lon=data['longitude'],
    )
)

circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
plot.add_glyph(source, circle)

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
output_file("gmap_plot.html")
show(plot)

l = layout([[p],[text()]],sizing_mode = "scale_width")
show(l)
data['latitude']
data['longitude']