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
from PowerBI import views
app_name='PowerBI'
urlpatterns = [
    path('', views.PowerBI,name='PowerBI'),
    path('get_embed_info/', views.get_embed_info,name='get_embed_info'),
    path('get_dashboard/', views.get_dashboard,name='get_dashboard'),
    path('regist_dashboard/', views.regist_dashboard,name='regist_dashboard'),
]
