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
from Search import views
app_name='Search'
urlpatterns = [
    path('', views.Search,name='Search'),
    path('PoolList/', views.PoolList,name='PoolList'),
    path('TimeShow/', views.TimeShow,name='TimeShow'),
    path('PrimaryText/', views.PrimaryText,name='PrimaryText'),
    path('structureData/', views.structureData,name='structureData'),
    path('getWard/', views.getWard,name='getWard'),
    path('getDivName/', views.getDivName,name='getDivName'),
    path('getCategory/', views.getCategory,name='getCategory'),
    
]
