"""show_route URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from route.views import showroute, showmap, mainmap, visualmap, show, dynamic_data_map, charts_1, charts_2, charts_3, covidmap

urlpatterns = [
    path('admin/', admin.site.urls),

    # 初始URL地址为localhost
    path('showmap/<str:lat1>,<str:long1>,<str:lat2>,<str:long2>', showroute, name='showroute'),
    path('showmap/', showmap, name='showmap'),
    path('mainmap/', mainmap, name='mainmap'),
    path('visualmap/', visualmap, name='visualmap'),
    path('covidmap/', covidmap, name='covidmap'),
    path('mainmap/show/<str:type>', show, name='show'),
    path('dynamic_data_map/', dynamic_data_map, name='dynamic'),
    path('charts_1/', charts_1, name='charts_1'),
    path('charts_2/', charts_2, name='charts_2'),
    path('charts_3/', charts_3, name='charts_3'),
    ]
    
