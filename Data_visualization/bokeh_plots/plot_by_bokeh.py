
import pandas as pd
sf = pd.read_csv('sf.csv')
abq = pd.read_csv('abq.csv')
detroit = pd.read_csv('detroit.csv')

def change_area(df):
    df['area'] = [a.split()[2] for a in df['area']]
    return df

sf = change_area(sf)
abq = change_area(abq)
detroit = change_area(detroit)

import json
with open('tags.json') as f:
    d = json.load(f)
tags = d.keys()

####prepare the data for summary
from bokeh.models import ColumnDataSource
def source_num_tags(df):
    count_tag = dict()
    for tag in tags:
        df_tag = find_by_tag(df, d[tag])
        n,p = df_tag.shape
        count_tag.update({tag:n})
    data = dict({'x': range(len(tags)), 'y': count_tag.values(),
                'x0': range(len(tags)), 'y0': count_tag.values(),
                'vars': count_tag.keys(), 'vars0': count_tag.keys()})
                source = ColumnDataSource(data=data)
return source

prices = ['1.0', '2.0', '3.0', '4.0']
price_d = ['$$', '$', '$$$$', '$$$']
ratings = ['1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0']
def source_num_var(df, var, var_list):
    count_var = dict()
    for v in var_list:
        df_var = df.loc[df[var] == v]
        n,p = df_var.shape
        count_var.update({v: n})

    data = dict({'x': [float(v) for v in count_var.keys()], 'y': count_var.values(),
                'x0': [float(v) for v in count_var.keys()], 'y0': count_var.values()})
if(var == 'price'):
    data.update({'vars': price_d, 'vars0': price_d})
    else:
        data.update({'vars': count_var.keys(), 'vars0': count_var.keys()})
source = ColumnDataSource(data=data)
    return source

def source_num_area(df):
    areas = df['area'].unique()
    count_area = dict()
    for a in areas:
        df_area = df.loc[df['area'] == a]
        n,p = df_area.shape
        count_area.update({a:n})
    data = dict({'x': range(len(areas)), 'y': count_area.values(),
                'x0': range(len(areas)), 'y0': count_area.values(),
                'vars': count_area.keys(), 'vars0': count_area.keys()})
                source = ColumnDataSource(data=data)
return source

##### !!!!!!bar plot for summary
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Select, HoverTool, LabelSet, Label
from bokeh.plotting import figure, output_file, show
from bokeh.models.formatters import TickFormatter
from bokeh.core.properties import Dict, Int, String

source_sf_tag = source_num_tags(sf)
source_abq_tag = source_num_tags(abq)
source_det_tag = source_num_tags(detroit)

source_sf_price = source_num_var(sf, 'price', prices)
source_abq_price = source_num_var(abq, 'price', prices)
source_det_price = source_num_var(detroit, 'price', prices)

source_sf_rate = source_num_var(sf, 'rating', ratings)
source_abq_rate = source_num_var(abq, 'rating', ratings)
source_det_rate = source_num_var(detroit, 'rating', ratings)

source_sf_area = source_num_area(sf)
source_abq_area = source_num_area(abq)
source_det_area = source_num_area(detroit)

plot = figure(background_fill_color="#EFE8E2", title="", plot_width=600, plot_height=400)

plot.vbar(x='x', width=0.5, bottom=0, top='y', source = source_sf_tag, color="#2E8B57", line_color="#033649")

hover = HoverTool(tooltips=[('Var', '@vars'), ('Count', '@y')])
plot.add_tools(hover)

select_city = Select(title="Select City:", value="San Francisco", options=["San Francisco", "Albuquerque", "Detroit"])
select_var = Select(title="Select Metrics:", value="Tag", options=["Tag", "Price", "Rating", "Area"])

callback = CustomJS(args=dict(source_sf_tag=source_sf_tag, source_abq_tag=source_abq_tag, source_det_tag=source_det_tag,
                              source_sf_price=source_sf_price, source_abq_price=source_abq_price, source_det_price=source_det_price,
                              source_sf_rate=source_sf_rate, source_abq_rate=source_abq_rate, source_det_rate=source_det_rate,
                              source_sf_area=source_sf_area, source_abq_area=source_abq_area, source_det_area=source_det_area,
                              city_select_obj=select_city, var_select_obj=select_var), code="""
    var data_sf_tag = source_sf_tag.data;
    var data_abq_tag = source_abq_tag.data;
    var data_det_tag = source_det_tag.data;
    var data_sf_price = source_sf_price.data;
    var data_abq_price = source_abq_price.data;
    var data_det_price = source_det_price.data;
    var data_sf_rate = source_sf_rate.data;
    var data_abq_rate = source_abq_rate.data;
    var data_det_rate = source_det_rate.data;
    var data_sf_area = source_sf_area.data;
    var data_abq_area = source_abq_area.data;
    var data_det_area = source_det_area.data;
    
    var city = city_select_obj.get('value');
    var the_var = var_select_obj.get('value');
    
    if (city == 'San Francisco'){
    if(the_var == 'Tag'){
    data_sf_tag['x']= data_sf_tag['x0'];
    data_sf_tag['y'] = data_sf_tag['y0'];
    data_sf_tag['vars'] = data_sf_tag['vars0']
    }else if(the_var == 'Price'){
    data_sf_tag['x']= data_sf_price['x0'];
    data_sf_tag['y'] = data_sf_price['y0'];
    data_sf_tag['vars'] = data_sf_price['vars0']
    }else if(the_var == 'Rating'){
    data_sf_tag['x']= data_sf_rate['x0'];
    data_sf_tag['y'] = data_sf_rate['y0'];
    data_sf_tag['vars'] = data_sf_rate['vars0']
    }else if(the_var == 'Area'){
    data_sf_tag['x']= data_sf_area['x0'];
    data_sf_tag['y'] = data_sf_area['y0'];
    data_sf_tag['vars'] = data_sf_area['vars0']
    }
    
    }else if(city == 'Albuquerque'){
    if(the_var == 'Tag'){
    data_sf_tag['x']= data_abq_tag['x0'];
    data_sf_tag['y'] = data_abq_tag['y0'];
    data_sf_tag['vars'] = data_abq_tag['vars0']
    }else if(the_var == 'Price'){
    data_sf_tag['x']= data_abq_price['x0'];
    data_sf_tag['y'] = data_abq_price['y0'];
    data_sf_tag['vars'] = data_abq_price['vars0']
    }else if(the_var == 'Rating'){
    data_sf_tag['x']= data_abq_rate['x0'];
    data_sf_tag['y'] = data_abq_rate['y0'];
    data_sf_tag['vars'] = data_abq_rate['vars0']
    }else if(the_var == 'Area'){
    data_sf_tag['x']= data_abq_area['x0'];
    data_sf_tag['y'] = data_abq_area['y0'];
    data_sf_tag['vars'] = data_abq_area['vars0']
    }
    
    }else if(city == 'Detroit'){
    if(the_var == 'Tag'){
    data_sf_tag['x']= data_det_tag['x0'];
    data_sf_tag['y'] = data_det_tag['y0'];
    data_sf_tag['vars'] = data_det_tag['vars0']
    }else if(the_var == 'Price'){
    data_sf_tag['x']= data_det_price['x0'];
    data_sf_tag['y'] = data_det_price['y0'];
    data_sf_tag['vars'] = data_det_price['vars0']
    }else if(the_var == 'Rating'){
    data_sf_tag['x']= data_det_rate['x0'];
    data_sf_tag['y'] = data_det_rate['y0'];
    data_sf_tag['vars'] = data_det_rate['vars0']
    }else if(the_var == 'Area'){
    data_sf_tag['x']= data_det_area['x0'];
    data_sf_tag['y'] = data_det_area['y0'];
    data_sf_tag['vars'] = data_det_area['vars0']
    }
    }
    source_sf_tag.trigger('change');
    source_abq_tag.trigger('change');
    source_det_tag.trigger('change');
    source_sf_price.trigger('change');
    source_abq_price.trigger('change');
    source_det_price.trigger('change');
    source_sf_rate.trigger('change');
    source_abq_rate.trigger('change');
    source_det_rate.trigger('change');
    source_sf_area.trigger('change');
    source_abq_area.trigger('change');
    source_det_area.trigger('change');
    """)

