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
from LabNLP import views
app_name='LabNLP'
urlpatterns = [
    path('', views.LabNLP,name='LabNLP'),

    path('InsertIntoDB/', views.InsertIntoDB, name='InsertIntoDB'),
    path('ThreeWord/', views.ThreeWord, name='ThreeWord'),
    path('TwoWord/', views.TwoWord, name='TwoWord'),
    path('InsertIntoDB_THREE/', views.InsertIntoDB_THREE, name='InsertIntoDB_THREE'),
    path('Select2/', views.Select2, name='Select2'),
    path('Select/', views.Select, name='Select'),
]
