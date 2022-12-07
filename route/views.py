import os
import folium
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from show_route import settings
import requests
import urllib.request
import pandas as pd
import geopandas as gpd
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig, SymbolType
from pyecharts import options as opts
from pyecharts.charts import Bar, PictorialBar, Scatter
from pyecharts.faker import Faker

from . import getroute
from . import GetData
from . import HandleFile

data_transport = ([], [], [])
file_type = 0

def mainmap(request):
    figure = folium.Figure()
    m = folium.Map(location=[22.276548, 114.151726], zoom_start=10)
    m.add_to(figure)
    figure.render()
    context = {'map': figure}
    return render(request, 'mainmap.html', context)


def visualmap(request):
    figure = folium.Figure()
    hk_geo_data = GetData.get_data(1800)
    hk_map = folium.Map(location=[22.276548, 114.151726], zoom_start=10)
    fg1 = folium.FeatureGroup(name='Hong Kong Districts Total Population',
                              overlay=False).add_to(hk_map)
    fg2 = folium.FeatureGroup(name='Hong Kong Districts Total Older Population',
                              overlay=False).add_to(hk_map)

    total_population = folium.Choropleth(
        geo_data=hk_geo_data,
        data=hk_geo_data,
        columns=['adcode', 'population'],
        key_on='feature.properties.adcode',
        # fill_color='red',
        fill_color='YlOrRd',
        nan_fill_color="WHITE",  # Use white color if there is no data available for the county
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Total Population in Hong Kong Districts',  # title of the legend
        highlight=True,
        # overlay=False,
        line_color='black'
    ).geojson.add_to(fg1)

    folium.features.GeoJson(
        data=hk_geo_data,
        name='Hong Kong Districts Total Population',
        smooth_factor=2,
        style_function=lambda x: {'color': 'black', 'fillColor': 'transparent', 'weight': 0.5},
        tooltip=folium.features.GeoJsonTooltip(
            fields=['name',
                    'center',
                    'level',
                    'population'
                    ],
            aliases=["District Name:",
                     "District Center:",
                     "Level:",
                     "Population:"
                     ],
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800, ),
        highlight_function=lambda x: {'weight': 3, 'fillColor': 'grey'},
    ).add_to(total_population)

    total_older_population = folium.Choropleth(
        geo_data=hk_geo_data,
        data=hk_geo_data,
        columns=['adcode', 'elderly'],
        key_on='feature.properties.adcode',
        # fill_color='red',
        fill_color='YlOrRd',
        nan_fill_color="WHITE",  # Use white color if there is no data available for the county
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Total Older Population in Hong Kong Districts',  # title of the legend
        highlight=True,
        overlay=False,
        line_color='black'
    ).geojson.add_to(fg2)

    folium.features.GeoJson(
        data=hk_geo_data,
        name='Hong Kong Districts Total Older Population',
        smooth_factor=2,
        style_function=lambda x: {'color': 'black', 'fillColor': 'transparent', 'weight': 0.5},
        tooltip=folium.features.GeoJsonTooltip(
            fields=['name',
                    'center',
                    'level',
                    'population'
                    ],
            aliases=["District Name:",
                     "District Center:",
                     "Level:",
                     "Population:"
                     ],
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800, ),
        highlight_function=lambda x: {'weight': 3, 'fillColor': 'grey'},
    ).add_to(total_older_population)

    folium.TileLayer('cartodbdark_matter', overlay=True, name="View in Dark Mode").add_to(hk_map)
    folium.TileLayer('cartodbpositron', overlay=True, name="Viw in Light Mode").add_to(hk_map)
    folium.LayerControl(collapsed=False).add_to(hk_map)

    hk_map.add_to(figure)
    figure.render()
    context = {'map': figure}
    return render(request, 'visualmap.html', context)

def covidmap(request):
    figure = folium.Figure()
    hk_map_2 = folium.Map(location=[22.276548, 114.151726], zoom_start=10)

    covid = pd.read_csv('./media/final.csv')
    covid = pd.DataFrame(covid)

    hk_map_2.add_to(figure)

    # folium.Marker(
    #     location=[22.276548, 114.151726],
    #     popup='雄县',
    #     icon=folium.Icon(color='red')
    # ).add_to(hk_map_2)

    for i in range(0, 810):
        x = covid['lat'][i]
        y = covid['lng'][i]
        Msg = "Name :" + covid['building_name'][i] + "\n" + "Date: " + covid['date'][i]
        folium.Marker(
            location=[y, x],
            popup=Msg,
            # tooltip=tooltip,
            icon=folium.Icon(color='red')
        ).add_to(hk_map_2)

    hk_geo_data = GetData.get_data(1800)
    Covid_data = {"NAme": ["中西区", "湾仔区", "东区", "南区", "油尖旺区", "深水埗区", "九龙城区", "黄大仙区", "观塘区", "葵青区", "荃湾区", "屯门区", "元朗区", "北区", "大埔区", "沙田区", "西贡区", "离岛区"],
                    "CASES": [2, 4, 15, 3, 6, 15, 10, 14, 19, 17, 13, 21, 21, 26, 4, 35, 14, 5]}
    Covid_data = pd.DataFrame(Covid_data)
    hk_geo_data = pd.concat([hk_geo_data, Covid_data], axis=1)

    print(hk_geo_data)
    fg1 = folium.FeatureGroup(name='Hong Kong Districts Total Population',
                              overlay=False).add_to(hk_map_2)

    folium.Choropleth(
        geo_data=hk_geo_data,
        data=hk_geo_data,
        columns=['adcode', 'CASES'],
        key_on='feature.properties.adcode',
        # fill_color='red',
        fill_color='YlOrRd',
        nan_fill_color="WHITE",  # Use white color if there is no data available for the county
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Total Covid Related Cases Buildings in Hong Kong',  # title of the legend
        line_color='black'
    ).add_to(hk_map_2)

    hk_map_2.add_to(figure)
    figure.render()
    context = {'map': figure}
    return render(request, 'covidmap.html', context)