select_city.callback = callback
select_var.callback = callback

plot.grid.grid_line_width = 2
plot.xaxis.major_label_text_font_size="12pt"
plot.xaxis.axis_label = 'Variable'
plot.yaxis.axis_label = 'Count'

layout_bar1 = column(row(select_city, select_var), plot)


#####!!!!prepare the data for bar plot2
from collections import Counter
from filter_dataframe import *
def var_by_tag(df, tag, var='price'):
    df_tag = find_by_tag(df, d[tag])
    df_var_no_none = df_tag[var].loc[~df_tag[var].str.contains('None')]
    df_var_count = Counter(df_var_no_none)
    if var == 'price':
        prices = ['1.0', '2.0', '3.0', '4.0']
        for p in prices:
            if df_var_count[p] == 0:
                df_var_count.update({p:0})
    return df_var_count

###!!!!get source data
def get_source_bar(df, tags):
    dict_one_tag = var_by_tag(df, tags[1])
    data = dict(x=[float(t) for t in dict_one_tag.keys()], y=dict_one_tag.values(), dollar=['$$', '$', '$$$$', '$$$'], dollar0=['$$', '$', '$$$$', '$$$'])
    for i in xrange(0, len(tags)):
        dict_one_tag = var_by_tag(df, tags[i])
        data.update({'x'+str(i):[float(t) for t in dict_one_tag.keys()], 'y'+str(i):dict_one_tag.values()})
    
    source = ColumnDataSource(data=data)
    return source

#####!!!!prepare the data for bar plot2
##### add the rating data
ratings = ['1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0']
prices = ['1.0', '2.0', '3.0', '4.0']
def make_up_price(the_dict):
    for p in prices:
        if the_dict[p] == 0:
            the_dict.update({p:0})
    return the_dict

def get_source_bar_rating(df, ratings):
    df_var_one = df.loc[df['rating'] == ratings[0]]['price']
    df_var_one = [c for c in df_var_one if c != 'None']
    count_var_one = Counter(df_var_one)
    count_var_one = make_up_price(count_var_one)
    
    data = dict(x=[float(v) for v in count_var_one.keys()], y=count_var_one.values())
    
    for i in xrange(0, len(ratings)):
        df_var = df.loc[df['rating'] == ratings[i]]['price']
        df_var = [c for c in df_var if c != 'None']
        count_var = Counter(df_var)
        count_var = make_up_price(count_var)
        data.update({'x'+str(i):[float(v) for v in count_var.keys()], 'y'+str(i):count_var.values()})
    
    source = ColumnDataSource(data=data)
    return source

##### bar plot for price by tag
from bokeh.layouts import column, row
from bokeh.models import CustomJS, ColumnDataSource, RadioButtonGroup, Select, HoverTool
from bokeh.plotting import figure, output_file, show
from bokeh.models.formatters import TickFormatter
from bokeh.core.properties import Dict, Int, String

source_sf_tags = get_source_bar(sf, tags)
source_abq_tags = get_source_bar(abq, tags)
source_det_tags = get_source_bar(detroit, tags)

plot = figure(background_fill_color="#EFE8E2", title="Bar plot for price", plot_width=600, plot_height=400)
plot.vbar(x='x', width=0.5, bottom=0, top='y', source = source_sf_tags, color="firebrick")

hover = HoverTool(tooltips=[('Price', '@dollar'), ('Count', '@y')])
plot.add_tools(hover)

select_city = Select(title="Select City:", value="San Francisco", options=["San Francisco", "Albuquerque", "Detroit"])
select_tag = Select(title="Select tag:", value="Chinese", options=tags)

