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
from appeal import views
app_name='appeal'
urlpatterns = [
    path('', views.appeal,name='appeal'),
    path('appeallist/', views.appeallist,name='appeallist'),
    path('appealdealwith/', views.appealdealwith,name='appealdealwith'),
    path('SearchWord/', views.SearchWord,name='SearchWord'),
    path('back_word/', views.back_word,name='back_word'),
    path('front_word/', views.front_word,name='front_word'),
    path('Schedule/', views.Schedule,name='Schedule'),
    path('update_schedule/', views.update_schedule,name='update_schedule'),
    path('select_huge_data/', views.select_huge_data,name='select_huge_data'),
    path('insert_word/', views.insert_word,name='insert_word'),
    path('question_word/', views.question_word,name='question_word'),
    
]