def showmap(request):
    return render(request, 'showmap.html')


def showroute(request, lat1, long1, lat2, long2):
    figure = folium.Figure()
    lat1, long1, lat2, long2 = float(lat1), float(long1), float(lat2), float(long2)
    route = getroute.get_route(long1, lat1, long2, lat2)

    m = folium.Map(location=[(route['start_point'][0]),
                                (route['start_point'][1])],
                       zoom_start=10)
    m.add_to(figure)
    folium.PolyLine(route['route'], weight=8, color='blue', opacity=0.6).add_to(m)
    folium.Marker(location=route['start_point'], icon=folium.Icon(icon='play', color='green')).add_to(m)
    folium.Marker(location=route['end_point'], icon=folium.Icon(icon='stop', color='red')).add_to(m)
    figure.render()

    context = {'map': figure}
    return render(request, 'showroute.html', context)


def show(request, type):
    if type == 'JSON':
        data_transport[0].clear()
        received_file = request.FILES.get("upload_file1")  # upload_name是input按钮的name，必须一样
        filename = os.path.join(settings.MEDIA_ROOT, received_file.name)

        HandleFile.saveFile(received_file, filename)
        File = json.loads(HandleFile.readFile(filename))["content"]
        # File.to_dict()
        print(File)

        thesis = File["thesis"]
        fianl_data = GetData.handel_data(File)

        for i in range(0, 18):
            data_transport[0].append(fianl_data['data'][i])

        response = requests.get("https://geo.datav.aliyun.com/areas_v3/bound/810000_full.json")
        res = response.json()
        hk_map_data = gpd.GeoDataFrame.from_features(res)
        hk_map_data.crs = 'EPSG:4326'
        hk_map_data_final = pd.concat([hk_map_data, fianl_data], axis=1)
        print(thesis)
        print(hk_map_data_final)

        # return JsonResponse({
        #     'result': 'OK',
        #     'Status': 200,
        #     'filename': received_file.name,
        #     'content': HandleFile.readFile(filename),
        # })

        figure = folium.Figure()
        m = folium.Map(location=[22.276548, 114.151726], zoom_start=10)
        folium.Choropleth(
            geo_data=hk_map_data_final,
            data=hk_map_data_final,
            columns=['adcode', 'data'],
            key_on='feature.properties.adcode',
            # fill_color='red',
            fill_color='YlOrRd',
            nan_fill_color="WHITE",  # Use white color if there is no data available for the county
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=thesis,  # title of the legend
            highlight=True,
            # overlay=False,
            line_color='black'
        ).add_to(m)
        m.add_to(figure)
        figure.render()
        context = {'map': figure}
        return render(request, 'show.html', context)
    elif type == "CSV":
        data_transport[0].clear()
        file_type = 1

        received_file = request.FILES.get("upload_file2")  # upload_name是input按钮的name，必须一样
        filename = os.path.join(settings.MEDIA_ROOT, received_file.name)
        HandleFile.saveFile(received_file, filename)
        File_csv = pd.read_csv("./media/data.csv")
        File_csv.columns = ["district", "data"]

        thesis = File_csv['data'][0]
        figure = {'Adcode': {}, 'data': {}}
        for i in range(1, 19):
            figure['Adcode'][i - 1] = str(810000 + i)
            figure['data'][i - 1] = float(File_csv['data'][i])
        figure = pd.DataFrame(figure)
        fianl_data = figure
        print(fianl_data)

        for i in range(0, 18):
            data_transport[0].append(fianl_data['data'][i])

        response = requests.get("https://geo.datav.aliyun.com/areas_v3/bound/810000_full.json")
        res = response.json()
        hk_map_data = gpd.GeoDataFrame.from_features(res)
        hk_map_data.crs = 'EPSG:4326'
        hk_map_data_final = pd.concat([hk_map_data, fianl_data], axis=1)
        print(thesis)
        print(hk_map_data_final)

        # return JsonResponse({
        #     'result': 'OK',
        #     'Status': 200,
        #     'filename': received_file.name,
        #     'content': HandleFile.readFile(filename),
        # })

        figure = folium.Figure()
        m = folium.Map(location=[22.276548, 114.151726], zoom_start=10)
        folium.Choropleth(
            geo_data=hk_map_data_final,
            data=hk_map_data_final,
            columns=['adcode', 'data'],
            key_on='feature.properties.adcode',
            # fill_color='red',
            fill_color='YlOrRd',
            nan_fill_color="WHITE",  # Use white color if there is no data available for the county
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=thesis,  # title of the legend
            highlight=True,
            # overlay=False,
            line_color='black'
        ).add_to(m)
        m.add_to(figure)
        figure.render()
        context = {'map': figure}
        return render(request, 'show.html', context)
    elif type == "XLSX":
        data_transport[0].clear()
        file_type = 2
        received_file = request.FILES.get("upload_file3")  # upload_name是input按钮的name，必须一样
        filename = os.path.join(settings.MEDIA_ROOT, received_file.name)
        HandleFile.saveFile(received_file, filename)
        File_xlsx = pd.read_excel("./media/data.xlsx")

        thesis = File_xlsx['data'][0]
        figure = {'Adcode': {}, 'data': {}}
        for i in range(1, 19):
            figure['Adcode'][i - 1] = str(810000 + i)
            figure['data'][i - 1] = float(File_xlsx['data'][i])
        figure = pd.DataFrame(figure)
        fianl_data = figure
        print(fianl_data)

        for i in range(0, 18):
            data_transport[0].append(fianl_data['data'][i])

        #print(data_transport[2])

        response = requests.get("https://geo.datav.aliyun.com/areas_v3/bound/810000_full.json")
        res = response.json()
        hk_map_data = gpd.GeoDataFrame.from_features(res)
        hk_map_data.crs = 'EPSG:4326'
        hk_map_data_final = pd.concat([hk_map_data, fianl_data], axis=1)
        print(thesis)
        print(hk_map_data_final)

        # return JsonResponse({
        #     'result': 'OK',
        #     'Status': 200,
        #     'filename': received_file.name,
        #     'content': HandleFile.readFile(filename),
        # })

        figure = folium.Figure()
        m = folium.Map(location=[22.276548, 114.151726], zoom_start=10)
        folium.Choropleth(
            geo_data=hk_map_data_final,
            data=hk_map_data_final,
            columns=['adcode', 'data'],
            key_on='feature.properties.adcode',
            # fill_color='red',
            fill_color='YlOrRd',
            nan_fill_color="WHITE",  # Use white color if there is no data available for the county
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=thesis,  # title of the legend
            highlight=True,
            # overlay=False,
            line_color='black'
        ).add_to(m)
        m.add_to(figure)
        figure.render()
        context = {'map': figure}
        return render(request, 'show.html', context)


