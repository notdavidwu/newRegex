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
from django.urls import path,include
from demo import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', include('demo.urls', namespace='demo')),
    path('DICOM/', include('DICOM.urls', namespace='DICOM')),
    path('Upload/', include('Upload.urls', namespace='Upload')),
    path('pool/', include('pool.urls', namespace='pool')),
    path('confirm/', include('confirm.urls', namespace='confirm')),
    path('tube/', include('tube.urls', namespace='tube')),
    path('tube2/', include('tube2.urls', namespace='tube2')),
    path('LabNLP/', include('LabNLP.urls', namespace='LabNLP')),
    path('administrator/', include('administrator.urls', namespace='administrator')),
    path('Classify/', include('Classify.urls', namespace='Classify')),
    path('Search/', include('Search.urls', namespace='Search')),
    path('categorize/', include('categorize.urls', namespace='categorize')),
    path('poolConfirm/', include('poolConfirm.urls', namespace='poolConfirm')),
    path('warehousing/', include('warehousing.urls', namespace='warehousing')),
    path('', views.index, name="base"),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    #path('MEWS/', include('MEWS.urls', namespace='MEWS')),
    path('subjectPatientDecide/', include('subjectPatientDecide.urls', namespace='subjectPatientDecide')),
    
]
