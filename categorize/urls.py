"""djangoProject URL Configuration

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
from categorize import views
app_name='categorize'
urlpatterns = [
    path('', views.categorize,name='categorize'),
    path('PoolList/', views.PoolList,name='PoolList'),
    path('getCategory/', views.getCategory,name='getCategory'),
    path('add2Category/', views.add2Category,name='add2Category'),
    path('add2ConversionTable/', views.add2ConversionTable,name='add2ConversionTable'),
    path('removeList/', views.removeList,name='removeList'),
    path('comfirmList/', views.comfirmList,name='comfirmList'),
    path('confirmAndAbandon/', views.confirmAndAbandon,name='confirmAndAbandon'),
    path('getComfirmCategory/', views.getComfirmCategory,name='getComfirmCategory'),
    path('getCategoriedClass/', views.getCategoriedClass,name='getCategoriedClass'),
    path('getCategoriedList/', views.getCategoriedList,name='getCategoriedList'),

]
