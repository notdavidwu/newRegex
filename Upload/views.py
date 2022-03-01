import json

from django.shortcuts import render,HttpResponse

# Create your views here.
import sys
import os
sys.path.append("C:/Users/User/PycharmProjects/AIC/函式庫")
from pydicom import dcmread
import pathlib
import numpy as np
import cv2

import datetime
from .forms import FileFieldForm
from .models import upload

'''
上傳功能簡介
因為HTML的安全性問題沒辦法獲得上傳檔案在客戶端的位置因此只能這樣做
1.上傳
    ↓
2.伺服器根目錄
    ↓
3.讀單一dicom     ←       ←       ←       ←        ←   
    ↓
4.Get Patient ID、SeriesNumber、StudyDate          ↑
    ↓
5.搬移dicom檔案，沒有資料夾的建立資料夾       →   →   →
'''

def handle_uploaded_file(f,username):
    file_name = f.name#獲得上傳來的檔名稱,加入下劃線分開日期和名稱
    folderpath = "D:/DICOM/"
    file_path= os.path.join(folderpath, file_name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_file(request):
    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')#獲得多個檔案上傳進來的檔案列表。
        username=request.POST['username']
        print(username)
        if form.is_valid():#表單資料如果合法
            for f in files:
                handle_uploaded_file(f,username)#處理上傳來的檔案
            moveDicom(username)#將檔案整理，搬移
            return render(request, 'upload/upload.html', {'form':form})
    else:
        form = FileFieldForm()
        print(form)
    request.session['test']='傳送變數'
    return render(request, 'upload/upload.html', {'form':form})

def moveDicom(username):
    MedicalRecordNumber='12345' #patient ID
    series='12345' # 病歷號從dicom解
    dicom_date='2020-09-28'
    folderpath = "D:/DICOM/"
    # 要檢查的目錄路徑
    series_path = os.path.join(folderpath, series)
    # 檢查目錄是否存在
    if not os.path.isdir(series_path):
        os.mkdir(series_path)

    dicom_date_path = os.path.join(series_path, dicom_date)
    if not os.path.isdir(dicom_date_path):
        os.mkdir(dicom_date_path)

    upload.objects.create(
        medicalRecordNumber=MedicalRecordNumber,
        dicom_date=dicom_date,
        seriesNumber=series,
        username=username,
        path=dicom_date_path,
    )