"""regex URL Configuration

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
from mark.views import *
app_name = "mark"





urlpatterns = [
    path('admin/', admin.site.urls),
    path('view/', TextView),
    path('TextFormView/', TextFormView, name="TextFormView"),
    path('getVocabulary/', getVocabulary, name="getVocabulary"),
    path('insertVocabulary/', insertVocabulary, name="insertVocabulary"),
    path('inserttokenRE/', inserttokenRE, name="inserttokenRE"),
    path('inserttokenREItem/', inserttokenREItem, name="inserttokenREItem"),
    path('checkName/', checkName, name="checkName"),
    path('checkRE/', checkRE, name="checkRE"),
    path('getVocabularyByType/', getVocabularyByType, name="getVocabularyByType"),
    path('getVocabulary/', getVocabulary, name="getVocabulary"),
    path('getAnalyseText/', getAnalyseText, name="getAnalyseText"),
    path('getReportID/', getReportID, name="getReportID"),
    path('getReportText/', getReportText, name="getReportText"),
    path('getTokenREItemID/', getTokenREItemID, name="getTokenREItemID"),
    path('insertExtractedValueFromToken/', insertExtractedValueFromToken, name="insertExtractedValueFromToken"),
    path('insertVocabulary_U/', insertVocabulary_U, name="insertVocabulary_U"),
    path('getTextToken/', getTextToken, name="getTextToken"),
    path('getToken/', getToken, name="getToken"),
    path('insertTexttoken/', insertTexttoken, name="insertTexttoken"),
    path('getTextToken_3/', getTextToken_3, name="getTextToken_3"),
    path('insertTexttoken_3/', insertTexttoken_3, name="insertTexttoken_3"),
    path('getTokenIDCheckTextToken/', getTokenIDCheckTextToken, name="getTokenIDCheckTextToken"),
    path('getVocabularyByType_Ptable/', getVocabularyByType_Ptable, name="getVocabularyByType_Ptable"),
    path('getNextWord/', getNextWord, name="getNextWord"),
    path('getNextWordReport/', getNextWordReport, name="getNextWordReport"),
    
    path('', Home.as_view(),name="home"),
    path('Page2/', Page2.as_view(),name="Page2"),
    path('Merge/', Merge.as_view(),name="Merge"),
    
]