callback = CustomJS(args=dict(source_sf_tag=source_sf_tags, source_abq_tag=source_abq_tags, source_det_tag=source_det_tags,
                              city_select_obj=select_city, tag_select_obj=select_tag, rating_select_obj=select_rating), code="""
    var data_sf_tag = source_sf_tag.data;
    var data_abq_tag = source_abq_tag.data;
    var data_det_tag = source_det_tag.data;
    
    var city = city_select_obj.get('value');
    var tag = tag_select_obj.get('value');
    
    if (city == 'San Francisco'){
    if(tag == 'Alcohol'){
    data_sf_tag['x']= data_sf_tag['x0'];
    data_sf_tag['y'] = data_sf_tag['y0'];
    }else if(tag == 'Chinese'){
    data_sf_tag['x']= data_sf_tag['x1'];
    data_sf_tag['y'] = data_sf_tag['y1'];
    }else if(tag == 'Southeast Asian'){
    data_sf_tag['x']= data_sf_tag['x2'];
    data_sf_tag['y'] = data_sf_tag['y2'];
    }else if(tag == 'Dessert'){
    data_sf_tag['x']= data_sf_tag['x3'];
    data_sf_tag['y'] = data_sf_tag['y3'];
    }else if(tag == 'American'){
    data_sf_tag['x']= data_sf_tag['x4'];
    data_sf_tag['y'] = data_sf_tag['y4'];
    }else if(tag == 'JanpaneseKorean'){
    data_sf_tag['x']= data_sf_tag['x5'];
    data_sf_tag['y'] = data_sf_tag['y5'];
    }else if(tag == 'Indian'){
    data_sf_tag['x']= data_sf_tag['x6'];
    data_sf_tag['y'] = data_sf_tag['y6'];
    }else if(tag == 'South American(Mexican)'){
    data_sf_tag['x']= data_sf_tag['x7'];
    data_sf_tag['y'] = data_sf_tag['y7'];
    }else if(tag == 'European'){
    data_sf_tag['x']= data_sf_tag['x8'];
    data_sf_tag['y'] = data_sf_tag['y8'];
    }
    
    }else if(city == 'Albuquerque'){
    if(tag == 'Alcohol'){
    data_sf_tag['x']= data_abq_tag['x0'];
    data_sf_tag['y'] = data_abq_tag['y0'];
    }else if(tag == 'Chinese'){
    data_sf_tag['x']= data_abq_tag['x1'];
    data_sf_tag['y'] = data_abq_tag['y1'];
    }else if(tag == 'Southeast Asian'){
    data_sf_tag['x']= data_abq_tag['x2'];
    data_sf_tag['y'] = data_abq_tag['y2'];
    }else if(tag == 'Dessert'){
    data_sf_tag['x']= data_abq_tag['x3'];
    data_sf_tag['y'] = data_abq_tag['y3'];
    }else if(tag == 'American'){
    data_sf_tag['x']= data_abq_tag['x4'];
    data_sf_tag['y'] = data_abq_tag['y4'];
    }else if(tag == 'JanpaneseKorean'){
    data_sf_tag['x']= data_abq_tag['x5'];
    data_sf_tag['y'] = data_abq_tag['y5'];
    }else if(tag == 'Indian'){
    data_sf_tag['x']= data_abq_tag['x6'];
    data_sf_tag['y'] = data_abq_tag['y6'];
    }else if(tag == 'South American(Mexican)'){
    data_sf_tag['x']= data_abq_tag['x7'];
    data_sf_tag['y'] = data_abq_tag['y7'];
    }else if(tag == 'European'){
    data_sf_tag['x']= data_abq_tag['x8'];
    data_sf_tag['y'] = data_abq_tag['y8'];
    }
    
    }else if(city == 'Detroit'){
    if(tag == 'Alcohol'){
    data_sf_tag['x']= data_det_tag['x0'];
    data_sf_tag['y'] = data_det_tag['y0'];
    }else if(tag == 'Chinese'){
    data_sf_tag['x']= data_det_tag['x1'];
    data_sf_tag['y'] = data_det_tag['y1'];
    }else if(tag == 'Southeast Asian'){
    data_sf_tag['x']= data_det_tag['x2'];
    data_sf_tag['y'] = data_det_tag['y2'];
    }else if(tag == 'Dessert'){
    data_sf_tag['x']= data_det_tag['x3'];
    data_sf_tag['y'] = data_det_tag['y3'];
    }else if(tag == 'American'){
    data_sf_tag['x']= data_det_tag['x4'];
    data_sf_tag['y'] = data_det_tag['y4'];
    }else if(tag == 'JanpaneseKorean'){
    data_sf_tag['x']= data_det_tag['x5'];
    data_sf_tag['y'] = data_det_tag['y5'];
    }else if(tag == 'Indian'){
    data_sf_tag['x']= data_det_tag['x6'];
    data_sf_tag['y'] = data_det_tag['y6'];
    }else if(tag == 'South American(Mexican)'){
    data_sf_tag['x']= data_det_tag['x7'];
    data_sf_tag['y'] = data_det_tag['y7'];
    }else if(tag == 'European'){
    data_sf_tag['x']= data_det_tag['x8'];
    data_sf_tag['y'] = data_det_tag['y8'];
    }
    }
    source_sf_tag.trigger('change');
    source_abq_tag.trigger('change');
    source_det_tag.trigger('change');
    """)

select_city.callback = callback
select_tag.callback = callback

plot.grid.grid_line_width = 2
plot.xaxis.major_label_text_font_size="12pt"
plot.xaxis.axis_label = 'Price'
plot.yaxis.axis_label = 'Count'

layout_bar2 = column(row(select_city, select_tag), plot)

###prepare the data for histogram1
def extract_var(df, tag, var='rating', bin_num = 10):
    df_tag = find_by_tag(df, d[tag])
    var_list = [float(r) for r in df_tag[var] if r != 'None']
    hist, edges = np.histogram(var_list, density=False, bins=bin_num)
    return hist, edges

def get_source_barplot_tag(df, tags):
    hist, edges = extract_var(df, tags[1])
    data = dict(x=hist, y=edges[:-1], z=edges[1:])
    for i in xrange(0, len(tags)):
        hist, edges = extract_var(df, tags[i])
        data.update({'x'+str(i):hist, 'y'+str(i):edges[:-1], 'z'+str(i):edges[1:]})
    
    source = ColumnDataSource(data=data)
    return source

###prepare the data for histogram2
prices=['1.0', '2.0', '3.0', '4.0']
def extract_variable(df, price, var1='price', var2='rating', bin_num = 10):
    df_var = df.loc[df[var1] == price][var2]
    var_list = [float(r) for r in df_var if r != 'None']
    hist, edges = np.histogram(var_list, bins=bin_num)
    return hist, edges

def get_source_barplot_price(df, prices):
    hist, edges = extract_variable(df, prices[0])
    data = dict(x=hist, y=edges[:-1], z=edges[1:])
    for i in xrange(0, len(prices)):
        hist, edges = extract_variable(df, prices[i])
        data.update({'x'+str(i):hist, 'y'+str(i):edges[:-1], 'z'+str(i):edges[1:]})
    
    source = ColumnDataSource(data=data)
    return source

##plot histogram for rating by tag
##combine two histogram
import numpy as np
import scipy.special
from bokeh.layouts import column, row, gridplot
from bokeh.models import CustomJS, ColumnDataSource, RadioButtonGroup, Select, HoverTool
from bokeh.plotting import figure, output_file, show

