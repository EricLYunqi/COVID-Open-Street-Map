import json
import requests
import urllib.request
import pandas as pd
import geopandas as gpd
from dbfread import DBF
import osmnx as ox
import networkx as nx

region = ("中西区", "湾仔区", "东区", "南区", "油尖旺区", "深水埗区", "九龙城区", "黄大仙区", "观塘区", "葵青区", "荃湾区", "屯门区", "元朗区", "北区", "大埔区", "沙田区", "西贡区", "离岛区")
covid_data = {"中西区" :{2}, "湾仔区": {4}, "东区": {15}, "南区": {3}, "油尖旺区": {6}, "深水埗区": {15}, "九龙城区": {10}, "黄大仙区": {14},
              "观塘区": {19}, "葵青区": {17}, "荃湾区": {13}, "屯门区": {21}, "元朗区": {21}, "北区": {16}, "大埔区": {4}, "沙田区": {35},
              "西贡区": {14}, "离岛区": {5}}
region_e = ()


def get_data(length):
    response = requests.get("https://geo.datav.aliyun.com/areas_v3/bound/810000_full.json")
    res = response.json()
    hk_map_data = gpd.GeoDataFrame.from_features(res)
    hk_map_data.crs = 'EPSG:4326'

    Population = {'Adcode': {}, 'population': {}, 'elderly': {}}
    url_path = "https://www.censtatd.gov.hk/api/get.php?id=216&lang=tc&param=N4IgxgbiBcoMJwJqJqATDEAGHu94E8QAaEAfQBczMsTyAHa6EARhAF9SBlAUwA9UrTAGY6lJkNJlGNDqQCCAcx6CMzFtSlVMbKTOa1OIACJxBbZmStjt6sfuwcjAZyiwGEjKQAK3mAG0QACUAQwB3aR4AJzIAOxAAXW5+MiiQigBLAHsA4PC4gFcAWzjE0gBZHgATMhDlXNCIup5ShKMAGxgKKIKediA"
    with urllib.request.urlopen(url_path) as url:
        s = url.read()
    s = s.decode('UTF-8')
    s = json.loads(s)
    s = s['dataSet']

    count = 0
    for i in range(1, length):
        if s[i]['AgeDesc'] == 'Total' and s[i]['period'] == '2021' and s[i]['Sex'] == '' and s[i]['DC'] != '':
            Population['population'][i-86] = s[i]['figure']
            Population['Adcode'][i-86] = str(81000+(i-86))
        elif s[i]['Age'] == '>= 65' and s[i]['period'] == '2021' and s[i]['Sex'] == '' and s[i]['DC'] != '':
            Population['elderly'][count] = s[i]['figure']
            count += 1
    Population = pd.DataFrame(Population)
    hk_map_data_final = pd.concat([hk_map_data, Population], axis=1)
    return hk_map_data_final

def get_covid(length):
    response = requests.get("https://geo.datav.aliyun.com/areas_v3/bound/810000_full.json")
    res = response.json()
    hk_map_data = gpd.GeoDataFrame.from_features(res)
    hk_map_data.crs = 'EPSG:4326'

    Population = {'Adcode': {}, 'population': {}, 'elderly': {}}
    url_path = "https://www.censtatd.gov.hk/api/get.php?id=216&lang=tc&param=N4IgxgbiBcoMJwJqJqATDEAGHu94E8QAaEAfQBczMsTyAHa6EARhAF9SBlAUwA9UrTAGY6lJkNJlGNDqQCCAcx6CMzFtSlVMbKTOa1OIACJxBbZmStjt6sfuwcjAZyiwGEjKQAK3mAG0QACUAQwB3aR4AJzIAOxAAXW5+MiiQigBLAHsA4PC4gFcAWzjE0gBZHgATMhDlXNCIup5ShKMAGxgKKIKediA"
    with urllib.request.urlopen(url_path) as url:
        s = url.read()
    s = s.decode('UTF-8')
    s = json.loads(s)
    s = s['dataSet']

    count = 0
    for i in range(1, length):
        if s[i]['AgeDesc'] == 'Total' and s[i]['period'] == '2021' and s[i]['Sex'] == '' and s[i]['DC'] != '':
            Population['population'][i - 86] = s[i]['figure']
            Population['Adcode'][i - 86] = str(81000 + (i - 86))
        elif s[i]['Age'] == '>= 65' and s[i]['period'] == '2021' and s[i]['Sex'] == '' and s[i]['DC'] != '':
            Population['elderly'][count] = s[i]['figure']
            count += 1
    Population = pd.DataFrame(Population)
    hk_map_data_final = pd.concat([hk_map_data, Population], axis=1)
    return hk_map_data_final


    #print(s)

def handel_data(File):
    figure = {'Adcode': {}, 'data': {}}
    for i in range(1, 19):
        figure['Adcode'][i-1] = str(810000+i)
        figure['data'][i-1] = float(File[region[i-1]])
    figure = pd.DataFrame(figure)
    return figure


