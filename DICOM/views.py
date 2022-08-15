import json
from datetime import datetime
from django.shortcuts import render, redirect
import shutil
# Create your views here.
import sys
import os

from scipy.fftpack import idctn
os.environ['CUDA_VISIBLE_DEVICES']="0"
import cmapy
PATH = os.getcwd()
parent_Path=os.path.abspath(os.path.join(PATH,'..'))
sys.path.append(os.path.join(parent_Path,"AIC","函式庫"))
import glob2 as glob
from readDicom import readCT, readPET
from Window import Window_FOR_VIEW, Window
import pathlib
from cv2 import applyColorMap, addWeighted, circle
import cv2
import matplotlib.pyplot as plt
from PIL.Image import fromarray
from skimage import transform
import cc3d
import h5py
import matplotlib
sys.path.append(PATH)
from MRI_CrossLink_line import MRI_CrossLink_line
from measure_Tumor import measure_Tumor
from plane3DIntersectionLine import customAPI,MRI_coordinate_API
matplotlib.use('agg')
import pydicom
import math
from numba import jit,cuda
import numpy as np
from cryptography.fernet import Fernet
from django.http import JsonResponse
from base64 import b64encode
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import codecs, json
import platform 
import tensorflow as tf
from keras import backend as K
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu,True)


def negativeTo0(number):
    if number <0:
        return 0
    else:
        return number


if len(tf.config.list_physical_devices('GPU'))>0:
    import cupy as cp
    from colormap import colormapping,GE,gray,binary
    GE = GE()
    gray = gray()
    binary = binary()
    def line(img,p1,p2,color,thinkness):
        for i in range(3):
            img[p1[1]:(p2[1]+1),p1[0]:(p2[0]+1),i]=color[i]
        return img
    def draw_line(img, x, y, plane, Ori_D):
        size = max(img.shape)
        if plane != 'Axial':
            space1 = 50
            space2 = int(50 * (img.shape[0] / Ori_D))
        else:
            space1 = 50
            space2 = 50

        img = line(img, (0, y), (negativeTo0(x - space1), y), (255, 0, 0), 1)
        img = line(img, (x + space1, y), (x + size, y), (255, 0, 0), 1)
        img = line(img, (x, 0), (x, negativeTo0(y - space2)), (255, 0, 0), 1)
        img = line(img, (x, y + space2), (x, y + size), (255, 0, 0), 1)
        #img = circle(img, (x, y), 1, (255, 0, 0), -1)
        return img.astype(np.uint8)
else:
    from colormap import GE_color_opencv
    GE = GE_color_opencv()
    gray = cmapy.cmap('gray')
    binary = cmapy.cmap('binary')
    cp=np
    from cv2 import line 
    colormapping=applyColorMap
    def draw_line(img, x, y, plane, Ori_D):
        size = max(img.shape)
        if plane != 'Axial':
            space1 = 50
            space2 = int(50 * (img.shape[0] / Ori_D))
        else:
            space1 = 50
            space2 = 50
        img = line(img, (0, y), (x - space1, y), (255, 0, 0), 1)
        img = line(img, (x + space1, y), (x + size, y), (255, 0, 0), 1)
        img = line(img, (x, 0), (x, y - space2), (255, 0, 0), 1)
        img = line(img, (x, y + space2), (x, y + size), (255, 0, 0), 1)
        #img = circle(img, (x, y), 1, (255, 0, 0), -1)
        return img.astype(np.uint8)
    
def to_image(numpy_img):
    img = fromarray(numpy_img)
    return img

@csrf_exempt
def researchTopic(request):
    query = '''select * from researchTopic'''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query)
    topicNo = []
    topicName = []
    res = cursor.fetchall()
    for row in res:
        topicNo.append(row[0])
        topicName.append(row[1])
    return JsonResponse({'topicNo': topicNo,'topicName': topicName})

@csrf_exempt
def DICOM(request):
    SeriesIdIndex = {'1': 0, '2': 0, '3': 0, '4': 0}
    
    request.session['unet_contour_1']=[]
    request.session['unet_contour_2']=[]
    request.session['unet_contour_3']=[]
    request.session['unet_contour_4']=[]


    if request.session.get('PID',0) != 0 : 
        PID = request.session.get('PID',0)
    else : 
        return redirect('/')

    MedExecTime = request.session.get('MedExecTime', 0)
    if request.session.get('Item',0) != 0 : 
        Item = request.session.get('Item',0).replace(' ','')
    else : 
        return redirect('/')
    de_identification = request.session.get('de_identification')
    
    StudyID = request.session.get('StudyID', 0)
    SeriesID = request.session.get('SeriesID', 0)
    SeriesDes = request.session.get('SeriesDes', 0)
    viewplane = request.session.get('viewplane', 0)

    Disease = request.session.get('Disease', 0)
    request.session['SeriesIdIndex'] = SeriesIdIndex
    au = request.session.get('au')

    return render(request, 'DICOM/DICOM.html',
                  {'de_identification':de_identification,'PID': PID, 'MedExecTime': MedExecTime, 'Item': Item, 'StudyID': StudyID, 'SeriesID': SeriesID,'SeriesDes':SeriesDes,'viewplane':viewplane,'Disease':Disease,'au':au})




def to_data_uri(pil_img):
    data = BytesIO()
    pil_img.save(data, "png")  # pick your format
    data64 = b64encode(data.getvalue())
    return u'data:img/png;base64,' + data64.decode('UTF-8')


def convert(x, y, z, Ori_W, Ori_H, Ori_D, plane, width, height):
    if plane == "Axial":
        x = round(x * (Ori_W / width))
        y = round(y * (Ori_H / height))
        x = x
        y = y
    elif plane == 'Coronal':
        x = round(x * (Ori_W / width))
        temp = y
        y = z
        z = round(temp * (Ori_D / height))

    elif plane == 'Sagittal':
        temp = x
        x = z
        z = round(y * (Ori_D / height))
        y = round(temp * (Ori_W / width))

    return x, y, z

@csrf_exempt
def convert_MRI_coordinate(request):
    imageType = str(request.POST.get('imageType'))
    source = request.POST.get('source',0)
    target = request.POST.get('target',0)
    source = request.POST.get('source',0)
    x = int(request.POST.get('x',0))
    y = int(request.POST.get('y',0))
    z = int(request.POST.get('z',0))
    ind = int(request.POST.get('ind',0))

    source_position = list(request.session.get('ImagePosition_'+source))[z]
    
    target_position = request.session.get('ImagePosition_'+target)
    source_orientation = request.session.get('ImageOrientation_'+source)[z]
    target_orientation = request.session.get('ImageOrientation_'+target)[0]
    source_pixelSpacing = request.session.get('MRI_pixelspacing_'+source)
    target_pixelSpacing = request.session.get('MRI_pixelspacing_'+target)
    source_shape = request.session.get('source_size'+source)
    target_shape = request.session.get('source_size'+target)

    target_position = np.array(target_position)

    #x,y,z = MRI_coordinate_API(source_position, source_orientation, target_position, target_orientation, source_pixelSpacing, target_pixelSpacing, source_shape, target_shape,x,y)

    coordinate = MRI_coordinate_API(source_position, source_orientation, target_position, target_orientation, source_pixelSpacing, target_pixelSpacing, source_shape, target_shape,x,y)

    if np.sum(np.array(coordinate)) !=-3:
        x,y,z=coordinate
    else:
        x,y= -999,-999
    return JsonResponse({'ind':ind,'x': x,'y':y,'z':z}, status=200)

def convert2draw(x, y, Ori_W, Ori_H, Ori_D, plane, width, height):
    if plane != "Axial":
        x = round(x * (Ori_W / width))
        y = round(y * (Ori_D / height))
    else:
        x = round(x * (Ori_W / width))
        y = round(y * (Ori_H / height))
    return x, y

def searchFilePath(chartNo,eventDate,studyID,seriesID):
    cursor = connections['practiceDB'].cursor()
    searchQuery='''
    SELECT [filePath]  FROM examStudy AS a
    INNER JOIN examSeries AS b on a.storageID=b.storageID
    WHERE [chartNo]=%s and [studyDate]=%s and [studyID]=%s and [seriesID]=%s
    '''
    cursor.execute(searchQuery,[chartNo,eventDate,studyID,seriesID])
    filePath = cursor.fetchall()[0][0]
    return filePath