source_sf_tag = get_source_barplot_tag(sf, tags)
source_abq_tag = get_source_barplot_tag(abq, tags)
source_det_tag = get_source_barplot_tag(detroit, tags)

source_sf_price = get_source_barplot_price(sf, prices)
source_abq_price = get_source_barplot_price(abq, prices)
source_det_price = get_source_barplot_price(detroit, prices)

plot = figure(background_fill_color="#EFE8E2", title="Histogram for rating", plot_width=600, plot_height=400)

hover = HoverTool(tooltips=[('Count', '@x')])
plot.add_tools(hover)

plot.quad(top='x', bottom=0, left='y', right='z', source=source_sf_tag, fill_color="#036564", line_color="#033649")

select_city = Select(title="Select City:", value="San Francisco", options=["San Francisco", "Albuquerque", "Detroit"])
select_tag = Select(title="Select tag:", value="Chinese", options=tags+['None'])
select_price = Select(title="Select price:", value="None", options=['$', '$$', '$$$', '$$$$', 'None'])

callback = CustomJS(args=dict(source_sf_tag=source_sf_tag, source_abq_tag=source_abq_tag, source_det_tag=source_det_tag,
                              source_sf_price=source_sf_price, source_abq_price=source_abq_price, source_det_price=source_det_price,
                              city_select_obj=select_city, tag_select_obj=select_tag, price_select_obj=select_price), code="""
    var data_sf_tag = source_sf_tag.data;
    var data_abq_tag = source_abq_tag.data;
    var data_det_tag = source_det_tag.data;
    
    var data_sf_price = source_sf_price.data;
    var data_abq_price = source_abq_price.data;
    var data_det_price = source_det_price.data;
    
    var city = city_select_obj.get('value');
    var tag = tag_select_obj.get('value');
    var price = price_select_obj.get('value');
    
    if (city == 'San Francisco'){
    if(tag == 'Alcohol' && price == 'None'){
    data_sf_tag['x']=data_sf_tag['x0']
    data_sf_tag['y']=data_sf_tag['y0']
    data_sf_tag['z']=data_sf_tag['z0']
    }else if(tag == 'Chinese' && price == 'None'){
    data_sf_tag['x']=data_sf_tag['x1']
    data_sf_tag['y']=data_sf_tag['y1']
    data_sf_tag['z']=data_sf_tag['z1']
    }else if(tag == 'Southeast Asian' && price == 'None'){
    data_sf_tag['x']=data_sf_tag['x2']
    data_sf_tag['y']=data_sf_tag['y2']
    data_sf_tag['z']=data_sf_tag['z2']
    }else if(tag == 'Dessert' && price == 'None'){
    data_sf_tag['x']= data_sf_tag['x3'];
    data_sf_tag['y'] = data_sf_tag['y3'];
    data_sf_tag['z']=data_sf_tag['z3'];
    }else if(tag == 'American' && price == 'None'){
    data_sf_tag['x']= data_sf_tag['x4'];
    data_sf_tag['y'] = data_sf_tag['y4'];
    data_sf_tag['z']=data_sf_tag['z4'];
    }else if(tag == 'JanpaneseKorean' && price == 'None'){
    data_sf_tag['x']= data_sf_tag['x5'];
    data_sf_tag['y'] = data_sf_tag['y5'];
    data_sf_tag['z']=data_sf_tag['z5'];
    }else if(tag == 'Indian' && price == 'None'){
    data_sf_tag['x']= data_sf_tag['x6'];
    data_sf_tag['y'] = data_sf_tag['y6'];
    data_sf_tag['z']=data_sf_tag['z6'];
    }else if(tag == 'South American(Mexican)' && price == 'None'){
    data_sf_tag['x']= data_sf_tag['x7'];
    data_sf_tag['y'] = data_sf_tag['y7'];
    data_sf_tag['z']=data_sf_tag['z7'];
    }else if(tag == 'European' && price == 'None'){
    data_sf_tag['x']= data_sf_tag['x8'];
    data_sf_tag['y'] = data_sf_tag['y8'];
    data_sf_tag['z']=data_sf_tag['z8'];
    }else if(tag == 'None' && price == '$'){
    data_sf_tag['x']= data_sf_price['x0'];
    data_sf_tag['y'] = data_sf_price['y0'];
    data_sf_tag['z']=data_sf_price['z0'];
    }else if(tag == 'None' && price == '$$'){
    data_sf_tag['x']= data_sf_price['x1'];
    data_sf_tag['y'] = data_sf_price['y1'];
    data_sf_tag['z']=data_sf_price['z1'];
    }else if(tag == 'None' && price == '$$$'){
    data_sf_tag['x']= data_sf_price['x2'];
    data_sf_tag['y'] = data_sf_price['y2'];
    data_sf_tag['z']=data_sf_price['z2'];
    }else if(tag == 'None' && price == '$$$$'){
    data_sf_tag['x']= data_sf_price['x3'];
    data_sf_tag['y'] = data_sf_price['y3'];
    data_sf_tag['z']=data_sf_price['z3'];
    }else if(tag == 'None' && price == 'None'){
    data_sf_tag['x']= [];
    data_sf_tag['y'] = [];
    data_sf_tag['z']= [];
    }
    
    }else if(city == 'Albuquerque'){
    if(tag == 'Alcohol' && price == 'None'){
    data_sf_tag['x']=data_abq_tag['x0']
    data_sf_tag['y']=data_abq_tag['y0']
    data_sf_tag['z']=data_abq_tag['z0']
    }else if(tag == 'Chinese' && price == 'None'){
    data_sf_tag['x']=data_abq_tag['x1']
    data_sf_tag['y']=data_abq_tag['y1']
    data_sf_tag['z']=data_abq_tag['z1']
    }else if(tag == 'Southeast Asian' && price == 'None'){
    data_sf_tag['x']=data_abq_tag['x2']
    data_sf_tag['y']=data_abq_tag['y2']
    data_sf_tag['z']=data_abq_tag['z2']
    }else if(tag == 'Dessert' && price == 'None'){
    data_sf_tag['x']= data_abq_tag['x3'];
    data_sf_tag['y'] = data_abq_tag['y3'];
    data_sf_tag['z']=data_abq_tag['z3'];
    }else if(tag == 'American' && price == 'None'){
    data_sf_tag['x']= data_abq_tag['x4'];
    data_sf_tag['y'] = data_abq_tag['y4'];
    data_sf_tag['z']=data_abq_tag['z4'];
    }else if(tag == 'JanpaneseKorean' && price == 'None'){
    data_sf_tag['x']= data_abq_tag['x5'];
    data_sf_tag['y'] = data_abq_tag['y5'];
    data_sf_tag['z']=data_abq_tag['z5'];
    }else if(tag == 'Indian' && price == 'None'){
    data_sf_tag['x']= data_abq_tag['x6'];
    data_sf_tag['y'] = data_abq_tag['y6'];
    data_sf_tag['z']=data_abq_tag['z6'];
    }else if(tag == 'South American(Mexican)' && price == 'None'){
    data_sf_tag['x']= data_abq_tag['x7'];
    data_sf_tag['y'] = data_abq_tag['y7'];
    data_sf_tag['z']=data_abq_tag['z7'];
    }else if(tag == 'European' && price == 'None'){
    data_sf_tag['x']= data_abq_tag['x8'];
    data_sf_tag['y'] = data_abq_tag['y8'];
    data_sf_tag['z']=data_abq_tag['z8'];
    }else if(tag == 'None' && price == '$'){
    data_sf_tag['x']= data_abq_price['x0'];
    data_sf_tag['y'] = data_abq_price['y0'];
    data_sf_tag['z']=data_abq_price['z0'];
    }else if(tag == 'None' && price == '$$'){
    data_sf_tag['x']= data_abq_price['x1'];
    data_sf_tag['y'] = data_abq_price['y1'];
    data_sf_tag['z']=data_abq_price['z1'];
    }else if(tag == 'None' && price == '$$$'){
    data_sf_tag['x']= data_abq_price['x2'];
    data_sf_tag['y'] = data_abq_price['y2'];
    data_sf_tag['z']=data_abq_price['z2'];
    }else if(tag == 'None' && price == '$$$$'){
    data_sf_tag['x']= data_abq_price['x3'];
    data_sf_tag['y'] = data_abq_price['y3'];
    data_sf_tag['z']=data_abq_price['z3'];
    }else if(tag == 'None' && price == 'None'){
    data_sf_tag['x']= [];
    data_sf_tag['y'] = [];
    data_sf_tag['z']= [];
    }
    
    }else if(city == 'Detroit'){
    if(tag == 'Alcohol' && price == 'None'){
    data_sf_tag['x']=data_det_tag['x0']
    data_sf_tag['y']=data_det_tag['y0']
    data_sf_tag['z']=data_det_tag['z0']
    }else if(tag == 'Chinese' && price == 'None'){
    data_sf_tag['x']=data_det_tag['x1']
    data_sf_tag['y']=data_det_tag['y1']
    data_sf_tag['z']=data_det_tag['z1']
    }else if(tag == 'Southeast Asian' && price == 'None'){
    data_sf_tag['x']=data_det_tag['x2']
    data_sf_tag['y']=data_det_tag['y2']
    data_sf_tag['z']=data_det_tag['z2']
    }else if(tag == 'Dessert' && price == 'None'){
    data_sf_tag['x']= data_det_tag['x3'];
    data_sf_tag['y'] = data_det_tag['y3'];
    data_sf_tag['z']=data_det_tag['z3'];
    }else if(tag == 'American' && price == 'None'){
    data_sf_tag['x']= data_det_tag['x4'];
    data_sf_tag['y'] = data_det_tag['y4'];
    data_sf_tag['z']=data_det_tag['z4'];
    }else if(tag == 'JanpaneseKorean' && price == 'None'){
    data_sf_tag['x']= data_det_tag['x5'];
    data_sf_tag['y'] = data_det_tag['y5'];
    data_sf_tag['z']=data_det_tag['z5'];
    }else if(tag == 'Indian' && price == 'None'){
    data_sf_tag['x']= data_det_tag['x6'];
    data_sf_tag['y'] = data_det_tag['y6'];
    data_sf_tag['z']=data_det_tag['z6'];
    }else if(tag == 'South American(Mexican)' && price == 'None'){
    data_sf_tag['x']= data_det_tag['x7'];
    data_sf_tag['y'] = data_det_tag['y7'];
    data_sf_tag['z']=data_det_tag['z7'];
    }else if(tag == 'European' && price == 'None'){
    data_sf_tag['x']= data_det_tag['x8'];
    data_sf_tag['y'] = data_det_tag['y8'];
    data_sf_tag['z']=data_det_tag['z8'];
    }else if(tag == 'None' && price == '$'){
    data_sf_tag['x']= data_det_price['x0'];
    data_sf_tag['y'] = data_det_price['y0'];
    data_sf_tag['z']=data_det_price['z0'];
    }else if(tag == 'None' && price == '$$'){
    data_sf_tag['x']= data_det_price['x1'];
    data_sf_tag['y'] = data_det_price['y1'];
    data_sf_tag['z']=data_det_price['z1'];
    }else if(tag == 'None' && price == '$$$'){
    data_sf_tag['x']= data_det_price['x2'];
    data_sf_tag['y'] = data_det_price['y2'];
    data_sf_tag['z']=data_det_price['z2'];
    }else if(tag == 'None' && price == '$$$$'){
    data_sf_tag['x']= data_det_price['x3'];
    data_sf_tag['y'] = data_det_price['y3'];
    data_sf_tag['z']=data_det_price['z3'];
    }else if(tag == 'None' && price == 'None'){
    data_sf_tag['x']= [];
    data_sf_tag['y'] = [];
    data_sf_tag['z']= [];
    }
    }
    source_sf_tag.trigger('change');
    source_abq_tag.trigger('change');
    source_det_tag.trigger('change');
    source_sf_price.trigger('change');
    source_abq_price.trigger('change');
    source_det_price.trigger('change');
    """)

