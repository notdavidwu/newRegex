from django.contrib import admin
from django.urls import path
from tube import views
app_name='tube'
urlpatterns = [
    path('', views.tube,name='tube'),
    path('TextReport/', views.TextReport,name='TextReport'),
    path('sql12/', views.sql12,name='sql12'),
    path('sqlupdate/', views.sqlupdate,name='sqlupdate'),
]