import pandas as pd
import folium
import geopandas as gpd
import shapely.geometry as geom
import numpy as np
import json


with open("state.geo.json") as file:
    state = json.load(file)

state_shape = pd.DataFrame([{'State':i['properties']["STUSPS10"]} for i in  state['features']])

shape_json = [i["geometry"]["coordinates"][0] for i in state['features']]
#first_shape = sfneigh['features'][0]['geometry']['geometries'][0]['coordinates'][0]
#name = sfneigh['features'][0]['properties']['neighborhood']
#ID = sfneigh['features'][0]['properties']['id']
for i in range(len(shape_json)):
    if len(shape_json[i]) == 1:
        shape_json[i] = shape_json[i][0]

poly = []
for j in shape_json:
    poly.append(geom.Polygon([(i[0],i[1]) for i in j]))


state_geoshape = gpd.GeoDataFrame(state_shape.State, geometry = poly, crs = {'init' :'epsg:4326'})

#locationcenter = zip(state_geoshape.State,[np.array(i.centroid).tolist()[::-1] for i in state_geoshape.geometry])
USA_COORDINATES = (48, -102)

num = pd.read_csv("restaurants_num_usa.csv")
summary = num.groupby("State").sum()/2
summary["State"] = summary.index
num_res = pd.merge(state_geoshape, summary, how='left', on="State")
num_res = num_res[["State","total_business"]]

district_geo = r'state.geo.json'
num_res.to_json('num_res.json')
num_res = num_res.reset_index()



map1 = folium.Map(location=USA_COORDINATES, zoom_start=3.5)
#for i in locationcenter:
#    folium.Marker(i[1], popup=i[0]).add_to(map1)


map1.choropleth(geo_path = district_geo,
              data_out = 'num_res.json',
              data = num_res,
              columns = ['State', 'total_business'],
              key_on = 'feature.properties.STUSPS10',
              fill_color = 'YlOrRd',
              fill_opacity = 0.7,
              line_opacity = 0.2,
              legend_name = 'Number of restaurants in USA')

    
map1.save('us_state_restaurant_choropleth.html')
print "Success"