select_city.callback = callback
select_tag.callback = callback
select_price.callback = callback

plot.grid.grid_line_width = 2
plot.xaxis.major_label_text_font_size="12pt"
plot.xaxis.axis_label = 'Rating'
plot.yaxis.axis_label = 'Count'

layout_hist = column(row(select_city, column(select_tag, select_price)), plot)


###prepare the data for boxplot
from itertools import compress
def prepare_data(df, size, var):
    df_var_area = df[[var, 'area']].loc[~df[var].str.contains('None')]
    df_var_area[var] = df_var_area[var].astype(float)
    
    big_area = df_var_area.groupby('area').size() > size
    area_name = list(df_var_area.groupby('area').size().index)
    big_areas = list(compress(area_name, big_area))
    
    filter_area = df_var_area['area'].apply(lambda x : x in big_areas)
    return big_areas, df_var_area.loc[filter_area]

def outliers(group, var, upper, lower):
    area = group.name
    return group[(group[var] > upper.loc[area][var]) | (group[var] < lower.loc[area][var])][var]

def get_source_boxplot(df, size, var):
    big_areas, df_var_area = prepare_data(df, size, var)
    
    #find the quartiles and IQR for each category
    groups = df_var_area.groupby('area')
    q1 = groups.quantile(q=0.25)
    q2 = groups.quantile(q=0.5)
    q3 = groups.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr
    
    # find the outliers for each category
    out = groups.apply(lambda x: outliers(x, var, upper, lower))
    
    # prepare outlier data for plotting, we need coordinates for every outlier.
    if not out.empty:
        outx = []
        outy = []
        for a in df_var_area['area']:
            # only add outliers if they exist
            if not out.loc[a].empty:
                for value in out[a]:
                    outx.append(big_areas.index(a))
                    outy.append(value)

    qmin = groups.quantile(q=0.00)
    qmax = groups.quantile(q=1.00)
    upper[var] = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,var]), upper[var])]
    lower[var] = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,var]), lower[var])]
    
    data1 = {'big_areas':big_areas, 'area':range(len(big_areas)), 'upper':upper[var], 'lower':lower[var], 'q1': q1[var],
        'q2': q2[var], 'q3': q3[var],
            'big_areas0':big_areas, 'area0':range(len(big_areas)), 'upper0':upper[var], 'lower0':lower[var], 'q10': q1[var],
                'q20': q2[var], 'q30': q3[var]}
    data2 = {'outx':outx, 'outy': outy, 'outx0':outx, 'outy0': outy}
    source1 = ColumnDataSource(data=data1)
    source2 = ColumnDataSource(data=data2)
    return source1, source2

