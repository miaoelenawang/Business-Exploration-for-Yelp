import pandas as pd
import folium
import geopandas as gpd
import shapely.geometry as geom
import numpy as np
import json


df = pd.read_csv('sf.csv')
#print df.columns
price_sf = df[['price','longitude','latitude','title']]
n = price_sf.isnull()
n['c'] = [any(n.ix[i,:]) for i in range(n.shape[0])]
N = price_sf.applymap(lambda i: i=='None')
N['c'] = [any(N.ix[i,:]) for i in range(n.shape[0])]
alldata = price_sf.ix[~N['c'],:]
alldata[['price','longitude','latitude']] = alldata[['price','longitude','latitude']].astype('float64') 
alldata = alldata.reset_index()

with open("SanFrancisco.Neighborhoods.json") as file:
    sfneigh = json.load(file)
neighbor_sf_df = pd.DataFrame([{'neighbor':i['properties']['neighborhood'],'id':i['properties']['id']} for i in sfneigh['features']])
shape_json = [i['geometry']['geometries'][0]['coordinates'][0] for i in sfneigh['features']]
#first_shape = sfneigh['features'][0]['geometry']['geometries'][0]['coordinates'][0]
#name = sfneigh['features'][0]['properties']['neighborhood']
#ID = sfneigh['features'][0]['properties']['id']
for i in range(len(shape_json)):
    if len(shape_json[i]) == 1:
        shape_json[i] = shape_json[i][0]

poly_sf = []
for j in shape_json:
    poly_sf.append(geom.Polygon([(i[0],i[1]) for i in j]))

first = gpd.GeoDataFrame(neighbor_sf_df, geometry = poly_sf, crs = {'init' :'epsg:4326'})



lonlat = [geom.Point(lon, lat) for lon, lat in zip(alldata.longitude, alldata.latitude)]
sf = gpd.GeoDataFrame(alldata, geometry = lonlat, crs = {'init' :'epsg:4326'})
f1 = lambda x: any([x.within(i) for i in first.geometry])
sf_neighbor = map(f1, sf.geometry)
sf_neighbor_df1= sf.ix[sf_neighbor,:].reset_index()
f2 = lambda x: [x.within(i) for i in first.geometry].index(True)
neigh_range = map(f2, sf_neighbor_df1.geometry)
id_neigh = [first.ix[i,'id'] for i in neigh_range]
sf_neighbor_df1['id_neigh'] = id_neigh

#[i.centroid for i in first.geometry]
locationcenter = zip(first.neighbor,[np.array(i.centroid).tolist()[::-1] for i in first.geometry])

SF_COORDINATES = (37.76, -122.45)

district_geo = r'SanFrancisco.Neighborhoods.json'
sf_neighbor_df2 = pd.DataFrame(sf_neighbor_df1['id_neigh'].value_counts().astype(float))
sf_neighbor_df2.to_json('sf_neighbor_df2.json')
sf_neighbor_df2 = sf_neighbor_df2.reset_index()
sf_neighbor_df2.columns = ['District', 'Number']



map1 = folium.Map(location=SF_COORDINATES, zoom_start=12)
for i in locationcenter:
    folium.Marker(i[1], popup=i[0]).add_to(map1)


map1.choropleth(geo_path = district_geo,
              data_out = 'sf_neighbor_df2.json',
              data = sf_neighbor_df2,
              columns = ['District', 'Number'],
              key_on = 'feature.properties.id',
              fill_color = 'BuPu',
              fill_opacity = 0.7,
              line_opacity = 0.2,
              legend_name = 'Number of resturant per district')

    
map1.save('sf_resturant.html')
print "Success"
