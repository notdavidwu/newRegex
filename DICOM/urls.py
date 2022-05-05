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
from DICOM import views
app_name='DICOM'
urlpatterns = [
    path('', views.DICOM,name='DICOM'),
    path('DICOM_show/', views.DICOM_show,name='DICOM_show'),
    path('DICOM_show1/', views.DICOM_show1, name='DICOM_show1'),
    path('DICOM_show2/', views.DICOM_show2, name='DICOM_show2'),
    path('DICOM_show3/', views.DICOM_show3, name='DICOM_show3'),
    path('DICOM_show4/', views.DICOM_show4, name='DICOM_show4'),
    path('insertLocation/', views.insertLocation, name='insertLocation'),
    path('deleteLocation/', views.deleteLocation, name='deleteLocation'),
    path('selectLocation/', views.selectLocation, name='selectLocation'),
    path('convertLocation/', views.convertLocation, name='convertLocation'),
    path('findLocalMax/', views.findLocalMax, name='findLocalMax'),
    path('TextReport/', views.TextReport, name='TextReport'),
    path('load_DICOM1/', views.load_DICOM1, name='load_DICOM1'),
    path('load_DICOM/', views.load_DICOM, name='load_DICOM'),
    path('LabelGroup/', views.LabelGroup, name='LabelGroup'),
    path('LabelName/', views.LabelName, name='LabelName'),
    path('findSUV/', views.findSUV, name='findSUV'),
    path('PatientImageInfo/', views.PatientImageInfo, name='PatientImageInfo'),
    path('load_RT_DICOM/', views.load_RT_DICOM, name='load_RT_DICOM'),
    path('ROIname/', views.ROIname, name='ROIname'),
    path('DrawContour/', views.DrawContour, name='DrawContour'),
    path('RT_change/', views.RT_change, name='RT_change'),
    path('load_CT_DICOM/', views.load_CT_DICOM, name='load_CT_DICOM'),
    path('UNet/', views.UNet, name='UNet'),
    path('window_load/', views.window_load, name='window_load'),
    path('load_MRI_DICOM/', views.load_MRI_DICOM, name='load_MRI_DICOM'),
    path('SaveCoordinate/', views.SaveCoordinate, name='SaveCoordinate'),
    path('cancer/', views.cancer, name='cancer'),
    path('convert_MRI_coordinate/', views.convert_MRI_coordinate, name='convert_MRI_coordinate'),
    path('getusers/', views.getusers, name='getusers'),
    path('insertAnnotationFactor/', views.insertAnnotationFactor, name='insertAnnotationFactor'),
    path('getAnnotationFactorGroup/', views.getAnnotationFactorGroup, name='getAnnotationFactorGroup'),
    path('getAnnotationFactorDetail/', views.getAnnotationFactorDetail, name='getAnnotationFactorDetail'),
    path('getAnnotationFactor/', views.getAnnotationFactor, name='getAnnotationFactor'),
    path('updateDrConfirm/', views.updateDrConfirm, name='updateDrConfirm'),
    
]