#####boxplot!!!
from math import pi
import numpy as np
from bokeh.layouts import column, row, gridplot
from bokeh.models import CustomJS, ColumnDataSource, RadioButtonGroup, Select, HoverTool
from bokeh.plotting import figure, output_file, show

####data for boxplot!!!
source_sf_rate1, source_sf_rate2 = get_source_boxplot(sf, 100, 'rating')
source_abq_rate1, source_abq_rate2 = get_source_boxplot(abq, 30, 'rating')
source_det_rate1, source_det_rate2 = get_source_boxplot(detroit, 30, 'rating')

source_sf_price1, source_sf_price2 = get_source_boxplot(sf, 100, 'price')
source_abq_price1, source_abq_price2 = get_source_boxplot(abq, 30, 'price')
source_det_price1, source_det_price2 = get_source_boxplot(detroit, 30, 'price')

plot = figure(background_fill_color="#EFE8E2", title="", plot_width=600, plot_height=400)

hover = HoverTool(tooltips=[('Area', '@big_areas'), ('25% quantile', '@q1'), ('mean', '@q2'), ('75% quantile', '@q3')])
plot.add_tools(hover)

# stems
plot.segment(x0='area', y0='upper', x1='area', y1='q3', line_color="black", source=source_sf_rate1)
plot.segment(x0='area', y0='lower', x1='area', y1='q1', line_color="black", source=source_sf_rate1)

# boxes
plot.vbar(x='area', width=0.7, bottom='q2', top='q3', fill_color="#E08E79", line_color="black", source=source_sf_rate1)
plot.vbar(x='area', width=0.7, bottom='q1', top='q2', fill_color="#3B8686", line_color="black", source=source_sf_rate1)

# whiskers (almost-0 height rects simpler than segments)
plot.rect(x='area', y='upper', width=0.2, height=0.01, line_color="black", source=source_sf_rate1)
plot.rect(x='area', y='lower', width=0.2, height=0.01, line_color="black", source=source_sf_rate1)

# outliers
#if not out.empty:
plot.circle(x='outx', y='outy', size=6, color="red", fill_alpha=0.6, source= source_sf_rate2)

radio_button_group_city = RadioButtonGroup(labels=["San Francisco", "Albuquerque", "Deltroit"], active=0)
radio_button_group_var = RadioButtonGroup(labels=["Rating", "Price"], active=0)
radio_button_group_outlier = RadioButtonGroup(labels=["Show outliers", "Not show outliers"], active=0)

