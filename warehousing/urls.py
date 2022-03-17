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
    path('ResearchTopic/', views.warehousing,name='ResearchTopic'),
    path('SubjectPatientList/', views.SubjectPatientList,name='SubjectPatientList'),
    path('PatientList/', views.PatientList,name='PatientList'),
    path('Session/', views.Session,name='Session'),
    path('Patient_num/', views.Patient_num,name='Patient_num'),
    path('getPreviousAction/', views.getPreviousAction,name='getPreviousAction'),
    path('Disease/', views.Disease,name='Disease'),
]
