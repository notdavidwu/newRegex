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
from warehousing import views
app_name='warehousing' 
urlpatterns = [
    path('', views.warehousing,name='warehousing'),
    path('imageList/', views.imageList,name='imageList'),
    path('addPatientList/', views.addPatientList,name='addPatientList'),    
    path('disease/', views.disease,name='disease'),
    path('session/', views.session,name='session'),

]
