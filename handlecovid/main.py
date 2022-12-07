import pandas as pd
from dbfread import DBF
import geopandas
from shapely.geometry import Polygon,Point
import fiona
import shapefile




path = r'SHX/buildings.dbf'  # 文件目录
table = DBF(path, encoding='GBK', char_decode_errors='ignore')
df2 = pd.DataFrame(iter(table))
df = df2['name']
df2.to_csv('test.csv')

buildings = {'osm_id': {}, 'build_name': {}}
cnt = 0;

for i in range(0, 76717):
    temp = df[i]
    #print(temp[12])
    #print(temp[1])
    for j in range(0, len(temp)):
        if ((temp[j] >= 'a' and temp[j] <= 'z') or (temp[j] >= 'A' and temp[j] <= 'Z') ) and j != 0:
            buildings['osm_id'][cnt] = df2['osm_id'][i];
            buildings['build_name'][cnt] = temp[j:]
            cnt += 1
            break;

buildings = pd.DataFrame(buildings)
buildings.to_csv('buildings.csv')

covid = pd.read_json('covid.json')
covid.to_csv('test.csv')

new_covid = {'osm_id': {}, 'building_name': {}, 'date': {}}
cnt2 = 0;

# for i in range(0, 8766):
#     for j in range (0, cnt):
#         if buildings['build_name'][j] == covid['Building name'][i] :
#             new_covid['osm_id'][cnt2] = buildings['osm_id'][j]
#             new_covid['building_name'][cnt2] = buildings['build_name'][j]
#             new_covid['date'][cnt2] = covid['Last date of visit of the case(s)'][i]
#             cnt2 += 1
#             break
# new_covid = pd.DataFrame(new_covid)
# new_covid.to_csv('ncovid.csv')

# sf = shapefile.Reader('buildings.shp')
# sf = sf.shapeRecords()[0]
# print(sf.records())
# P = 22.276548, 114.151726
# G = ox.graph_from_place('Hong Kong')
# node_id = list(G.nodes)[0]
# print(node_id)
# Covid = pd.read_csv('ncovid.csv')
# #for i in range (0,53):
# print(G.nodes)

final_covid = {'osm_id': {}, 'building_name': {}, 'date': {}, 'lat': {}, 'lng': {}}
Covid = geopandas.read_file('shape/buildings.shp', encoding="utf-8")
Covid = pd.DataFrame(Covid)
Covid.to_csv('lbuild.csv')
# print(Covid.head())
newc = pd.read_csv('ncovid.csv')
final_cnt = 0;

# test2 = geopandas.GeoDataFrame.from_features(Covid['geometry'].values[0])
# test2.crs = 'EPSG:4326'
# test2 = pd.Series(Covid['geometry'][0])
# print(test2[0])
print(Covid['geometry'][0].exterior.coords[0])
x,y = Covid['geometry'][0].exterior.coords[0]
x = float(x)
y = float(y)
c = (x,y)
print(c[0])


for j in range(0, 810):
    for i in range(0, 76717):
        if Covid['osm_id'][i] == newc['osm_id'][j]:
            x, y = Covid['geometry'][i].exterior.coords[0]
            x = float(x)
            y = float(y)
            final_covid['lat'][final_cnt] = x
            final_covid['lng'][final_cnt] = y
            final_covid['osm_id'][final_cnt] = Covid['osm_id'][i]
            final_covid['building_name'][final_cnt] = newc['building_name'][j]
            final_covid['date'][final_cnt] = newc['date'][j]
            final_cnt += 1
            break

final_covid = pd.DataFrame(final_covid)
final_covid.to_csv('final.csv')




# df.to_csv('test.csv')
# print(df)
