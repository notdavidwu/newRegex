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
from Classify import views
app_name='Classify'
urlpatterns = [
    path('', views.Classify,name='Classify'),
    path('WordCategory/', views.WordCategory,name='WordCategory'),
    path('Leading/', views.Leading,name='Leading'),
    path('Item2/', views.Item2,name='Item2'),
    path('MultipleWords/', views.MultipleWords,name='MultipleWords'),
    path('Sort/', views.Sort,name='Sort'),
    path('FinishSort/', views.FinishSort,name='FinishSort'),
]