callback = CustomJS(args=dict(source_sf_rate1=source_sf_rate1, source_sf_rate2=source_sf_rate2, source_abq_rate1=source_abq_rate1,
                              source_abq_rate2=source_abq_rate2, source_det_rate1=source_det_rate1, source_det_rate2=source_det_rate2,
                              source_sf_price1=source_sf_price1, source_sf_price2=source_sf_price2, source_abq_price1=source_abq_price1,
                              source_abq_price2=source_abq_price2, source_det_price1=source_det_price1, source_det_price2=source_det_price2,
                              city_select_obj=radio_button_group_city, var_select_obj=radio_button_group_var,
                              outlier_select_obj=radio_button_group_outlier), code="""
    var data_sf_rate1 = source_sf_rate1.data;
    var data_sf_rate2 = source_sf_rate2.data;
    var data_abq_rate1 = source_abq_rate1.data;
    var data_abq_rate2 = source_abq_rate2.data;
    var data_det_rate1 = source_det_rate1.data;
    var data_det_rate2 = source_det_rate2.data;
    
    var data_sf_price1 = source_sf_price1.data;
    var data_sf_price2 = source_sf_price2.data;
    var data_abq_price1 = source_abq_price1.data;
    var data_abq_price2 = source_abq_price2.data;
    var data_det_price1 = source_det_price1.data;
    var data_det_price2 = source_det_price2.data;
    
    var city = city_select_obj.get('active');
    var the_var =  var_select_obj.get('active');
    var outlier =  outlier_select_obj.get('active');
    
    if (city == 0){
    if(the_var == 0){
    data_sf_rate1['area']=data_sf_rate1['area0'];
    data_sf_rate1['upper']=data_sf_rate1['upper0'];
    data_sf_rate1['lower']=data_sf_rate1['lower0'];
    data_sf_rate1['q1']=data_sf_rate1['q10'];
    data_sf_rate1['q2']=data_sf_rate1['q20'];
    data_sf_rate1['q3']=data_sf_rate1['q30'];
    data_sf_rate1['big_areas']=data_sf_rate1['big_areas0'];
    
    if(outlier == 0){
    data_sf_rate2['outx']=data_sf_rate2['outx0'];
    data_sf_rate2['outy']=data_sf_rate2['outy0'];
    }else if(outlier == 1){
    data_sf_rate2['outx']=[];
    data_sf_rate2['outy']=[];
    }
    }else if(the_var == 1){
    data_sf_rate1['area']=data_sf_price1['area0'];
    data_sf_rate1['upper']=data_sf_price1['upper0'];
    data_sf_rate1['lower']=data_sf_price1['lower0'];
    data_sf_rate1['q1']=data_sf_price1['q10'];
    data_sf_rate1['q2']=data_sf_price1['q20'];
    data_sf_rate1['q3']=data_sf_price1['q30'];
    data_sf_rate1['big_areas']=data_sf_price1['big_areas0'];
    
    if(outlier == 0){
    data_sf_rate2['outx']=data_sf_price2['outx0'];
    data_sf_rate2['outy']=data_sf_price2['outy0'];
    }else if(outlier == 1){
    data_sf_rate2['outx']=[];
    data_sf_rate2['outy']=[];
    }
    }
    }else if(city == 1){
    if(the_var == 0){
    data_sf_rate1['area']=data_abq_rate1['area0'];
    data_sf_rate1['upper']=data_abq_rate1['upper0'];
    data_sf_rate1['lower']=data_abq_rate1['lower0'];
    data_sf_rate1['q1']=data_abq_rate1['q10'];
    data_sf_rate1['q2']=data_abq_rate1['q20'];
    data_sf_rate1['q3']=data_abq_rate1['q30'];
    data_sf_rate1['big_areas']=data_abq_rate1['big_areas0'];
    
    if(outlier == 0){
    data_sf_rate2['outx']=data_abq_rate2['outx0'];
    data_sf_rate2['outy']=data_abq_rate2['outy0'];
    }else if(outlier == 1){
    data_sf_rate2['outx']=[];
    data_sf_rate2['outy']=[];
    }
    }else if(the_var == 1){
    data_sf_rate1['area']=data_abq_price1['area0'];
    data_sf_rate1['upper']=data_abq_price1['upper0'];
    data_sf_rate1['lower']=data_abq_price1['lower0'];
    data_sf_rate1['q1']=data_abq_price1['q10'];
    data_sf_rate1['q2']=data_abq_price1['q20'];
    data_sf_rate1['q3']=data_abq_price1['q30'];
    data_sf_rate1['big_areas']=data_abq_price1['big_areas0'];
    
    if(outlier == 0){
    data_sf_rate2['outx']=data_abq_price2['outx0'];
    data_sf_rate2['outy']=data_abq_price2['outy0'];
    }else if(outlier == 1){
    data_sf_rate2['outx']=[];
    data_sf_rate2['outy']=[];
    }
    }
    }else if(city == 2){
    if(the_var == 0){
    data_sf_rate1['area']=data_det_rate1['area0'];
    data_sf_rate1['upper']=data_det_rate1['upper0'];
    data_sf_rate1['lower']=data_det_rate1['lower0'];
    data_sf_rate1['q1']=data_det_rate1['q10'];
    data_sf_rate1['q2']=data_det_rate1['q20'];
    data_sf_rate1['q3']=data_det_rate1['q30'];
    data_sf_rate1['big_areas']=data_det_rate1['big_areas0'];
    
    if(outlier == 0){
    data_sf_rate2['outx']=data_det_rate2['outx0'];
    data_sf_rate2['outy']=data_det_rate2['outy0'];
    }else if(outlier == 1){
    data_sf_rate2['outx']=[];
    data_sf_rate2['outy']=[];
    }
    }else if(the_var == 1){
    data_sf_rate1['area']=data_det_price1['area0'];
    data_sf_rate1['upper']=data_det_price1['upper0'];
    data_sf_rate1['lower']=data_det_price1['lower0'];
    data_sf_rate1['q1']=data_det_price1['q10'];
    data_sf_rate1['q2']=data_det_price1['q20'];
    data_sf_rate1['q3']=data_det_price1['q30'];
    data_sf_rate1['big_areas']=data_det_price1['big_areas0'];
    
    if(outlier == 0){
    data_sf_rate2['outx']=data_det_price2['outx0'];
    data_sf_rate2['outy']=data_det_price2['outy0'];
    }else if(outlier == 1){
    data_sf_rate2['outx']=[];
    data_sf_rate2['outy']=[];
    }
    }
    }
    source_sf_rate1.trigger('change');
    source_sf_rate2.trigger('change');
    source_abq_rate1.trigger('change');
    source_abq_rate2.trigger('change');
    source_det_rate1.trigger('change');
    source_det_rate2.trigger('change');
    source_sf_price1.trigger('change');
    source_sf_price2.trigger('change');
    source_abq_price1.trigger('change');
    source_abq_price2.trigger('change');
    source_det_price1.trigger('change');
    source_det_price2.trigger('change');
    """)

radio_button_group_city.callback = callback
radio_button_group_outlier.callback = callback
radio_button_group_var.callback = callback

plot.xgrid.grid_line_color = None
plot.ygrid.grid_line_color = "white"
plot.grid.grid_line_width = 2
plot.xaxis.major_label_text_font_size="12pt"
#plot.xaxis.major_label_orientation = -pi/4

plot.xaxis.axis_label = 'Variable'
plot.yaxis.axis_label = 'Value'

layout_boxplot = column(row(radio_button_group_city, radio_button_group_var), radio_button_group_outlier, plot)

###output html file
from bokeh.models.widgets import Slider,CheckboxGroup,DataTable,MultiSelect,TableColumn
from bokeh.models.layouts import WidgetBox
from bokeh.embed import components
from bokeh.util.browser import view
from bokeh.resources import INLINE
from bokeh.plotting import ColumnDataSource, curdoc

from jinja2 import Template
script_bar1, div_bar1 = components(layout_bar1)
script_bar2, div_bar2 = components(layout_bar2)
script_hist, div_hist = components(layout_hist)
script_box, div_box = components(layout_boxplot)

js_resources = INLINE.render_js()
css_resources = INLINE.render_css()

