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
from subjectPatientDecide import views
app_name='subjectPatientDecide'
urlpatterns = [
    path('', views.subjectPatientDecide,name='subjectPatientDecide'),
    path('getDisease/', views.getDisease,name='getDisease'),
    path('getImageClinicalProcedures/', views.getImageClinicalProcedures,name='getImageClinicalProcedures'),
    path('getPatient/', views.getPatient,name='getPatient'),
    path('getRegistTopicList/', views.getRegistTopicList,name='getRegistTopicList'),
    path('addCorrelationPatientListAndAnnotation/', views.addCorrelationPatientListAndAnnotation,name='addCorrelationPatientListAndAnnotation'),
    path('deleteCorrelationPatientListAndAnnotation/', views.deleteCorrelationPatientListAndAnnotation,name='deleteCorrelationPatientListAndAnnotation'),
    path('getMedType/', views.getMedType,name='getMedType'),
    path('getPatientWithMedType/', views.getPatientWithMedType,name='getPatientWithMedType'),
    path('downloadCSV/', views.downloadCSV,name='downloadCSV'),
    path('uploadCandicate/', views.uploadCandicate,name='uploadCandicate'),
    path('getPatientWithProcedure/', views.getPatientWithProcedure,name='getPatientWithProcedure'),
    path('getPatientWithMedTypeAndProcedure/', views.getPatientWithMedTypeAndProcedure,name='getPatientWithMedTypeAndProcedure'),
    
]
