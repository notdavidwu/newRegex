from django.contrib import admin
from django.urls import path
from tube2 import views
app_name='tube2'
urlpatterns = [
    path('', views.tube2,name='tube2'),
    path('TextReport/', views.TextReport,name='TextReport'),
    path('sql12/', views.sql12,name='sql12'),
    path('sqlupdate/', views.sqlupdate,name='sqlupdate'),
]