template = Template('''<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <title>Price</title>
    {{ js_resources }}
    {{ css_resources }}
    <style>
    .bk-root{
    float: left;
    width: 50%;
    margin: 10px;
    clear: left;
    margin-bottom: 60px;
    }
    .analysis{
    margin-top: 40px;
    }
    h3{
    clear:left;
    }
    
    </style>
    </head>
    <body>
    <h1>Descriptive Satitstics</h1>
    <h3 align = "center">Summary</h3>
    {{ div_bar1}}
    <p class = "analysis"><strong> Are there any differences between three cities? </strong></p>
    <ol>
    <li><strong>Tag</strong>
    <ul style="list-style-type:disc">
    <li>Among these three cities, restaurants belonging to American, Alcohol and Dessert categories
    share the largest proportion.</li>
    <li>The number of different categories of restaurants in San Francisco is almost evenly distributed
    (since San Francisco is an international metropolis). Albuquerque has larger proportion of
    Mexican food than other food since it is close to Mexico, while Detroit has more European food
    than others.</li>
    </ul>
    </li>
    
    <li><strong>Price('$':Inexpensive, '$$':Moderate, '$$$':Pricey, '$$$$':Highend)</strong>
    <ul style="list-style-type:disc">
    <li>Most restaurants are inexpensive and moderate in three cities.</li>
    <li>The average price in San Francisco is higher than two other cities.</li>
    <li>In San Francisco, the number of moderate restaurants is larger than inexpensive restaurants.
    Also, it has many pricey and highend restaurants. However, in two other cities,
    the number of inexpensive restaurants is larger than moderate restaurants.
    And they rarely have pricey and highend restaurants.</li>
    </ul>
    </li>
    
    <li><strong>Rating(1.0-3.0:Low, 3.0-4.0:Moderate, 4.0-5.0:High)</strong>
    <ul style="list-style-type:disc">
    <li>The rating in three cities are all close to normal distribution.</li>
    <li>San Francisco obviously has fewer restaurants whose rating is lower than 3.0.
    It means we are more likely to enter a great restaurant in San Francisco.</li>
    </ul>
    </li>
    
    <li><strong>Area</strong>
    <ul style="list-style-type:disc">
    <li>In <a href = "number_sf_restaurant_choropleth.html">San Francisco</a>, the main areas for restaurants are SoMa, Misson, Financial District and North Beach.</li>
    <li>In Albuquerque, most restaurants are located in Business Parkway/Academy Acres and Eastside. </li>
    <li>In Detroit, Downriver is the home for the restaurants.</li>
    </ul>
    </li>
    </ol>
    {{ script_bar1 }}
    
    <h3 align = "center">Barplot for price</h3>
    {{ div_bar2}}
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <p class = "analysis"><strong> Do different kinds of food have different distribution of price? </strong></p>
    <ol>
    <li>In general, cities do not affect the distribution of price for various kinds of food.
    For example, the distribution of price for Chinese food is similar among three cities.
    To our surprise, Detroit has more moderate southeast Asian restaurants than other cities.</li>
    <li>Chinese, Southeast Asian, Dessert, American, Indian, South American(Mexican) foods are cheaper than
    Alcohol, JanpaneseKorean, European foods.</li>
    </ol>
    
    <p><strong> Is price related to rating?</strong></p>
    <p>From the distribution of price under different ratings, we find that price is not related to rating
    since the price is concentrated on '$' and '$$' and do not show significant difference under various ratings.</p>
    
    {{ script_bar2 }}
    
    <h3 align = "center">Histogram for rating</h3>
    {{ div_hist }}
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <p class = "analysis"><strong> Do different kinds of food have different distributions of rating? </strong></p>
    <ol>
    <li>In general, cities affect the distribution of rating for some kinds of food.
    For example, Albuquerque has a larger proportion of Low ratings for European food
    than other cities.</li>
    <li>In San Francisco, Alcohol, Dessert, American and South American(Mexican) food tend to
    have higher ratings than other kinds of food.</li>
    <li>In Albuquerque, Dessert, American and South American(Mexican) food have a larger percentage of high ratings,
    while American food has a larger proportion of low ratings than others.</li>
    <li>In Detroit, Dessert and Southeast Asian food have a larger percentage of high ratings.</li>
    <li>In conclusion, people in different areas might have different tastes. </li>
    </ol>
    <p><strong> Is price related to rating?</strong></p>
    <p> We check the distribution of rating under different prices.
    Then it is found that when restaurants are expensive, they are more likely to have high ratings. </p>
    {{ script_hist }}
    
    
    <h3 align = "center">Boxplot for Rating/Price in Different Areas</h3>
    {{ div_box }}
    <p class = "analysis"><strong> Does different areas have different distribution of rating and price?</strong></p>
    <p>There are 75, 12 and 38 areas in San Francisco, Albuquerque and Detroit respectively.
    Some areas only have several restaurants, so we select areas which contains more than 100 restaurants
    in San Francisco and more than 30 restaurants in Albuquerque and Detroit to plot.</p>
    <p>The orange bar in the boxplot shows the range of mean to 75% quantile while the green bar displays
    the range of 25% quantile to the mean.</p>
    <ol>
    <li><strong> Rating </strong>
    <ul style="list-style-type:disc">
    <li>In San Francisco, restaurants in Bayview-Hunters Point, Bernal Heights, Castro, Misson, Potrero Hill,
    SoMa areas have higher rating than others.</li>
    <li>In Albuquerque, restaurants in Barelas/South Valley, Downtown and International District areas have
    higher rating than others.</li>
    <li>In Detroit, restaurants in Eastern Market, Southwest Detroit, Warrendale areas have higher rating than
    others.</li>
    </ul>
    </li>
    
    <li><strong> Price </strong>
    <ul style="list-style-type:disc">
    <li>For each city, price of restaurants in different areas are concentrated on "$" and "$$".
    But there still exists slightly difference.</li>
    <li>In <a href= "ratio_expensive_restaurant_choropleth.html">San Francisco</a>, restaurants in Chinatown, Inner Sunset, Mission, Outer Sunset, Tenderlion areas
    are cheaper than others.</li>
    <li>In Albuquerque, restaurants in the Barelas/South Valley area are cheaper than others.</li>
    <li>In Detroit, restaurants in Downtown Birmingham and Downtown Royal Oak areas are little more expensive than
    others.</li>
    </ul>
    </li>
    
    </ol>
    {{ script_box }}
    
    </body>
    </html>
    ''')

html = template.render(js_resources=js_resources,
                       css_resources=css_resources,
                       script_bar1=script_bar1,
                       div_bar1=div_bar1,
                       script_bar2=script_bar2,
                       div_bar2=div_bar2,
                       script_hist=script_hist,
                       div_hist=div_hist,
                       script_box=script_box,
                       div_box=div_box,)

filename = 'price.html'

import codecs
with codecs.open(filename, 'w', encoding='utf8') as f:
    f.write(html)