@csrf_exempt
def load_DICOM(request):

    #PID = fernet.decrypt(request.POST.get('PID').encode()).decode()
    PID = request.POST.get('PID')
    MedExecTime = request.POST.get('MedExecTime')
    StudyIDText = request.POST.get('StudyIDText')
    SeriesIDText = request.POST.get('SeriesIDText')

    filePath = searchFilePath(PID,MedExecTime,StudyIDText,SeriesIDText)
    if platform.system()!='Windows':
        dir = os.path.join('/home','user','netapp',filePath)
    else:
        dir= os.path.join('//172.31.6.6/share1/NFS/image_v2',filePath)

    fileDir = dir.replace('-', '')
    fileDir = fileDir.replace(' ', '')
    
    WindowNo = str(1) if (str(request.POST.get('WindowNo')) == 'None') else str(request.POST.get('WindowNo'))
    request.session['Category_' + WindowNo] = 'PET'
    SeriesIdIndex = request.session.get('SeriesIdIndex')
    SeriesIdIndex.update({str(WindowNo): (str(StudyIDText)+'_'+str(SeriesIDText))})
    request.session['SeriesIdIndex'] = SeriesIdIndex

    tempPath = list(pathlib.Path(fileDir).glob('*PETCT.h5'))
    paths = sorted([os.path.join(filename) for filename in tempPath])[0]
    request.session['PET_' + WindowNo] = paths
    with h5py.File(paths, "r") as f:
        a_group_key = list(f.keys())
        headers = f['CT_header']
        request.session['CT_pixelspacing_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[0]).PixelSpacing[0])
        request.session['CT_slicethickness_' + WindowNo] = float(pydicom.dataset.Dataset.from_json(headers[1]).SliceThickness)
        request.session['CT_dlta_Z_' + WindowNo] = abs(float(pydicom.dataset.Dataset.from_json(headers[1]).ImagePositionPatient[2])-float(pydicom.dataset.Dataset.from_json(headers[2]).ImagePositionPatient[2]))
        request.session['CT_D_' + WindowNo] = f['CT_vol'].shape[0]
        request.session['CT_H_' + WindowNo] = f['CT_vol'].shape[1]
        request.session['CT_W_' + WindowNo] = f['CT_vol'].shape[2]

        headers = f['PET_header']
        request.session['PET_pixelspacing_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[0]).PixelSpacing[0])
        request.session['PET_slicethickness_' + WindowNo] = float(pydicom.dataset.Dataset.from_json(headers[1]).SliceThickness)
        request.session['PET_dlta_Z_' + WindowNo] = round(abs(float(pydicom.dataset.Dataset.from_json(headers[1]).ImagePositionPatient[2])-float(pydicom.dataset.Dataset.from_json(headers[2]).ImagePositionPatient[2])),3)
        request.session['PET_D_' + WindowNo] = f['PET_vol'].shape[0]
        request.session['PET_H_' + WindowNo] = f['PET_vol'].shape[1]
        request.session['PET_W_' + WindowNo] = f['PET_vol'].shape[2]

    fileExt = "*PETCTmod*.h5"
    tempPath = list(pathlib.Path(fileDir).glob(fileExt))
    paths = sorted([os.path.join(filename) for filename in tempPath])
    request.session['PET_view_' + WindowNo] = paths

    with h5py.File(list(filter(lambda path: 'Axial' in path, paths))[0], "r") as f:
        headers = f['CT_header']
        request.session['CT_view_pixelspacing_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[0]).PixelSpacing[0])
        request.session['CT_view_ImagePositionPatient_F_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[0]).ImagePositionPatient[2])
        request.session['CT_view_ImagePositionPatient_S_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[1]).ImagePositionPatient[2])
        request.session['view_D_' + WindowNo] = f['PETCT_vol'][:,0].shape[0]
        request.session['view_H_' + WindowNo] = f['PETCT_vol'][:,0].shape[1]
        request.session['view_W_' + WindowNo] = f['PETCT_vol'][:,0].shape[2]
        

    return JsonResponse({}, status=200)


@csrf_exempt
def load_RT_DICOM(request):

    #PID = fernet.decrypt(request.POST.get('PID').encode()).decode()
    PID = request.POST.get('PID')
    MedExecTime = request.POST.get('MedExecTime')
    StudyIDText = request.POST.get('StudyIDText')
    SeriesIDText = request.POST.get('SeriesIDText')

    filePath = searchFilePath(PID,MedExecTime,StudyIDText,SeriesIDText)

    if platform.system()!='Windows':
        dir = os.path.join('/home','user','netapp',filePath)
    else:
        dir= os.path.join('//172.31.6.6/share1/NFS/image_v2',filePath)

    fileDir = dir.replace('-', '')
    fileDir = fileDir.replace(' ', '')
    
    WindowNo = str(1) if (str(request.POST.get('WindowNo')) == 'None') else str(request.POST.get('WindowNo'))
    request.session['Category_' + WindowNo] = 'RT'
    SeriesIdIndex = request.session.get('SeriesIdIndex')
    SeriesIdIndex.update({str(WindowNo): (str(StudyIDText)+'_'+str(SeriesIDText))})
    request.session['SeriesIdIndex'] = SeriesIdIndex

    fileExt = "*RTCT*.h5"
    tempPath = list(pathlib.Path(fileDir).glob(fileExt))
    paths = sorted([os.path.join(filename) for filename in tempPath])

    request.session['CT_view_' + WindowNo] = paths
    with h5py.File(list(filter(lambda path: 'Axial' in path, paths))[0], "r") as f:
        headers = f['header']
        request.session['CT_view_pixelspacing_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[0]).PixelSpacing[0])
        request.session['CT_view_slicethickness_' + WindowNo] = float(pydicom.dataset.Dataset.from_json(headers[1]).SliceThickness)
        request.session['CT_view_delta_Z_' + WindowNo] = (abs(float(pydicom.dataset.Dataset.from_json(headers[1]).ImagePositionPatient[2])-float(pydicom.dataset.Dataset.from_json(headers[2]).ImagePositionPatient[2])))
        request.session['CT_view_ImagePositionPatient_F_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[0]).ImagePositionPatient[2])
        request.session['CT_view_ImagePositionPatient_S_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[1]).ImagePositionPatient[2])
        request.session['view_D_' + WindowNo] = f['vol'].shape[0]
        request.session['view_H_' + WindowNo] = f['vol'].shape[1]
        request.session['view_W_' + WindowNo] = f['vol'].shape[2]
        ROI = pydicom.dataset.Dataset.from_json(f['rtss_header'][()])

    request.session['ROI_index_'+WindowNo] = -1
    request.session['ROIname_'+WindowNo] = [ROI.StructureSetROISequence[i].ROIName for i in range(len(ROI.StructureSetROISequence))]
    
   
    Color=[]
    for ROIContourSequence in ROI.ROIContourSequence:
        try:
            Color.append(list(np.array(ROIContourSequence[0x3006, 0x002a].value, dtype='float')))
        except:
            Color.append([255.0,0.0,0.0])
    
    request.session['Color_'+WindowNo] = Color
    return JsonResponse({}, status=200)


@csrf_exempt
def load_CT_DICOM(request):

    #PID = fernet.decrypt(request.POST.get('PID').encode()).decode()
    PID = request.POST.get('PID')
    MedExecTime = request.POST.get('MedExecTime')
    StudyIDText = request.POST.get('StudyIDText')
    SeriesIDText = request.POST.get('SeriesIDText')
    filePath = searchFilePath(PID,MedExecTime,StudyIDText,SeriesIDText)
    if platform.system()!='Windows':
        dir = os.path.join('/home','user','netapp',filePath)
    else:
        dir= os.path.join('//172.31.6.6/share1/NFS/image_v2',filePath)

    fileDir = dir.replace('-', '')
    fileDir = fileDir.replace(' ', '')
    
    WindowNo = str(1) if (str(request.POST.get('WindowNo')) == 'None') else str(request.POST.get('WindowNo'))
    request.session['Category_' + WindowNo] = 'CT'
    SeriesIdIndex = request.session.get('SeriesIdIndex')
    SeriesIdIndex.update({str(WindowNo): (str(StudyIDText)+'_'+str(SeriesIDText))})
    request.session['SeriesIdIndex'] = SeriesIdIndex

    fileExt = "*CT*.h5"
    tempPath = list(pathlib.Path(fileDir).glob(fileExt))
    paths = sorted([os.path.join(filename) for filename in tempPath])
    request.session['CT_view_' + WindowNo] = paths
    with h5py.File(list(filter(lambda path: 'Axial' in path, paths))[0], "r") as f:
        headers = f['header']
        request.session['CT_view_pixelspacing_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[0]).PixelSpacing[0])
        request.session['CT_view_slicethickness_' + WindowNo] = float(pydicom.dataset.Dataset.from_json(headers[1]).SliceThickness)
        request.session['CT_view_delta_Z_' + WindowNo] = (abs(float(pydicom.dataset.Dataset.from_json(headers[1]).ImagePositionPatient[2])-float(pydicom.dataset.Dataset.from_json(headers[2]).ImagePositionPatient[2])))
        request.session['view_D_' + WindowNo] = f['vol'].shape[0]
        request.session['view_H_' + WindowNo] = f['vol'].shape[1]
        request.session['view_W_' + WindowNo] = f['vol'].shape[2]

    return JsonResponse({}, status=200)

@csrf_exempt
def load_MRI_DICOM(request):

    #PID = fernet.decrypt(request.POST.get('PID').encode()).decode()
    PID = request.POST.get('PID')
    MedExecTime = request.POST.get('MedExecTime')
    StudyIDText = request.POST.get('StudyIDText')
    SeriesIDText = request.POST.get('SeriesIDText')
    filePath = searchFilePath(PID,MedExecTime,StudyIDText,SeriesIDText)
    if platform.system()!='Windows':
        dir = os.path.join('/home','user','netapp',filePath)
    else:
        dir= os.path.join('//172.31.6.6/share1/NFS/image_v2',filePath)

    fileDir = dir.replace('-', '')
    fileDir = fileDir.replace(' ', '')
    
    WindowNo = str(1) if (str(request.POST.get('WindowNo')) == 'None') else str(request.POST.get('WindowNo'))
    request.session['Category_' + WindowNo] = 'MRI'
    SeriesIdIndex = request.session.get('SeriesIdIndex')
    SeriesIdIndex.update({str(WindowNo): (str(StudyIDText)+'_'+str(SeriesIDText))})
    request.session['SeriesIdIndex'] = SeriesIdIndex

    fileExt = "*MRI*.h5"
    tempPath = list(pathlib.Path(fileDir).glob(fileExt))
    paths = sorted([os.path.join(filename) for filename in tempPath])
    request.session['MRI_' + WindowNo] = paths
    with h5py.File(paths[0], "r") as f:
        headers = f['header']
        request.session['MRI_pixelspacing_' + WindowNo] = float(pydicom.dataset.Dataset.from_json(headers[0]).PixelSpacing[0])

        request.session['MRI_slicethickness_' + WindowNo] = float(pydicom.dataset.Dataset.from_json(headers[1]).SliceThickness)
        MRIWC = []
        MRIWW = []
        MRI_ImagePosition = []
        MRI_ImageOrientation = []
        for header in headers:
            if type(pydicom.dataset.Dataset.from_json(header)['0028', '1050'].value) is list:
                MRIWC.append(float(pydicom.dataset.Dataset.from_json(header)['0028', '1050'].value[0])) 
                MRIWW.append(float(pydicom.dataset.Dataset.from_json(header)['0028', '1051'].value[0])) 
            else:
                MRIWC.append(float(pydicom.dataset.Dataset.from_json(header)['0028', '1050'].value)) 
                MRIWW.append(float(pydicom.dataset.Dataset.from_json(header)['0028', '1051'].value)) 
            MRI_ImagePosition.append(list(pydicom.dataset.Dataset.from_json(header)['0020', '0032'].value))
            MRI_ImageOrientation.append(list(pydicom.dataset.Dataset.from_json(header)['0020', '0037'].value)) 

        request.session['view_D_' + WindowNo] = f['vol'].shape[0]
        request.session['view_H_' + WindowNo] = f['vol'].shape[1]
        request.session['view_W_' + WindowNo] = f['vol'].shape[2]
        request.session['source_size' +str(MedExecTime)+str(StudyIDText)+str(SeriesIDText)] = f['vol'].shape[1:3]
        request.session['ImagePosition_'+str(MedExecTime)+str(StudyIDText)+str(SeriesIDText)] = MRI_ImagePosition
        request.session['ImageOrientation_'+str(MedExecTime)+str(StudyIDText)+str(SeriesIDText)] = MRI_ImageOrientation
        request.session['MRI_pixelspacing_' + str(MedExecTime)+str(StudyIDText)+str(SeriesIDText)] = float(pydicom.dataset.Dataset.from_json(headers[0]).PixelSpacing[0])
    return JsonResponse({'MRIWC':MRIWC,'MRIWW':MRIWW}, status=200)



@csrf_exempt
def load_DICOM1(request):
    global CT, PET, CT_tag, PET_tag, CT_view, PET_view, CT_view_tag, PET_view_tag
    dir = request.POST.get('path')

    # dir = 'D:\\to大益\\HNC-不同張數\\11964\\1.2.410.200010.886.1317040011.1450101100.4905.5.60545182'
    fileDir = dir
    fileExt = r"**\*.dcm"
    tempPath = list(pathlib.Path(fileDir).glob(fileExt))
    paths = sorted([
        os.path.join(filename)
        for filename in tempPath
    ])
    folders = np.unique(sorted([
        os.path.join(filename.parent)
        for filename in tempPath
    ]))
    filenames = sorted([
        os.path.join(filename.name)
        for filename in tempPath
    ])
    file = [FilePath for FilePath in paths if folders[0] in FilePath]
    CT_path = [CT_path for CT_path in file if
               'CT' in CT_path.split('\\')[-1] and 'adjustment' in CT_path.split('\\')[-1]]
    PET_path = [PET_path for PET_path in file if 'PT' in PET_path.split('\\')[-1]]
    CT, CT_tag = readCT(CT_path)
    PET, PET_tag = readPET(PET_path)
    # CT = CT_Change(CT, CT_tag['PixelSpacing'], PET, PET_tag['PixelSpacing'])
    PET_view = transform.resize(PET, (CT.shape), order=3, mode='constant', cval=0)
    # return CT, PET, CT_tag, PET_tag, PET_view

    return JsonResponse({}, status=200)


@csrf_exempt
def DICOM_show(request):
    CT_view = request.session.get('CT_view_1')
    z = request.session.get('CT_view_D_1')
    CTimg = Window_FOR_VIEW(np.array(h5py.File(CT_view, "r")['vol'][0, :, :]), 35, 350)
    colormap = plt.get_cmap('gray')
    CTimg = colormap(CTimg)
    CTimg = (CTimg[:, :, :3] * 255).astype(np.uint8)
    CTpil_image = to_image(CTimg)
    CTimage_uri = to_data_uri(CTpil_image)

    # return render(request, 'DICOM/DICOM.html', {'dicom_url': CTimage_uri, 'z': json.dumps(CT.shape[2])})
    return JsonResponse({"dicom_url": CTimage_uri, 'z': z}, status=200)


def localmax(CT_D, CT_H, CT_W, PET, CT_mod_x, CT_mod_y, CT_mod_z, PET_PixelSpacing, PET_SliceThickness, PETWC,Category):

    PET = np.array(h5py.File(PET, "r")['PET_vol'])
    
    maxValue = []
    Rx = []
    Ry = []
    Rz = []
    distance = []
    PET_H = PET.shape[1]
    PET_W = PET.shape[2]
    PET_D = PET.shape[0]

    CT_H = CT_H  # CT_mod
    CT_W = CT_W
    CT_D = CT_D
    PET_PS = PET_PixelSpacing
    PET_TH = PET_SliceThickness
    RegionSize = float(70 / 2)  # 挖7公分的區域
    PET_RegionSize = math.floor(RegionSize / PET_PS) + 1  # 轉換成pixel尺度
    PET_RegionSize_D = math.floor(RegionSize / PET_TH) + 1
    PET_X = math.floor(CT_mod_x * (PET_W / CT_W))
    PET_Y = math.floor(CT_mod_y * (PET_H / CT_H))
    PET_Z = math.floor(CT_mod_z * (PET_D / CT_D))

    PET_X_UpperBound = PET_X + PET_RegionSize
    PET_X_LowerBound = PET_X - PET_RegionSize
    PET_Y_UpperBound = PET_Y + PET_RegionSize
    PET_Y_LowerBound = PET_Y - PET_RegionSize
    PET_Z_UpperBound = PET_Z + PET_RegionSize_D
    PET_Z_LowerBound = PET_Z - PET_RegionSize_D
    len = 1
    for z in range(PET_Z_LowerBound, PET_Z_UpperBound + 1):
        for y in range(PET_Y_LowerBound, PET_Y_UpperBound + 1):
            for x in range(PET_X_LowerBound, PET_X_UpperBound + 1):
                if z >= 0 and y >= 0 and x >= 0 and z < PET_D and y < PET_H and x < PET_W:
                    tz = (PET_Z - z) * PET_TH  # 歐式距離
                    ty = (PET_Y - y) * PET_PS
                    tx = (PET_X - x) * PET_PS
                    
                    if math.sqrt(math.pow(tz, 2) + math.pow(ty, 2) + math.pow(tx, 2)) <= RegionSize:  # 確認是否在有效半徑內
                        area_max = True

                        for i in range(len * -1, len + 1):
                            for j in range(len * -1, len + 1):
                                for k in range(len * -1, len + 1):
                                    if ((abs(i) + abs(j) + abs(k)) < 3):
                                        pz = z + i
                                        py = y + j
                                        px = x + k
                                        if pz >= 0 and py >= 0 and px >= 0 and pz < PET_D and py < PET_H and px < PET_W:
                                            if PET[z, y, x] < PET[pz, py, px]:
                                                area_max = False
                        if area_max:
                            maxValue.append(PET[z, y, x])
                            Rx.append(x)
                            Ry.append(y)
                            Rz.append(z)

    x = np.ceil(np.array(Rx) / (PET_W / CT_W))
    y = np.ceil(np.array(Ry) / (PET_H / CT_H))
    z = np.ceil(np.array(Rz) / (PET_D / CT_D))
    maxValue = np.array(maxValue, dtype='float')
    SortIndex = (-maxValue).argsort()
    x = x[SortIndex]
    y = y[SortIndex]
    z = z[SortIndex]
    maxValue = maxValue[SortIndex]

    RemoveIndex = maxValue >= PETWC
    if sum(RemoveIndex) != 0:
        x = list(x[RemoveIndex])
        y = list(y[RemoveIndex])
        z = list(z[RemoveIndex])
        maxValue = list(maxValue[RemoveIndex])
    else:
        x = [CT_mod_x]
        y = [CT_mod_y]
        z = [CT_mod_z]
        maxValue = [float(PET[PET_Z, PET_Y, PET_X])]

    return x, y, z, maxValue


def _localmax(CT, PET, Ox, Oy, Oz, PET_tag, PETWC):
    maxValue = []
    Rx = []
    Ry = []
    Rz = []
    distance = []
    PET_H = PET.shape[0]
    PET_W = PET.shape[1]
    PET_D = PET.shape[2]
    CT_H = CT.shape[0]
    CT_W = CT.shape[1]
    CT_D = CT.shape[2]
    PET_SP = float(PET_tag[0].PixelSpacing[0])
    PET_TH = float(PET_tag[0].SliceThickness)
    RegionSize = 70 / 2  # 挖7公分的區域
    PET_RegionSize = round(RegionSize / PET_SP)  # 轉換成pixel尺度
    PET_RegionSize_D = round(RegionSize / PET_TH)

    PET_X = round(Ox * (PET_W / CT_W))
    PET_Y = round(Oy * (PET_H / CT_H))
    PET_Z = round(Oz * (PET_D / CT_D))
    PET_X_UpperBound = PET_X + PET_RegionSize
    PET_X_LowerBound = PET_X - PET_RegionSize
    PET_Y_UpperBound = PET_Y + PET_RegionSize
    PET_Y_LowerBound = PET_Y - PET_RegionSize
    PET_Z_UpperBound = PET_Z + PET_RegionSize_D
    PET_Z_LowerBound = PET_Z - PET_RegionSize_D
    PET_PreConnectedComponent = PET[PET_Y_LowerBound:PET_Y_UpperBound, PET_X_LowerBound:PET_X_UpperBound,
                                PET_Z_LowerBound:PET_Z_UpperBound]

    PET_PreConnectedComponent = PET_PreConnectedComponent
    PET_PreConnectedComponent_Binary = PET_PreConnectedComponent.copy()
    PET_PreConnectedComponent_Binary[PET_PreConnectedComponent_Binary < float(PETWC)] = 0
    PET_PreConnectedComponent_Binary[PET_PreConnectedComponent_Binary >= float(PETWC)] = 1
    PET_PreConnectedComponent_Binary = PET_PreConnectedComponent_Binary.astype('int')
    connectivity = 18  # only 4,8 (2D) and 6, 18, and 26 (3D) are allowed
    labels_out = cc3d.connected_components(PET_PreConnectedComponent_Binary, connectivity=connectivity)

    for i in np.unique(labels_out):
        VM = PET_PreConnectedComponent[labels_out == i].max()
        Region = np.where(labels_out == i)
        maxValue.append(VM)
        maxPosition = np.where(PET_PreConnectedComponent == VM)
        Tx = maxPosition[1][0] + PET_X_LowerBound
        Ty = maxPosition[0][0] + PET_Y_LowerBound
        Tz = maxPosition[2][0] + PET_Z_LowerBound
        Rx.append(Tx)
        Ry.append(Ty)
        Rz.append(Tz)
        tempDistance = []
        for j in range(len(Region[0])):
            Jy = Region[0][j] + PET_Y_LowerBound
            Jx = Region[1][j] + PET_X_LowerBound
            Jz = Region[2][j] + PET_Z_LowerBound
            tempDistance.append(abs(Jx - PET_X) + abs(Jy - PET_Y) + abs(Jz - PET_Z))

        distance.append(min(tempDistance))

    # index=np.argmin(distance)
    # maxValue=maxValue[index]
    # x = round(Rx[index] / (PET_W / CT_W))
    # y = round(Ry[index] / (PET_H / CT_H))
    # z = round(Rz[index] / (PET_D / CT_D))

    x = np.round(np.array(Rx) / (PET_W / CT_W))
    y = np.round(np.array(Ry) / (PET_H / CT_H))
    z = np.round(np.array(Rz) / (PET_D / CT_D))
    maxValue = np.array(maxValue, dtype='float')

    SortIndex = (-maxValue).argsort()

    x = x[SortIndex]
    y = y[SortIndex]
    z = z[SortIndex]
    maxValue = maxValue[SortIndex]
    RemoveIndex = maxValue >= PETWC
    x = list(x[RemoveIndex])
    y = list(y[RemoveIndex])
    z = list(z[RemoveIndex])
    maxValue = list(maxValue[RemoveIndex])
    return x, y, z, maxValue


def slicing(plane, img_path, variable, drawActualCoordinates, WC, WW, y, tag, catergory):
    
    if variable is None:variable = 0
    if catergory =='PET':
        img_path = list(filter(lambda x: plane in x, img_path))[0]
        img = cp.array(h5py.File(img_path, "r")['PETCT_vol'][variable, :, :, :])
        PETimg = Window_FOR_VIEW(img[0], WC['PET'], WW['PET'])
        CTimg = Window_FOR_VIEW(img[1], WC['CT'], WW['CT'])
        img = cp.stack((PETimg,CTimg),axis=0)
    elif catergory =='MRI':
        img_path = img_path[0]
        img = Window_FOR_VIEW(cp.array(h5py.File(img_path, "r")['vol'][variable, :, :]), WC[catergory], WW[catergory])
    else:
        img_path = list(filter(lambda x: plane in x, img_path))[0]
        img = Window_FOR_VIEW(cp.array(h5py.File(img_path, "r")['vol'][variable, :, :]), WC[catergory], WW[catergory])
    if plane == 'Axial':
        z = tag['D']
    elif plane == 'Coronal':
        if drawActualCoordinates == 'true':
            y = y
        z = tag['H']
    elif plane == 'Sagittal':
        if drawActualCoordinates == 'true':
            y =  y
        z = tag['W']

    return img, y, z


def processing_CT(CT, variable,  WC, WW, plane, x, y, height, drawActualCoordinates, CT_tag,contour_list,Category):
    CTimg, y, z = slicing(plane, CT, variable, drawActualCoordinates,  WC, WW, y, CT_tag,Category)
    resize_shape = CTimg.shape[0:2]
    ratio = (float(CT_tag['SliceThickness']) * resize_shape[0]) / (resize_shape[1] * float(CT_tag['PixelSpacing']))
    CTpil_image = colormapping(CTimg, gray)
    CTpil_image = draw_line(CTpil_image.get(), x, y, plane, height)
    if len(contour_list)!=0:
        CTpil_image=segmentation(CTpil_image,contour_list,variable,plane)
    CTpil_image = to_image(CTpil_image)
    CTimage_uri = to_data_uri(CTpil_image)
    dicom_url = CTimage_uri
    return dicom_url, z, ratio

def segmentation(img,contour_list,variable,plane):
    matched = [match for match in contour_list if plane in match]
    
    for filepath in matched:
        f = h5py.File(filepath, "r")
        if str(variable) in list(f.keys()):
            contour=json.loads(f[str(variable)][()])
            for i in list(contour.keys()):
                cv2.drawContours(img, [np.array(contour[i],dtype='int')], 0, (0, 255, 0), thickness=1)
    return img

def processing_RT(img_path, variable,  WC, WW, plane, x, y, height, drawActualCoordinates, CT_tag, Color,
                  ROI_checked, catergory):
    CTimg, y, z = slicing(plane, img_path, variable, drawActualCoordinates,  WC, WW, y, CT_tag, catergory)
    resize_shape = CTimg.shape[0:2]
    ratio = (float(CT_tag['SliceThickness']) * resize_shape[0]) / (resize_shape[1] * float(CT_tag['PixelSpacing']))
    CTpil_image = colormapping(CTimg, gray).astype(np.uint8)
    CTpil_image = draw_line(CTpil_image.get(), x, y, plane, height)
    
    if(ROI_checked!=-1):
        CTpil_image = rt_contour(CTpil_image, ROI_checked, Color, list(filter(lambda x: plane in x, img_path))[0], variable,plane)

    CTpil_image = to_image(CTpil_image)
    CTimage_uri = to_data_uri(CTpil_image)
    dicom_url = CTimage_uri
    return dicom_url, z, ratio


def processing_PET( PET_view, variable, WC, WW, plane, mode, x, y, height,
                   drawActualCoordinates,
                   CT_tag, PET_tag,Category):
    
    img, y, z = slicing(plane,PET_view , variable, drawActualCoordinates, WC, WW, y, CT_tag,Category)
    PETimg=img[0]
    CTimg=img[1]
    resize_shape = CTimg.shape[0:2]
    ratio = (float(PET_tag['SliceThickness']) * resize_shape[0]) / (resize_shape[1] * float(CT_tag['PixelSpacing']))
    CTpil_image = colormapping(CTimg, gray)
    PETpil_image = colormapping(PETimg, binary)
    
    if mode == 'CT':
        CTpil_image = draw_line(CTpil_image.get(), x, y, plane, height)
        CTpil_image = to_image(CTpil_image)
        CTimage_uri = to_data_uri(CTpil_image)
        dicom_url = CTimage_uri
    elif mode == 'PET':
        PETpil_image = draw_line(PETpil_image.get(), x, y, plane, height)
        PETpil_image = to_image(PETpil_image)
        PETimage_uri = to_data_uri(PETpil_image)
        dicom_url = PETimage_uri
    elif mode == 'Fusion':
        CTpil_image = draw_line(CTpil_image.get(), x, y, plane, height)
        PET2Fusion = PETimg
        Fusionimg = colormapping(PET2Fusion, GE)
        Fusionimg = draw_line(Fusionimg.get(), x, y, plane, height)
        Fusionimg = addWeighted(Fusionimg, 0.5, CTpil_image, 0.5, 0)
        Fusionimg = to_image(Fusionimg)
        Fusionimage = Fusionimg
        Fusionimage_uri = to_data_uri(Fusionimage)
        dicom_url = Fusionimage_uri
    return dicom_url, z, ratio

def processing_MRI(MRI, variable,  WC, WW, plane, x, y, height, drawActualCoordinates, MRI_tag,Category,request,source,target,source_variable,MRI_CrossLink):
    MRIimg, y, z = slicing(plane, MRI, variable, drawActualCoordinates,  WC, WW, y, MRI_tag,Category)
    resize_shape = MRIimg.shape[0:2]
    ratio = (float(MRI_tag['SliceThickness']) * resize_shape[0]) / (resize_shape[1] * float(MRI_tag['PixelSpacing']))
    MRIpil_image = colormapping(MRIimg, gray).get()
    if MRI_CrossLink == 'true': MRIpil_image = drawMRILine(MRIpil_image,request,variable,source,target,source_variable)
    MRIpil_image = draw_line(MRIpil_image, x, y, plane, height)
    MRIpil_image = to_image(MRIpil_image)
    MRIimage_uri = to_data_uri(MRIpil_image)
    dicom_url = MRIimage_uri
    return dicom_url, z, ratio

def drawMRILine(img,request,variable,source,target,source_variable):
    if source!=target:
        ImagePosition_source = list(request.session.get('ImagePosition_'+source))[source_variable]
        ImagePosition_target = request.session.get('ImagePosition_'+target)[variable]
        ImageOrientation_source = request.session.get('ImageOrientation_'+source)[source_variable]
        ImageOrientation_target = request.session.get('ImageOrientation_'+target)[variable]
        MRI_pixelspacing_source = request.session.get('MRI_pixelspacing_'+source)
        MRI_pixelspacing_target = request.session.get('MRI_pixelspacing_'+target)
        source_shape = request.session.get('source_size'+source)
        target_shape = request.session.get('source_size'+target)
        startPointX,startPointY,endPointX,endPointY = customAPI(ImagePosition_source,ImageOrientation_source,ImagePosition_target,ImageOrientation_target,MRI_pixelspacing_source,MRI_pixelspacing_target,source_shape,target_shape)
        img = cv2.line(img, (round(startPointX), round(startPointY)), (round(endPointX), round(endPointY)), (255, 255, 0), 1,cv2.LINE_AA)
    return img




def image_show(request,No):
    variable = int(request.POST.get('variable',0))

    source_variable = int(request.POST.get('source_variable')) 
    CTWC = int(request.POST.get('CTWC'))
    CTWW = int(request.POST.get('CTWW'))
    PETWC = float(request.POST.get('PETWC'))
    PETWW = float(request.POST.get('PETWW'))
    MRIWC = float(request.POST.get('MRIWC',0))
    MRIWW = float(request.POST.get('MRIWW',0))
    source = request.POST.get('source',0)
    target = request.POST.get('target',0)

    plane = request.POST.get('plane')
    mode = request.POST.get('mode')
    drawActualCoordinates = request.POST.get('drawActualCoordinates')
    plane = plane.replace(" ", "")
    mode = mode.replace(" ", "")
    ActualCoordinates = request.POST.get('ActualCoordinates')
    x = int(request.POST.get('x'))
    y = int(request.POST.get('y'))
    height = float(request.POST.get('height'))
    width = float(request.POST.get('width'))
    Category = request.session.get('Category_' + No)

    WC={'CT':CTWC,'PET':PETWC,'RT':CTWC,'MRI':MRIWC}
    WW={'CT':CTWW,'PET':PETWW,'RT':CTWW,'MRI':MRIWW}

    if Category == 'PET':
        thickness = request.session.get('PET_slicethickness_' + No)
        Ori_H = request.session.get('CT_H_' + No)
        Ori_W = request.session.get('CT_W_' + No)
        Ori_D = request.session.get('CT_D_' + No)
        if ActualCoordinates == 'false':
            x, y = convert2draw(x, y, Ori_W, Ori_H, Ori_D, plane, width, height)
        PET_view = request.session.get('PET_view_' + No)
        CT_view_tag = {
            'ImagePositionPatient_F': request.session.get('CT_view_ImagePositionPatient_F_' + No),
            'ImagePositionPatient_S': request.session.get('CT_view_ImagePositionPatient_S_' + No),
            'D': request.session.get('view_D_' + No),
            'H': request.session.get('view_H_' + No),
            'W': request.session.get('view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
        }
        PET_tag = {
            'SliceThickness': request.session.get('PET_slicethickness_' + No),
        }
        dicom_url, z, ratio = processing_PET(PET_view, variable,WC,WW , plane, mode, x, y,
                                             height, drawActualCoordinates, CT_view_tag, PET_tag, Category)
    elif Category == 'CT':
        thickness = request.session.get('CT_view_slicethickness_' + No)
        Ori_H = request.session.get('CT_H_' + No)
        Ori_W = request.session.get('CT_W_' + No)
        Ori_D = request.session.get('CT_D_' + No)
        if ActualCoordinates == 'false':
            x, y = convert2draw(x, y, Ori_W, Ori_H, Ori_D, plane, width, height)
        CT = request.session.get('CT_view_' + No)
        CT_tag = {
            'ImagePositionPatient_F': request.session.get('CT_view_ImagePositionPatient_F_' + No),
            'ImagePositionPatient_S': request.session.get('CT_view_ImagePositionPatient_S_' + No),
            'D': request.session.get('view_D_' + No),
            'H': request.session.get('view_H_' + No),
            'W': request.session.get('view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
            'SliceThickness': request.session.get('CT_view_slicethickness_' + No),
        }
        contour_list=request.session.get('unet_contour_'+No)
        dicom_url, z, ratio = processing_CT(CT, variable, WC,WW, plane, x, y, height, drawActualCoordinates,
                                            CT_tag,contour_list, Category)
    elif Category == 'RT':
        thickness = request.session.get('CT_view_slicethickness_' + No)
        Ori_H = request.session.get('view_H_' + No)
        Ori_W = request.session.get('view_W_' + No)
        Ori_D = request.session.get('view_D_' + No)
        if ActualCoordinates == 'false':
            x, y = convert2draw(x, y, Ori_W, Ori_H, Ori_D, plane, width, height)
        CT_view = request.session.get('CT_view_' + No)
        CT_view_tag = {
            'ImagePositionPatient_F': request.session.get('CT_view_ImagePositionPatient_F_' + No),
            'ImagePositionPatient_S': request.session.get('CT_view_ImagePositionPatient_S_' + No),
            'D': request.session.get('view_D_' + No),
            'H': request.session.get('view_H_' + No),
            'W': request.session.get('view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
            'SliceThickness': request.session.get('CT_view_slicethickness_' + No),
        }
        dicom_url, z, ratio = processing_RT(CT_view, variable, WC, WW, plane, x, y, height, drawActualCoordinates,
                                            CT_view_tag, request.session.get('ROI_index_color_' + No),
                                            request.session.get('ROI_index_' + No), Category)
    elif Category == 'MRI':
        MRI_CrossLink = request.POST.get('MRI_CrossLink')
        thickness = request.session.get('MRI_slicethickness_' + No)
        Ori_H = request.session.get('MRI_H_' + No)
        Ori_W = request.session.get('MRI_W_' + No)
        Ori_D = request.session.get('MRI_D_' + No)
        if ActualCoordinates == 'false':
            x, y = convert2draw(x, y, Ori_W, Ori_H, Ori_D, plane, width, height)
        MRI = request.session.get('MRI_' + No)
        MRI_tag = {
            'D': request.session.get('view_D_' + No),
            'H': request.session.get('view_H_' + No),
            'W': request.session.get('view_W_' + No),
            'PixelSpacing': request.session.get('MRI_pixelspacing_' + No),
            'SliceThickness': request.session.get('MRI_slicethickness_' + No),
        }

        dicom_url, z, ratio = processing_MRI(MRI, variable, WC,WW, plane, x, y, height, drawActualCoordinates,
                                            MRI_tag, Category,request,source,target,source_variable,MRI_CrossLink)
    return dicom_url, z, ratio,variable, thickness

@csrf_exempt
def DICOM_show1(request):
    No = str(1)
    dicom_url, z, ratio,variable, thickness=image_show(request,No)
    return JsonResponse({"dicom_url": dicom_url, 'z': z, 'ratio': ratio, 'variable': variable,'thickness':thickness})


@csrf_exempt
def DICOM_show2(request):
    No = str(2)
    dicom_url, z, ratio,variable, thickness=image_show(request,No)
    return JsonResponse({"dicom_url": dicom_url, 'z': z, 'ratio': ratio, 'variable': variable,'thickness':thickness})


@csrf_exempt
def DICOM_show3(request):
    No = str(3)
    dicom_url, z, ratio,variable, thickness=image_show(request,No)
    return JsonResponse({"dicom_url": dicom_url, 'z': z, 'ratio': ratio, 'variable': variable,'thickness':thickness})


@csrf_exempt
def DICOM_show4(request):
    No = str(4)
    dicom_url, z, ratio,variable, thickness=image_show(request,No)
    return JsonResponse({"dicom_url": dicom_url, 'z': z, 'ratio': ratio, 'variable': variable,'thickness':thickness})


@csrf_exempt
def convertLocation(request):
    height = float(request.POST.get('height'))
    width = float(request.POST.get('width'))
    plane = request.POST.get('plane')
    x = int(request.POST.get('x'))
    y = int(request.POST.get('y'))
    z = int(request.POST.get('z'))
    WindowNo = str(request.POST.get('WindowNo'))
    imageType = str(request.POST.get('imageType'))
    source = request.POST.get('source',0)
    target = request.POST.get('target',0)

    Ori_H = request.session.get('view_H_' + WindowNo)
    Ori_W = request.session.get('view_W_' + WindowNo)
    Ori_D = request.session.get('view_D_' + WindowNo)
    x, y, z = convert(x, y, z, Ori_W, Ori_H, Ori_D, plane, width, height)
    # CT_mod座標
    request.session['Click_X'] = x
    request.session['Click_X'] = y
    request.session['Click_X'] = z
    return JsonResponse({'x': x, 'y': y, 'z': z})

@csrf_exempt
def getAnnotationFactorGroup(request):
    query ='''select factor from factorGroup order by id'''
    cursor = connections['AIC'].cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    factor=''
    for i, object in enumerate(res):
        factor += f'<option value={object[0]}>{object[0]}</option>'
    return JsonResponse({'factor':factor})

@csrf_exempt
def getAnnotationFactorDetail(request):
    factor_id = request.POST.get('factor_id')
    query ='''select distinct detail from annotationFactor where factor=%s order by detail'''
    cursor = connections['AIC'].cursor()
    cursor.execute(query,[factor_id])
    res = cursor.fetchall()
    detail=''
    for i, object in enumerate(res):
        detail += f'<option value="{object[0]}">'
    return JsonResponse({'detail':detail})

@csrf_exempt
def insertAnnotationFactor(request):
    a_id = request.POST.get('a_id')
    factor = request.POST.getlist('factor[]')
    detail = request.POST.getlist('detail[]')
    detail = np.delete(np.array(detail),np.where(np.array(factor)=='請選擇')[0]).tolist()
    factor = np.delete(np.array(factor),np.where(np.array(factor)=='請選擇')[0]).tolist()
    factor = np.delete(np.array(factor),np.where(np.array(detail)=='')[0]).tolist()
    detail = np.delete(np.array(detail),np.where(np.array(detail)=='')[0]).tolist()
    delete_query = '''delete from annotationFactor where a_id=%s'''
    cursor = connections['AIC'].cursor()
    cursor.execute(delete_query,[a_id])
    insert_query = '''insert into annotationFactor (a_id,factor,detail) values(%s,%s,%s)'''
    cursor = connections['AIC'].cursor()
    for perFactor, perDetail in zip(factor,detail):
        cursor.execute(insert_query,[a_id,perFactor,perDetail])
    return JsonResponse({})


def process_annotation_coordinate(request,multiplyOrDivide,Type,WindowNo,x,y,z):
    if multiplyOrDivide=='multiply':
        if Type == 'PET':
            PET_H = request.session.get('PET_H_' + WindowNo)
            PET_W = request.session.get('PET_W_' + WindowNo)
            PET_D = request.session.get('PET_D_' + WindowNo)
            CT_H = request.session.get('view_H_' + WindowNo)
            CT_W = request.session.get('view_W_' + WindowNo)
            CT_D = request.session.get('view_D_' + WindowNo)
            x = (x * (PET_W / CT_W))
            y = (y * (PET_H / CT_H))
            z = (z * (PET_D / CT_D))
        elif Type == 'RTPLAN':
            x = math.floor(x)
            y = math.floor(y)
            z = math.floor(z)
        elif Type == 'LDCT':
            x = math.floor(x)
            y = math.floor(y)
            z = math.floor(z)
    elif multiplyOrDivide=='divide':
        if Type == 'PET':
            PET_H = request.session.get('PET_H_' + WindowNo)
            PET_W = request.session.get('PET_W_' + WindowNo)
            PET_D = request.session.get('PET_D_' + WindowNo)
            CT_H = request.session.get('view_H_' + WindowNo)
            CT_W = request.session.get('view_W_' + WindowNo)
            CT_D = request.session.get('view_D_' + WindowNo)
            x = math.ceil((float(x) / (PET_W / CT_W)))
            y = math.ceil((float(y) / (PET_H / CT_H)))
            z = math.ceil((float(z) / (PET_D / CT_D)))
        elif Type == 'RTPLAN':
            x = math.ceil(float(x))
            y = math.ceil(float(y))
            z = math.ceil(float(z))
        elif Type == 'LDCT':
            x = math.ceil(float(x))
            y = math.ceil(float(y))
            z = math.ceil(float(z))
        elif Type == 'MRI':
            x = math.ceil(float(x))
            y = math.ceil(float(y))
            z = math.ceil(float(z))    
    return x,y,z
@csrf_exempt
def insertLocation(request):
    '''-----------------POST.get------------------'''
    x = float(request.POST.get('x'))
    y = float(request.POST.get('y'))
    z = float(request.POST.get('z'))
    StudyID = str(request.POST.get('StudyID'))
    SeriesID = request.POST.get('SeriesID')
    WindowNo = str(request.POST.get('WindowNo'))
    PID = 'null' if (str(request.POST.get('PID')) == '') else  request.POST.get('PID')
    SD = '' if (str(request.POST.get('SD')) == '') else str(request.POST.get('SD'))
    Item = '' if (str(request.POST.get('Item')) == '') else str(request.POST.get('Item'))
    date = '' if (str(request.POST.get('date')) == '') else str(request.POST.get('date'))
    username = 'null' if (str(request.POST.get('username')) == '') else str(request.POST.get('username'))
    SUV = '0' if (str(request.POST.get('SUV')) == '') else request.POST.get('SUV')
    Disease = '' if (str(request.POST.get('Disease')) == '') else str(request.POST.get('Disease'))
    LabelGroup = '' if (str(request.POST.get('LabelGroup')) == '') else str(request.POST.get('LabelGroup'))
    LabelName = '' if (str(request.POST.get('LabelName')) == '') else str(request.POST.get('LabelName'))
    LabelRecord = '' if (str(request.POST.get('LabelRecord')) == '') else str(request.POST.get('LabelRecord'))

    '''-----------------------------------'''

    Type = Item.replace(' ', '')
    now = datetime.now()
    current_time = str(now.strftime("%Y-%m-%d %H:%M:%S"))


    '''-----------Processing annotation coordinate------------'''
    x,y,z = process_annotation_coordinate(request,'multiply',Type,WindowNo,x,y,z)
    '''------------------------------------------------------'''
    cursor = connections['AIC'].cursor()
    query_insertAnnotation = '''
    insert into　annotation_new (chartNo,imageType,studyID,seriesID,studyDate,username,topicNo,updateTime,SUV,x,y,z,labelGroup,labelName,labelRecord) 
    output Inserted.id 
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''
    cursor.execute(query_insertAnnotation,[PID,Item,StudyID,SeriesID,SD,username,Disease,current_time,SUV,x,y,z,LabelGroup,LabelName,LabelRecord])
    inserted_id = cursor.fetchone()[0]
    id,PID,SD,Item,date,username,SUV,x,y,z,LabelGroup,LabelName,LabelRecord,StudyID,SeriesID,Dr_confirm,indices = selectAnnotation(request)
    return JsonResponse(
        {'inserted_id':inserted_id,'id': id, 'PID': PID, 'SD': SD, 'Item': Item, 'date': date, 'username': username, 'SUV': SUV, 'x': x, 'y': y,
         'z': z, 'LabelGroup': LabelGroup, 'LabelName': LabelName, 'LabelRecord': LabelRecord, 'StudyID':StudyID, 'SeriesID': SeriesID,'Dr_confirm':Dr_confirm,
         'indices': indices},
        status=200)

def removeContourFile(request,PID,studyDate,studyID,seriesID,id):
    filePath = searchFilePath(PID,studyDate,studyID,seriesID)
    if platform.system()!='Windows':
        dir = os.path.join('/home','user','netapp',filePath,'segmentation',id)
    else:
        dir= os.path.join('//172.31.6.6/share1/NFS/image_v2',filePath,'segmentation',id)

    if os.path.isdir(dir):
        for ind in range(4):
            ind = str(ind)
            unet_contourList = request.session.get('unet_contour_'+ind)
            try:
                if len(unet_contourList)!=1:
                    removeList = [i for i in unet_contourList if id in i]
                    list(filter(lambda x: unet_contourList.remove(x),removeList))
                    request.session['unet_contour_'+ind] =  unet_contourList
                else:
                    request.session['unet_contour_'+ind] = []
            except:
                pass
        shutil.rmtree(dir)

@csrf_exempt
def deleteLocation(request):
    '''---------------------Get POST and SESSION--------------------'''
    PID = 'null' if (str(request.POST.get('PID')) == '') else request.POST.get('PID')
    '''-------------------------------------------------------------'''
    all_annotations = request.session.get('all_annotations')
    id=str(request.POST.get('id'))
    querySearch='''SELECT chartNo,studyDate,studyID,seriesID FROM annotation_new WHERE id=%s'''
    cursor = connections['AIC'].cursor()
    cursor.execute(querySearch,[id])
    info = cursor.fetchall()
    PID=str(info[0][0])
    studyDate=str(info[0][1]).replace('-','')
    studyID=str(info[0][2])
    seriesID=str(info[0][3])
    removeContourFile(request,PID,studyDate,studyID,seriesID,id)
    query = '''delete from annotation_new where id=%s'''
    cursor = connections['AIC'].cursor()
    cursor.execute(query,[id])
    query = '''delete from measureTumor where annotationID=%s'''
    cursor = connections['AIC'].cursor()
    cursor.execute(query,[id])
    query = '''delete from annotationFactor where a_id=%s'''
    cursor = connections['AIC'].cursor()
    cursor.execute(query,[id])
    id,PID,SD,Item,date,username,SUV,x,y,z,LabelGroup,LabelName,LabelRecord,StudyID,SeriesID,Dr_confirm,indices = selectAnnotation(request)
    return JsonResponse(
        {'id': id, 'PID': PID, 'SD': SD, 'Item': Item, 'date': date, 'username': username, 'SUV': SUV, 'x': x, 'y': y,
         'z': z, 'LabelGroup': LabelGroup, 'LabelName': LabelName, 'LabelRecord': LabelRecord, 'StudyID':StudyID, 'SeriesID': SeriesID,'Dr_confirm':Dr_confirm,
         'indices': indices},
        status=200)


def selectAnnotation(request):
    is_superuser = request.session.get('is_superuser')
    all_annotations = request.session.get('all_annotations')
    SeriesIdIndex = request.session.get('SeriesIdIndex')
    Disease = '' if (str(request.POST.get('Disease')) == '') else str(request.POST.get('Disease'))
    PID = request.POST.get('PID')
    string = request.POST.getlist('str[]')
    studyDate = request.POST.getlist('Study_Date[]')
    username = str(request.POST.get('username'))
    cursor = connections['AIC'].cursor()
    
    if all_annotations==True:
        query = '''
        select * from (select　*,(CAST(studyID as VARCHAR(50)) + '_' + 
        CAST(seriesID as VARCHAR(50))) as 'studySeries' from annotation_new) as a 
        where  chartNo=%s  and topicNo=%s and studySeries in (%s,%s,%s,%s) 
        and studyDate in (%s,%s,%s,%s) order by CAST(SUV as float) DESC,studySeries,updateTime,labelName ASC
        '''
        cursor.execute(query,[PID, Disease, string[0], string[1], string[2], string[3],studyDate[0],studyDate[1],studyDate[2],studyDate[3]])
    else:
        query = '''
        select * from (select　*,(CAST(studyID as VARCHAR(50)) + '_' + 
        CAST(seriesID as VARCHAR(50))) as 'studySeries' from annotation_new) as a 
        where  chartNo=%s and (username=%s or username='') and topicNo=%s 
        and studySeries in (%s,%s,%s,%s) and studyDate in (%s,%s,%s,%s) 
        order by studySeries,updateTime,labelName ASC
        '''
        cursor.execute(query,[PID, username, Disease, string[0], string[1], string[2], string[3],studyDate[0],studyDate[1],studyDate[2],studyDate[3]])
    response = cursor.fetchall()
    id, PID, SD, Item, date, username, SUV, x, y, z, LabelGroup, LabelName, LabelRecord, StudyID,SeriesID,Dr_confirm = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],[]
    for info in response:
        Type = str(info[2]).replace(' ', '')
        StudySeries = str(info[3])+'_'+str(info[4])
        ind = str(list(SeriesIdIndex.keys())[list(SeriesIdIndex.values()).index(StudySeries)])
        
        rx,ry,rz = process_annotation_coordinate(request,'divide',Type,ind,info[10],info[11],info[12])
        id.append(info[0])
        PID.append(info[1])
        SD.append(info[5])
        Item.append(info[2])
        date.append(info[8])
        username.append(info[6])
        if float(info[9]) == 0:
            SUV.append('')
        else:
            SUV.append(round(float(info[9]), 3))
        x.append(rx)
        y.append(ry)
        z.append(rz)
        LabelGroup.append(info[13])
        LabelName.append(info[14])
        LabelRecord.append(info[15])
        StudyID.append(info[3])
        SeriesID.append(info[4])
        Dr_confirm.append(info[17])
    _, indices = np.unique(SeriesID, return_inverse=True)
    indices = list(indices.astype('float'))
    return id,PID,SD,Item,date,username,SUV,x,y,z,LabelGroup,LabelName,LabelRecord,StudyID,SeriesID,Dr_confirm,indices
@csrf_exempt
def selectLocation(request):
    id,PID,SD,Item,date,username,SUV,x,y,z,LabelGroup,LabelName,LabelRecord,StudyID,SeriesID,Dr_confirm,indices = selectAnnotation(request)
    return JsonResponse(
        {'id': id, 'PID': PID, 'SD': SD, 'Item': Item, 'date': date, 'username': username, 'SUV': SUV, 'x': x, 'y': y,
         'z': z, 'LabelGroup': LabelGroup, 'LabelName': LabelName, 'LabelRecord': LabelRecord, 'StudyID':StudyID, 'SeriesID': SeriesID,'Dr_confirm':Dr_confirm,
         'indices': indices},
        status=200)


@csrf_exempt
def findLocalMax(request):
    x = float(request.POST.get('x'))
    y = float(request.POST.get('y'))
    z = float(request.POST.get('z'))
    WC = float(request.POST.get('PETWC'))
    SeriesID = str(request.POST.get('SeriesID'))
    SeriesIdIndex = request.session.get('SeriesIdIndex')
    ind = list(SeriesIdIndex.keys())[list(SeriesIdIndex.values()).index(SeriesID)]
    Category = request.session.get('Category_' + ind)
    vol = request.session.get(str(Category)+'_' + str(ind))
    D = request.session.get('view_D_' + str(ind))
    H = request.session.get('view_H_' + str(ind))
    W = request.session.get('view_W_' + str(ind))
    PixelSpacing = request.session.get(str(Category)+'_pixelspacing_' + str(ind))
    SliceThickness = request.session.get(str(Category)+'_slicethickness_' + str(ind))
    Category = request.session.get('Category_' + ind)
    x, y, z, maxValue = localmax(D, H, W, vol, x, y, z, PixelSpacing, SliceThickness, WC,Category)

    return JsonResponse({'x': x, 'y': y, 'z': z, 'maxValue': maxValue})


@csrf_exempt
def findSUV(request):
    x = float(request.POST.get('x'))
    y = float(request.POST.get('y'))
    z = float(request.POST.get('z'))
    isNotPET = request.POST.get('isNotPET')
    SeriesID = request.POST.get('SeriesID')
    SeriesIdIndex = request.session.get('SeriesIdIndex')
    ind = str(list(SeriesIdIndex.keys())[list(SeriesIdIndex.values()).index(str(SeriesID))])

    if not (isNotPET):
        PET_H = request.session.get('PET_H_' + ind)
        PET_W = request.session.get('PET_W_' + ind)
        PET_D = request.session.get('PET_D_' + ind)
        CT_H = request.session.get('view_H_' + ind)
        CT_W = request.session.get('view_W_' + ind)
        CT_D = request.session.get('view_D_' + ind)
        PET_X = round(x * (PET_W / CT_W))
        PET_Y = round(y * (PET_H / CT_H))
        PET_Z = round(z * (PET_D / CT_D))
        PET = request.session.get('PET_' + ind)
        SUV = np.array(h5py.File(PET, "r")['vol'])[PET_Z, PET_Y, PET_X]
        SUV = np.float64(SUV)
    else:
        SUV = ''
    return JsonResponse({'SUV': SUV})



from django.db import connections



@csrf_exempt
def TextReport(request):
    MedExecTime= request.session.get('MedExecTime', 0)
    pid = request.POST.get('PID')
    image_type = request.POST.get('image_type')

    query = '''
    declare @chartNo int
    set @chartNo= %s
    select * ,ROW_NUMBER()　over(order by eventDate DESC,reportText)　as ind from(
        select distinct result.typeName ,result.eventDate, (
            select '--------------------------- \n '+
                'DescriptionType:'+cast(c.descriptionType AS VARCHAR(max) )+
                ' \n ---------------------------  \n '+cast(c.reportText AS VARCHAR(max) ) + ' \n  \n  \n '
            from allEvents as a
            inner join medTypeSet as b on a.medType=b.medType
            left join eventDetails as c on a.eventID=c.eventID
            where a.chartNo=@chartNo 
            and eventID_F is null and (a.eventChecked <>0 or a.eventChecked is null) 
            and a.orderNo = result.orderNo 
            FOR XML PATH('')
            ) as reportText
                
        from(
            select a.chartNo,a.orderNo,a.eventDate,a.medType,b.typeName,a.eventID,a.eventChecked,a.note,c.descriptionType,c.reportText
            from allEvents as a
            inner join medTypeSet as b on a.medType=b.medType
            left join eventDetails as c on a.eventID=c.eventID
            where a.chartNo=@chartNo 
            and eventID_F is null and (a.eventChecked <>0 or a.eventChecked is null)
        ) as result where result.medType<30000 
    ) as final
    '''
    # select c.typeName,a.eventDate,b.reportText,ROW_NUMBER()　over(order by a.eventDate DESC,reportText)　as ind 
	# from allEvents as a
	# left join eventDetails as b on a.eventID=b.eventID
	# left join medTypeSet as c on a.medType=c.medType
	# where (b.descriptionType>2 or b.descriptionType is null)and a.chartNo=%s
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[pid])
    sn = []
    examItem = []
    examDate = []
    examReport = []
    exam = cursor.fetchall()

    for i in range(len(exam)):
        examItem.append(exam[i][0].replace(' ', ''))
        examDate.append(str(exam[i][1]).split(' ')[0])
        examReport.append(exam[i][2])
        sn.append(exam[i][3])
    

    query_find_index = """
    declare @chartNo int, @eventDate datetime
    set @chartNo= %s
    set @eventDate=%s  + ' 23:59:59 '
    select top 1 ind from (
        select * ,ROW_NUMBER()　over(order by eventDate DESC,reportText)　as ind from(
            select distinct result.typeName ,result.eventDate,result.medType ,(
                select '--------------------------- &#13;'+
                'DescriptionType:'+cast(c.descriptionType AS VARCHAR(max) )+
                '&#13--------------------------- &#13;'+cast(c.reportText AS VARCHAR(max) ) + '&#13;&#13;&#13; '
                from allEvents as a
                inner join medTypeSet as b on a.medType=b.medType
                left join eventDetails as c on a.eventID=c.eventID
                where a.chartNo=@chartNo 
                and eventID_F is null and (a.eventChecked <>0 or a.eventChecked is null) 
                and a.orderNo = result.orderNo 
                FOR XML PATH('')
                ) as reportText
                    
            from(
                select a.chartNo,a.orderNo,a.eventDate,a.medType,b.typeName,a.eventID,a.eventChecked,a.note,c.descriptionType,c.reportText
                from allEvents as a
                inner join medTypeSet as b on a.medType=b.medType
                left join eventDetails as c on a.eventID=c.eventID
                where a.chartNo=@chartNo 
                and eventID_F is null and (a.eventChecked <>0 or a.eventChecked is null)
            ) as result where result.medType<30000 
        ) as final
    ) as a where a.eventDate<=@eventDate
    """


    if image_type=='PET':
        medType='(3570,3579)'
        query_find_index += f''' and a.medType in {medType} '''
    elif image_type=='CT':
        medType='(3030,3031,3032,3036,3037,3038,3039)'
        query_find_index += f''' and a.medType in {medType} '''
    elif image_type=='MRI':
        medType='(3040,3041,3042,3047,3048,3049)'
        query_find_index += f''' and a.medType in {medType} '''


    # if image_type=='PET' or image_type=='CT' or image_type=='MRI':
    #     if image_type=='PET':
    #         medType='(3570,3579)'
    #     elif image_type=='CT':
    #         medType='(3030,3031,3032,3036,3037,3038,3039)'
    #     elif image_type=='MRI':
    #         medType='(3040,3041,3042,3047,3048,3049)'
    #     query_find_index = f"""
    #         select top 1 ind from(
    #         select c.medType,a.eventDate,b.reportText,ROW_NUMBER()　over(order by a.eventDate DESC,reportText)　as ind 
    #         from allEvents as a
    #         left join eventDetails as b on a.eventID=b.eventID
    #         left join medTypeSet as c on a.medType=c.medType
    #         where (b.descriptionType>2 or b.descriptionType is null)and a.chartNo=%s
    #         ) as a where a.eventDate<=%s　and a.medType in {medType}"""
    # else :
    #     query_find_index = """
    #         select top 1 ind from(
    #         select c.medType,a.eventDate,b.reportText,ROW_NUMBER()　over(order by a.eventDate DESC,reportText)　as ind 
    #         from allEvents as a
    #         left join eventDetails as b on a.eventID=b.eventID
    #         left join medTypeSet as c on a.medType=c.medType
    #         where (b.descriptionType>2 or b.descriptionType is null)and a.chartNo=%s
    #         ) as a where a.eventDate<=%s"""
    cursor.execute(query_find_index,[pid,MedExecTime])
    idx = cursor.fetchall()[0][0]

    return JsonResponse({'examItem': examItem, 'examDate': examDate, 'examReport': examReport,'sn':sn ,'idx': idx})


import pandas as pd


def string2date(str):
    str = pd.to_datetime(str,errors = 'coerce')
    str = np.array(str, dtype=np.datetime64)
    str = np.float64(str)
    return str


@csrf_exempt
def cancer(request):
    query = '''
            select DiseaseNo ,Disease
            from Disease 
            '''
    cursor = connections['AIC'].cursor()
    cursor.execute(query)
    DiseaseNo = []
    Disease = []
    res = cursor.fetchall()
    for i in range(len(res)):
        DiseaseNo.append(res[i][0])
        Disease.append(res[i][1])
    return JsonResponse({'DiseaseNo': DiseaseNo, 'Disease': Disease})

@csrf_exempt
def LabelGroup(request):
    subjectID = request.POST.get('SubjectID')
    query = '''
            select SeqNo as 'GroupID',LabelGroup
            from SubjectLabelGroup 
            where SubjectID=%s group by SeqNo,LabelGroup
            '''
    cursor = connections['AIC'].cursor()
    cursor.execute(query,[subjectID])
    GroupID = []
    LabelGroup = []
    res = cursor.fetchall()
    for i in range(len(res)):
        GroupID.append(res[i][0])
        LabelGroup.append(res[i][1])
    return JsonResponse({'GroupID': GroupID, 'LabelGroup': LabelGroup})

@csrf_exempt
def LabelName(request):

    query = '''
            select　b.LabelName
            from SubjectLabelGroup as a left outer join SubjectLabelContent as b on a.LabelGroupID=b.LabelGroupID
		　　where  SubjectID=''' + str(request.POST.get('SubjectID')) + ''' and a.SeqNo=''' + str(
        request.POST.get('LabelGroup'))
    cursor = connections['AIC'].cursor()
    cursor.execute(query)
    LabelName = []
    res = cursor.fetchall()
    for i in range(len(res)):
        LabelName.append(res[i][0])
    return JsonResponse({'LabelName': LabelName})


@csrf_exempt
def PatientImageInfo(request):
   

    PID = request.POST.get('PID')
    ImageSelect_cat = request.POST.get('ImageSelect_cat')
    ImageSelect_date = request.POST.get('ImageSelect_date')
    cursor = connections['practiceDB'].cursor()

    if ImageSelect_date=='-1' and ImageSelect_cat=='-1':
        query = ''' 
        select a.chartNo,a.studyID,a.category,a.studyDate,
        b.seriesID,b.sliceNo,b.seriesDes,b.note as viewplane from examStudy as a
        inner join examSeries as b on a.storageID=b.storageID
        where chartNo=%s
        '''
        cursor.execute(query, [PID])
    elif ImageSelect_date!='-1' and ImageSelect_cat=='-1':
        query = ''' 
        select a.chartNo,a.studyID,a.category,a.studyDate,
        b.seriesID,b.sliceNo,b.seriesDes,b.note as viewplane from examStudy as a
        inner join examSeries as b on a.storageID=b.storageID
        where chartNo=%s and studyDate=%s
        '''    
        cursor.execute(query, [PID,ImageSelect_date])
    elif ImageSelect_date=='-1' and ImageSelect_cat!='-1':
        query = ''' 
        select a.chartNo,a.studyID,a.category,a.studyDate,
        b.seriesID,b.sliceNo,b.seriesDes,b.note as viewplane from examStudy as a
        inner join examSeries as b on a.storageID=b.storageID
        where chartNo=%s and category=%s
        '''
        cursor.execute(query, [PID,ImageSelect_cat])
    elif ImageSelect_date!='-1' and ImageSelect_cat!='-1':
        query = ''' 
        select a.chartNo,a.studyID,a.category,a.studyDate,
        b.seriesID,b.sliceNo,b.seriesDes,b.note as viewplane from examStudy as a
        inner join examSeries as b on a.storageID=b.storageID
        where chartNo=%s and category=%s and studyDate=%s
        '''
        cursor.execute(query, [PID,ImageSelect_cat,ImageSelect_date])
    # select *,SUBSTRING(viewplane,1,1) as v1,SUBSTRING(viewplane,2,1) as v2 from (
    # select b.chartNo,a.studyID,a.category,a.eventDate,a.seriesID,a.sliceNo,a.seriesDes
    # ,CONVERT(varchar, a.seriesID) as viewplane from ExamStudySeries_6
    # as a inner join allEvents as b on a.eventID=b.eventID where  b.chartNo=%s ) 
    # as a　order by a.eventDate ASC,v2 ASC,v1 ASC

    
    
    res = cursor.fetchall()
    ChartNo = []
    StudyID = []
    StudyDes = []
    ExecDate = []
    SeriesID = []
    SliceNo = []
    note = []
    SeriesDes=[]
    viewplane = []
    for i in range(len(res)):
        
        PID,MedExecTime,StudyIDText,SeriesIDText = res[i][0],res[i][3],res[i][1],res[i][4]
        
        filePath = searchFilePath(PID,MedExecTime,StudyIDText,SeriesIDText)
        if platform.system()!='Windows':
            fileDir = os.path.join('/home','user','netapp',filePath)
        else:
            fileDir= os.path.join('//172.31.6.6/share1/NFS/image_v2',filePath)

        fileDir = fileDir.replace('-', '')
        fileDir = fileDir.replace(' ', '')

        fileExt = "*.h5"

        if len(list(pathlib.Path(fileDir).glob(fileExt))) != 0:
            ChartNo.append(str(res[i][0]))
            StudyID.append(res[i][1])
            StudyDes.append(res[i][2])
            ExecDate.append(res[i][3])
            SeriesID.append(res[i][4])
            SliceNo.append(res[i][5])
            note.append(res[i][6])
            SeriesDes.append(res[i][6])
            viewplane.append(res[i][7])
    
    date = pd.unique(ExecDate).tolist()
    category = pd.unique(StudyDes).tolist()
    return JsonResponse({'ChartNo': ChartNo,
                         'StudyID': StudyID,
                         'StudyDes': StudyDes,
                         'ExecDate': ExecDate,
                         'SeriesID': SeriesID,
                         'SliceNo': SliceNo,
                         'note':note,
                         'SeriesDes':SeriesDes,
                         'viewplane':viewplane,
                         'date':date,
                         'category':category
                         })


@csrf_exempt
def RT_change(request):
    WindowNo = str(request.POST.get('WindowNo'))
    index = request.session.get('ROI_index_' + WindowNo)
    ROIname = request.session.get('ROIname_' + WindowNo)
    Color = request.session.get('Color_' + WindowNo)
    color = []
    for i in range(len(ROIname)):
        color.append(tuple(np.array(Color[i], dtype='float')))

    return JsonResponse({'ROIname': ROIname, 'color': color, 'index': index}, status=200)


@csrf_exempt
def ROIname(request):
    WindowNo = str(request.POST.get('WindowNo'))
    ROIname = request.session.get('ROIname_' + WindowNo)
    Color = request.session.get('Color_' + WindowNo)
    color = []
    for i in range(len(ROIname)):
        color.append(tuple(np.array(Color[i], dtype='float')))
    return JsonResponse({'ROIname': ROIname, 'color': color}, status=200)


@csrf_exempt
def DrawContour(request):
    WindowNo = str(request.POST.get('WindowNo'))
    ROIname_checked = request.POST.getlist('ROIname[]')
    ROIname = request.session.get('ROIname_' + WindowNo)
    Color = request.session.get('Color_' + WindowNo)
    index = [ROIname.index(_) for _ in ROIname_checked]  # 取得要繪製的輪廓代號
    request.session['ROI_index_color_' + WindowNo] = list(
        map(lambda i: list(np.array(Color[i], dtype='float')), index))
    request.session['ROI_index_' + WindowNo] = index

    return JsonResponse({}, status=200)


def rt_contour(ct_img, ROI_checked, Color, Path, variable,plane):
    for i in range(len(ROI_checked)):
        rt_img = np.int32((h5py.File(Path, "r")['rtss_vol'][variable, :, :] >> ROI_checked[i]) % 2)
        imgTemp = rt_img.astype("uint8")
        ret, binary = cv2.threshold(imgTemp, 0, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            cv2.drawContours(ct_img, [contour], -1, Color[i], thickness=1)
    return ct_img

@csrf_exempt
def UNet(request):

    WindowNo = str(request.POST.get('WindowNo'))
    id = str(request.POST.get('id'))
    plane = str(request.POST.get('plane'))
    x = int(request.POST.get('x'))
    y = int(request.POST.get('y'))
    z = int(request.POST.get('z'))
    PixelSpacing = request.session.get('CT_view_pixelspacing_' + WindowNo)
    delta_Z = request.session.get('CT_view_delta_Z_' + WindowNo)
    sliceThickness = request.session.get('CT_view_slicethickness_' + WindowNo)
    
    img_path = request.session.get('CT_view_' + WindowNo)
    for plane in ['Axial','Coronal','Sagittal']:
        unet_contour_path = os.path.join(pathlib.Path(img_path[0]).parents[0],'segmentation',id,plane+"_unet.h5")
        contour_list=request.session.get('unet_contour_'+WindowNo)

        if unet_contour_path not in contour_list : 
            contour_list.append(unet_contour_path)
            request.session['unet_contour_'+WindowNo]=contour_list

    if not os.path.isfile(unet_contour_path):
        model_UNet_path = os.path.join(PATH,'model','UNet.h5')
        model_UNet = tf.keras.models.load_model(model_UNet_path, compile=False)
        saveFiledir = pathlib.Path(unet_contour_path).parents[0]
        pathlib.Path(saveFiledir).mkdir(parents=True, exist_ok=True)
        
        
        pad_size = 160
        size = 20
        vol = np.array(h5py.File(img_path[0], "r")['vol'][(z-size):(z+size), (y-size):(y+size), (x-size):(x+size)])
        pad_x = np.repeat(np.array((pad_size - vol.shape[1]) / 2), 2).astype('int')
        pad_y = np.repeat(np.array((pad_size - vol.shape[2]) / 2), 2).astype('int')
        vol_ori = np.pad(vol, pad_width=((0, 0),pad_x, pad_y), mode='constant', constant_values=-2000)
        vol = Window(vol_ori.copy(), -550, 1600)
        mask = model_UNet.predict(vol)
        predict = mask.argmax(axis=3)

        unet_tumor_path = os.path.join(saveFiledir,"Tumor_unet.h5")
        hf_tumor = h5py.File(unet_tumor_path, 'w') 
        hf_tumor.create_dataset('Tumor', data=predict)
        hf_tumor.create_dataset('vol', data=vol_ori)
        #--------算體積--use cc3d------    


        for plane in ['Axial','Coronal','Sagittal']:

            unet_contour_path = os.path.join(saveFiledir,plane+"_unet.h5")
            contour_list=request.session.get('unet_contour_'+WindowNo)
            if unet_contour_path not in contour_list : 
                contour_list.append(unet_contour_path)
                request.session['unet_contour_'+WindowNo]=contour_list
            hf = h5py.File(unet_contour_path, 'w') 

            if plane == 'Axial':
                num=predict.shape[0]
            elif plane == 'Coronal':
                num=predict.shape[1]
            elif plane == 'Sagittal':
                num=predict.shape[2]
            for j in range(num):
                contour={}
                if plane == 'Axial':
                    imgTemp = predict[j].copy()
                elif plane == 'Coronal':
                    imgTemp = predict[:,j,:].copy()
                elif plane == 'Sagittal':
                    imgTemp = predict[:,:,j].copy()
                
                if imgTemp.max() != 0:
                    imgTemp = imgTemp.astype("uint8")
                    img = imgTemp.copy()
                    kernel = np.ones((3, 3), np.uint8)
                    dilation = cv2.dilate(img, kernel, iterations=1)
                    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                    for i in range(len(contours)): 
                        contour.update({i:(contours[i]-((pad_size/2)-(size))+[x-(size),y-(size)]).tolist()})
                        if plane == 'Axial':
                            contour.update({i:(contours[i]-((pad_size/2)-(size))+[x-(size),y-(size)]).tolist()})
                        elif plane == 'Coronal':

                            contour.update({i:(contours[i]-[((pad_size/2)-(size)),0]+[x-(size),z-(size)]).tolist()})
                        elif plane == 'Sagittal':
                            contour.update({i:(contours[i]-[((pad_size/2)-(size)),0]+[y-(size),z-(size)]).tolist()})
                    if plane == 'Axial':
                        hf.create_dataset(str((z-size)+j), data=json.dumps(contour))
                    elif plane == 'Coronal':
                        
                        hf.create_dataset(str((y-int(pad_size/2))+j), data=json.dumps(contour))
                    elif plane == 'Sagittal':
                        hf.create_dataset(str((x-int(pad_size/2))+j), data=json.dumps(contour))
        
        
        '''
        算腫瘤特徵
        '''
        ROISize =  str(size)+'x'+str(pad_size)+'x'+str(pad_size)
        
        maxDia_point1,maxDia_point2,maxDia,secDia_point1,secDia_point2,secDia,vector_angle,max_area,volume = measure_Tumor(predict,PixelSpacing,sliceThickness,delta_Z)
        AvgDia = (maxDia+secDia)/2
        
        query = ''' 
        INSERT INTO 
            measureTumor 
            VALUES 
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        cursor = connections['AIC'].cursor()
        cursor.execute(query, 
            [
                id,
                x,
                y,
                z,
                ROISize,
                float(maxDia),
                int(maxDia_point1[1]),
                int(maxDia_point1[0]),
                int(maxDia_point2[1]),
                int(maxDia_point2[0]),
                float(secDia),
                int(secDia_point1[1]),
                int(secDia_point1[0]),
                int(secDia_point2[1]),
                int(secDia_point2[0]),
                float(AvgDia),
                float(vector_angle),
                float(max_area),
                volume
            ]
        )
        device = cuda.get_current_device()
        device.reset()
    return JsonResponse({}, status=200)
    
@csrf_exempt
def window_load(request):
    WindowNo = str(request.POST.get('WindowNo'))
    request.session['unet_contour_'+WindowNo]=[]
    return JsonResponse({}, status=200)   

@csrf_exempt
def SaveCoordinate(request):
    PID = str(request.POST.get('PID'))
    StudyID = int(request.POST.get('StudyID'))
    SeriesID = int(request.POST.get('SeriesID'))
    variable = str(request.POST.get('variable'))
    username = str(request.POST.get('username'))
    date = str(request.POST.get('date'))
    Disease = str(request.POST.get('Disease'))
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    LabelRecord = str(request.POST.get('LabelRecord'))

    if str(SeriesID)[0]=='1':
        view =  '(A)'
    elif str(SeriesID)[0]=='2':
        view =  '(C)'
    elif str(SeriesID)[0]=='3':
        view =  '(S)'
    query = '''          
        INSERT INTO annotation_new (chartNo,imageType,studyID,seriesID,studyDate,username,topicNo,updateTime,SUV,x,y,z,labelGroup,labelName,labelRecord) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
    cursor = connections['AIC'].cursor()
    cursor.execute(query, [PID,'MRI',StudyID,SeriesID,date,username,Disease,str(current_time),'0','0','0',variable,'MRI','slice coordinate',f'note: {LabelRecord}'])
    return JsonResponse({}, status=200)   

@csrf_exempt
def getusers(request):
    username = str(request.POST.get('username'))
    '''get all users'''
    query = '''select username from auth_user order by is_superuser　DESC'''
    cursor = connections['default'].cursor()
    cursor.execute(query)
    users = []
    res = cursor.fetchall()
    for rows in res:
        users.append(rows[0])

    '''is current user superuser?'''
    query = '''select is_superuser from auth_user where username=%s'''
    cursor = connections['default'].cursor()
    cursor.execute(query,[username])
    is_superuser = cursor.fetchall()[0][0]
    request.session['is_superuser']=is_superuser
    return JsonResponse({'users':users,'is_superuser':is_superuser}, status=200) 

@csrf_exempt
def getAnnotationFactor(request):
    a_id = request.POST.get('a_id')
    cursor = connections['AIC'].cursor()
    query='''select f_id, factor, detail from annotationFactor where a_id=%s'''
    cursor.execute(query,[a_id])
    
    res = cursor.fetchall()
    f_id,factor,detail,dr_confirm = [],[],[],[]
    for row in res :
        f_id.append(row[0])
        factor.append(row[1])
        detail.append(row[2])

    query='''select doctor_confirm from annotation where id=%s'''
    cursor.execute(query,[a_id])
    dr_confirm = cursor.fetchall()[0][0]
    return JsonResponse({'f_id':f_id,'factor':factor,'detail':detail,'dr_confirm':dr_confirm}, status=200) 

@csrf_exempt
def updateDrConfirm(request):
    id = request.POST.get('id')
    doctor_confirm = request.POST.get('doctor_confirm')
    query='''update annotation set doctor_confirm=%s where id=%s'''
    cursor = connections['AIC'].cursor()
    cursor.execute(query,[doctor_confirm,id])
    return JsonResponse({}, status=200) 