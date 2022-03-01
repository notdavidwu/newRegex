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
from administrator import views
app_name='administrator'
urlpatterns = [
    path('auth_control/', views.auth_control,name='auth_control'),
    path('get_users/', views.get_users,name='get_users'),
    path('get_auth_app/', views.get_auth_app,name='get_auth_app'),
    path('upadte_auth_app/', views.upadte_auth_app,name='upadte_auth_app'),
    path('get_disease/', views.get_disease,name='get_disease'),
    path('get_auth_disease/', views.get_auth_disease,name='get_auth_disease'),
    path('upadte_auth_disease/', views.upadte_auth_disease,name='upadte_auth_disease'),
    path('get_user_setting/', views.get_user_setting,name='get_user_setting'),
    path('update_user_setting/', views.update_user_setting, name='update_user_setting'),
    path('getAuthDiseaseLabeledUser/', views.getAuthDiseaseLabeledUser, name='getAuthDiseaseLabeledUser'),
    path('insertAuthDiseaseLabeledUser/', views.insertAuthDiseaseLabeledUser, name='insertAuthDiseaseLabeledUser'),
    path('removeAuthDiseaseLabeledUser/', views.removeAuthDiseaseLabeledUser, name='removeAuthDiseaseLabeledUser'),

]