def dynamic_data_map(request):
    return render(request, "dynamic_data_map.html")


def charts_1(request):
    charts_region = ["中西区", "湾仔区", "东区", "南区", "油尖旺区", "深水埗区", "九龙城区", "黄大仙区", "观塘区", "葵青区", "荃湾区", "屯门区", "元朗区", "北区", "大埔区", "沙田区",
     "西贡区", "离岛区"]

    #print(file_type)

    c = (
        Bar()
            .add_xaxis(charts_region)
            .add_yaxis("ppl per houses", data_transport[file_type])
            .set_global_opts(title_opts=opts.TitleOpts(title="Hong Kong Ppl per Houses"))
    )
    return HttpResponse(c.render_embed())


def charts_2(request):
    charts_region = ["中西区", "湾仔区", "东区", "南区", "油尖旺区", "深水埗区", "九龙城区", "黄大仙区", "观塘区", "葵青区", "荃湾区", "屯门区", "元朗区", "北区",
                     "大埔区", "沙田区",
                     "西贡区", "离岛区"]
    values = data_transport[0]

    #print(file_type)

    c = (
        PictorialBar()
            .add_xaxis(charts_region)
            .add_yaxis(
            "",
            values,
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=18,
            symbol_repeat="fixed",
            symbol_offset=[0, 0],
            is_symbol_clip=True,
            symbol=SymbolType.ROUND_RECT,
        )
            .reversal_axis()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Hong Kong ppl per houses"),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                ),
            ),
        )
    )
    return HttpResponse(c.render_embed())

def charts_3(request):
    charts_region = ["中西区", "湾仔区", "东区", "南区", "油尖旺区", "深水埗区", "九龙城区", "黄大仙区", "观塘区", "葵青区", "荃湾区", "屯门区", "元朗区", "北区",
                     "大埔区", "沙田区",
                     "西贡区", "离岛区"]
    values = data_transport[file_type]

    #print(file_type)

    c = (
        Scatter()
            .add_xaxis(charts_region)
            .add_yaxis("Hong Kong ppl per Houses", values)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Scatter-VisualMap(Color)"),
            visualmap_opts=opts.VisualMapOpts(min_=min(data_transport[file_type]), max_=max(data_transport[file_type])),
        )
    )

    return HttpResponse(c.render_embed())




