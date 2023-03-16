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
from eventDefinition import views
app_name='eventDefinition'
urlpatterns = [
    path('connsql/',views.connsql,name = 'connsql'),
    path('', views.confirm,name='confirm'),
    path('confirmpat/', views.confirmpat,name='confirmpat'),
    path('confirmpat2/',views.confirmpat2,name='confirmpat2'),
    path('Phase/',views.Phase,name='Phase'),
    path('Disease/', views.Disease, name='Disease'),
    path('updatePhase/', views.updatePhase, name='updatePhase'),
    path('updateInterval/', views.updateInterval, name='updateInterval'),
    path('searchNote/', views.searchNote, name='searchNote'),
    path('searchPhaseAndInterval/', views.searchPhaseAndInterval, name='searchPhaseAndInterval'),
    path('searchRecord/', views.searchRecord, name='searchRecord'),
    path('deleteDefinition/', views.deleteDefinition, name='deleteDefinition'),
    path('updateCancerRegist/', views.updateCancerRegist, name='updateCancerRegist'),
    path('addInducedEvent/', views.addInducedEvent, name='addInducedEvent'),
    path('updateInducedEvent/', views.updateInducedEvent, name='updateInducedEvent'),
    path('deleteEvent_F/', views.deleteEvent_F, name='deleteEvent_F'),
    path('getClinicalProcedures/', views.getClinicalProcedures, name='getClinicalProcedures'),
    path('getCancerRegistData/', views.getCancerRegistData, name='getCancerRegistData'),
    path('updatePatientStatus/', views.updatePatientStatus, name='updatePatientStatus'),
    path('getNum/', views.getNum, name='getNum'),
    path('getPatientStatus/', views.getPatientStatus, name='getPatientStatus'),
    path('formGenerator/', views.formGenerator, name='formGenerator'),
    path('insertExtractedFactors/', views.insertExtractedFactors, name='insertExtractedFactors'),
    path('searchExtractedFactorsRecord/', views.searchExtractedFactorsRecord, name='searchExtractedFactorsRecord'),
    path('updateEventConfirm/', views.updateEventConfirm, name='updateEventConfirm'),
    path('searchExtractedEventFactorCode/', views.searchExtractedEventFactorCode, name='searchExtractedEventFactorCode'),
    path('getFromStructure/', views.getFromStructure, name='getFromStructure'),
    path('updateFromStructure/', views.updateFromStructure, name='updateFromStructure'),
    path('getEventFactorCode/', views.getEventFactorCode, name='getEventFactorCode'),
    path('searchEventFactorCode/', views.searchEventFactorCode, name='searchEventFactorCode'),
    path('getNewEventFactorID/', views.getNewEventFactorID, name='getNewEventFactorID'),
    path('getSeqNoOption/', views.getSeqNoOption, name='getSeqNoOption'),
    path('addPatientDiease/', views.addPatientDiease, name='addPatientDiease'),
    path('deletelePatientDisease/', views.deletelePatientDisease, name='deletelePatientDisease'),
    path('updateDiseaseAndSeq/', views.updateDiseaseAndSeq, name='updateDiseaseAndSeq'),
    path('updateEventNote/', views.updateEventNote, name='updateEventNote'),
    path('isDone/', views.isDone, name='isDone'),
    path('getTopic/', views.getTopic, name='getTopic'),
    path('getTopicPatientNum/', views.getTopicPatientNum, name='getTopicPatientNum'),
    path('getTopicRecord/', views.getTopicRecord, name='getTopicRecord'),
    path('processCorrelationPatientListAndAnnotation/', views.processCorrelationPatientListAndAnnotation, name='processCorrelationPatientListAndAnnotation'),
    path('addTTP/', views.addTTP, name='addTTP'),
    path('batchDefinite/', views.batchDefinite, name='batchDefinite'),
    path('getExtractedFactorsRecordSeq/', views.getExtractedFactorsRecordSeq, name='getExtractedFactorsRecordSeq'),
    path('confirmDone/', views.confirmDone, name='confirmDone'),
    path('getMedtype/', views.getMedtype, name='getMedtype'),
    path('deleteExtractedFactor/', views.deleteExtractedFactor, name='deleteExtractedFactor'),
    
]
