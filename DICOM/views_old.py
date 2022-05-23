import json

from django.shortcuts import render, redirect

# Create your views here.
import sys
import os
import cmapy
PATH = os.getcwd()
parent_Path=os.path.abspath(os.path.join(PATH,'..'))
sys.path.append(os.path.join(parent_Path,"AIC","函式庫"))

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

matplotlib.use('agg')
import pydicom
import math
from numba import jit
import numpy as np
from cryptography.fernet import Fernet

from base64 import b64encode
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import tensorflow as tf


model_UNet_path = os.path.join(PATH,'model','UNet.h5')
model_UNet = tf.keras.models.load_model(model_UNet_path, compile=False)

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
        img = line(img, (0, y), (x - space1, y), (255, 0, 0), 1)
        img = line(img, (x + space1, y), (x + size, y), (255, 0, 0), 1)
        img = line(img, (x, 0), (x, y - space2), (255, 0, 0), 1)
        img = line(img, (x, y + space2), (x, y + size), (255, 0, 0), 1)
        #img = circle(img, (x, y), 1, (255, 0, 0), -1)
        return img.get().astype(np.uint8)
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
def DICOM(request):
    StudyIdIndex = {'1': 0, '2': 0, '3': 0, '4': 0}

    request.session['unet_contour_1']=[]
    request.session['unet_contour_2']=[]
    request.session['unet_contour_3']=[]
    request.session['unet_contour_4']=[]
    key = Fernet.generate_key()
    request.session['key'] = key.decode()
    fernet = Fernet(key)
    try:
        PID = fernet.encrypt(request.session.get('PID', 0).encode()).decode()
    except:
        return redirect('/')
    MedExecTime = request.session.get('MedExecTime', 0)
    Item = request.session.get('Item', 0).replace(' ','')
    StudyID = request.session.get('StudyID', 0)
    Disease = request.session.get('Disease', 0)
    request.session['StudyIdIndex'] = StudyIdIndex
    au = request.session.get('au')

    return render(request, 'DICOM/DICOM.html',
                  {'PID': PID, 'MedExecTime': MedExecTime, 'Item': Item, 'StudyID': StudyID,'Disease':Disease,'au':au})




def to_data_uri(pil_img):
    data = BytesIO()
    pil_img.save(data, "png")  # pick your format
    data64 = b64encode(data.getvalue())
    return u'data:img/png;base64,' + data64.decode('UTF-8')


def convert(x, y, z, Ori_W, Ori_H, Ori_D, plane, width, height, Position_F, Position_S):
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


def convert2draw(x, y, Ori_W, Ori_H, Ori_D, plane, width, height):
    if plane != "Axial":
        x = round(x * (Ori_W / width))
        y = round(y * (Ori_D / height))
    else:
        x = round(x * (Ori_W / width))
        y = round(y * (Ori_H / height))
    return x, y

import codecs, json


@csrf_exempt
def load_DICOM(request):
    key = request.session['key'].encode()
    fernet = Fernet(key)
    root= request.POST.get('root')
    PID = fernet.decrypt(request.POST.get('PID').encode()).decode()
    MedExecTime = request.POST.get('MedExecTime')
    StudyIDText = request.POST.get('StudyIDText')
    


    dir=root+PID+'\\'+MedExecTime+'\\'+StudyIDText
    fileDir = dir.replace('-', '')
    fileDir = fileDir.replace(' ', '')
    WindowNo = str(1) if (str(request.POST.get('WindowNo')) == 'None') else str(request.POST.get('WindowNo'))
    request.session['Category_' + WindowNo] = 'PET'
    StudyIdIndex = request.session.get('StudyIdIndex')
    StudyIdIndex.update({str(WindowNo): fileDir.split('\\')[-1]})
    request.session['StudyIdIndex'] = StudyIdIndex
    fileExt = r"**\*CTvol.h5"
    tempPath = list(pathlib.Path(fileDir).glob(fileExt))
    paths = sorted([os.path.join(filename) for filename in tempPath])[0]
    request.session['CT_' + WindowNo] = paths
    with h5py.File(paths, "r") as f:
        a_group_key = list(f.keys())
        headers = f[a_group_key[0]]
        request.session['CT_pixelspacing_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[0]).PixelSpacing[0])
        request.session['CT_slicethickness_' + WindowNo] = abs(float(pydicom.dataset.Dataset.from_json(headers[0]).ImagePositionPatient[2])-float(pydicom.dataset.Dataset.from_json(headers[1]).ImagePositionPatient[2]))
        request.session['CT_D_' + WindowNo] = f[a_group_key[1]].shape[0]
        request.session['CT_H_' + WindowNo] = f[a_group_key[1]].shape[1]
        request.session['CT_W_' + WindowNo] = f[a_group_key[1]].shape[2]
    fileExt = r"**\*CTvolmod.h5"
    tempPath = list(pathlib.Path(fileDir).glob(fileExt))
    paths = sorted([os.path.join(filename) for filename in tempPath])[0]
    request.session['CT_view_' + WindowNo] = paths
    with h5py.File(paths, "r") as f:
        a_group_key = list(f.keys())
        headers = f[a_group_key[0]]
        request.session['CT_view_pixelspacing_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[0]).PixelSpacing[0])
        request.session['CT_view_ImagePositionPatient_F_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[0]).ImagePositionPatient[2])
        request.session['CT_view_ImagePositionPatient_S_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[1]).ImagePositionPatient[2])
        request.session['CT_view_D_' + WindowNo] = f[a_group_key[1]].shape[0]
        request.session['CT_view_H_' + WindowNo] = f[a_group_key[1]].shape[1]
        request.session['CT_view_W_' + WindowNo] = f[a_group_key[1]].shape[2]
        request.session['shiftspacing_' + WindowNo] = f[a_group_key[1]].attrs['shiftspacing']
    fileExt = r"**\*PETvol.h5"
    tempPath = list(pathlib.Path(fileDir).glob(fileExt))
    paths = sorted([os.path.join(filename) for filename in tempPath])[0]
    request.session['PET_' + WindowNo] = paths
    with h5py.File(paths, "r") as f:
        a_group_key = list(f.keys())
        headers = f[a_group_key[0]]
        request.session['PET_pixelspacing_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[0]).PixelSpacing[0])
        request.session['PET_slicethickness_' + WindowNo] = abs(float(pydicom.dataset.Dataset.from_json(headers[0]).ImagePositionPatient[2])-float(pydicom.dataset.Dataset.from_json(headers[1]).ImagePositionPatient[2]))
        request.session['PET_D_' + WindowNo] = f[a_group_key[1]].shape[0]
        request.session['PET_H_' + WindowNo] = f[a_group_key[1]].shape[1]
        request.session['PET_W_' + WindowNo] = f[a_group_key[1]].shape[2]
    fileExt = r"**\*PETvolmod.h5"
    tempPath = list(pathlib.Path(fileDir).glob(fileExt))
    paths = sorted([os.path.join(filename) for filename in tempPath])[0]
    request.session['PET_view_' + WindowNo] = paths
    return JsonResponse({}, status=200)


@csrf_exempt
def load_RT_DICOM(request):
    key = request.session['key'].encode()
    fernet = Fernet(key)

    root= request.POST.get('root')
    PID = fernet.decrypt(request.POST.get('PID').encode()).decode()
    MedExecTime = request.POST.get('MedExecTime')
    StudyIDText = request.POST.get('StudyIDText')


    dir=root+PID+'\\'+MedExecTime+'\\'+StudyIDText
    fileDir = dir.replace('-', '')
    fileDir = fileDir.replace(' ', '')
    WindowNo = str(1) if (str(request.POST.get('WindowNo')) == 'None') else str(request.POST.get('WindowNo'))
    request.session['Category_' + WindowNo] = 'RT'
    StudyIdIndex = request.session.get('StudyIdIndex')
    StudyIdIndex.update({str(WindowNo): fileDir.split('\\')[-1]})
    request.session['StudyIdIndex'] = StudyIdIndex
    fileExt = r"**\*RTCT.h5"
    tempPath = list(pathlib.Path(fileDir).glob(fileExt))
    paths = sorted([os.path.join(filename) for filename in tempPath])[0]
    request.session['CT_view_' + WindowNo] = paths
    with h5py.File(paths, "r") as f:
        a_group_key = list(f.keys())

        headers = f['header']

        request.session['CT_view_pixelspacing_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[0]).PixelSpacing[0])
        request.session['CT_view_slicethickness_' + WindowNo] = abs(float(pydicom.dataset.Dataset.from_json(headers[0]).ImagePositionPatient[2])-float(pydicom.dataset.Dataset.from_json(headers[1]).ImagePositionPatient[2]))
        request.session['CT_view_ImagePositionPatient_F_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[0]).ImagePositionPatient[2])
        request.session['CT_view_ImagePositionPatient_S_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[1]).ImagePositionPatient[2])
        request.session['CT_view_D_' + WindowNo] = f['vol'].shape[0]
        request.session['CT_view_H_' + WindowNo] = f['vol'].shape[1]
        request.session['CT_view_W_' + WindowNo] = f['vol'].shape[2]
        ROI = pydicom.dataset.Dataset.from_json(f['rtss_header'][()])

    request.session['ROI_index_'+WindowNo] = -1
    request.session['ROIname_'+WindowNo] = [ROI.StructureSetROISequence[i].ROIName for i in range(len(ROI.StructureSetROISequence))]
    request.session['Color_'+WindowNo] = list(map(lambda i: list(np.array(ROI.ROIContourSequence[i][0x3006, 0x002a].value, dtype='float')), range(len(ROI.ROIContourSequence))))
    return JsonResponse({}, status=200)


@csrf_exempt
def load_CT_DICOM(request):
    key = request.session['key'].encode()
    fernet = Fernet(key)

    root= request.POST.get('root')
    PID = fernet.decrypt(request.POST.get('PID').encode()).decode()
    MedExecTime = request.POST.get('MedExecTime')
    StudyIDText = request.POST.get('StudyIDText')

    
    dir=root+PID+'\\'+MedExecTime+'\\'+StudyIDText
    fileDir = dir.replace('-', '')
    fileDir = fileDir.replace(' ', '')

    WindowNo = str(1) if (str(request.POST.get('WindowNo')) == 'None') else str(request.POST.get('WindowNo'))
    request.session['Category_' + WindowNo] = 'CT'
    StudyIdIndex = request.session.get('StudyIdIndex')
    StudyIdIndex.update({str(WindowNo): fileDir.split('\\')[-1]})
    request.session['StudyIdIndex'] = StudyIdIndex
    fileExt = r"**\*CT.h5"
    tempPath = list(pathlib.Path(fileDir).glob(fileExt))
    paths = sorted([os.path.join(filename) for filename in tempPath])[0]
    request.session['CT_view_' + WindowNo] = paths
    with h5py.File(paths, "r") as f:
        a_group_key = list(f.keys())
        headers = f[a_group_key[0]]
        request.session['CT_view_pixelspacing_' + WindowNo] = float(
            pydicom.dataset.Dataset.from_json(headers[0]).PixelSpacing[0])
        request.session['CT_view_slicethickness_' + WindowNo] = abs(float(pydicom.dataset.Dataset.from_json(headers[0]).ImagePositionPatient[2])-float(pydicom.dataset.Dataset.from_json(headers[1]).ImagePositionPatient[2]))
        request.session['CT_view_D_' + WindowNo] = f[a_group_key[1]].shape[0]
        request.session['CT_view_H_' + WindowNo] = f[a_group_key[1]].shape[1]
        request.session['CT_view_W_' + WindowNo] = f[a_group_key[1]].shape[2]

    return JsonResponse({}, status=200)



@csrf_exempt
def load_DICOM1(request):
    global CT, PET, CT_tag, PET_tag, CT_view, PET_view, CT_view_tag, PET_view_tag, shiftspacing
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


def localmax(CT_D, CT_H, CT_W, PET, CT_mod_x, CT_mod_y, CT_mod_z, PET_PixelSpacing, PET_SliceThickness, PETWC):

    PET = np.array(h5py.File(PET, "r")['vol'])

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
                    # print(math.sqrt(math.pow(tz, 2) + math.pow(ty, 2) + math.pow(tx, 2))<= RegionSize)
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


def slicing(plane, img_path, variable, drawActualCoordinates, WC, WW, y, tag):
    if variable is None:
        variable = 0
    if plane == 'Axial':
        img = Window_FOR_VIEW(cp.array(h5py.File(img_path, "r")['vol'][variable, :, :]), WC, WW)
        z = tag['D']
    elif plane == 'Coronal':

        img = (Window_FOR_VIEW(((cp.array(h5py.File(img_path, "r")['vol'][:, variable, :]))), WC, WW))
        if drawActualCoordinates == 'true':
            y = y
        z = tag['H']
    elif plane == 'Sagittal':

        img = Window_FOR_VIEW(((cp.array(h5py.File(img_path, "r")['vol'][:, :, variable]))), WC, WW)
        if drawActualCoordinates == 'true':
            y =  y

        z = tag['W']
    return img, y, z


def processing_CT(CT, variable, CTWC, CTWW, plane, x, y, height, drawActualCoordinates, CT_tag,contour_list):
    CTimg, y, z = slicing(plane, CT, variable, drawActualCoordinates, CTWC, CTWW, y, CT_tag)
    resize_shape = CTimg.shape[0:2]
    ratio = (float(CT_tag['SliceThickness']) * resize_shape[0]) / (resize_shape[1] * float(CT_tag['PixelSpacing']))
    CTpil_image = colormapping(CTimg, gray)
    CTpil_image = draw_line(CTpil_image, x, y, plane, height)
    if len(contour_list)!=0:
        CTpil_image=segmentation(CTpil_image,contour_list,variable,plane)
    CTpil_image = to_image(CTpil_image)
    CTimage_uri = to_data_uri(CTpil_image)
    dicom_url = CTimage_uri
    return dicom_url, z, ratio

def segmentation(img,contour_list,variable,plane):
    matched = [match for match in contour_list if plane in match]
    print(matched)
    for filepath in matched:
        f = h5py.File(filepath, "r")
        if str(variable) in list(f.keys()):
            contour=json.loads(f[str(variable)][()])
            for i in list(contour.keys()):
                cv2.drawContours(img, [np.array(contour[i],dtype='int')], 0, (0, 255, 0), thickness=1)
    return img

def processing_RT(img_path, variable, CTWC, CTWW, plane, x, y, height, drawActualCoordinates, CT_tag, Color,
                  ROI_checked):
    CTimg, y, z = slicing(plane, img_path, variable, drawActualCoordinates, CTWC, CTWW, y, CT_tag)
    resize_shape = CTimg.shape[0:2]
    ratio = (float(CT_tag['SliceThickness']) * resize_shape[0]) / (resize_shape[1] * float(CT_tag['PixelSpacing']))
    CTpil_image = colormapping(CTimg, gray).astype(np.uint8)
    CTpil_image = draw_line(CTpil_image, x, y, plane, height)

    if(ROI_checked!=-1):
        CTpil_image = rt_contour(CTpil_image, ROI_checked, Color, img_path, variable,plane)

    CTpil_image = to_image(CTpil_image)
    CTimage_uri = to_data_uri(CTpil_image)
    dicom_url = CTimage_uri
    return dicom_url, z, ratio


def processing_PET(CT_view, PET_view, variable, CTWC, CTWW, PETWC, PETWW, plane, mode, x, y, height,
                   drawActualCoordinates,
                   CT_tag, PET_tag):
    CTimg, y, z = slicing(plane, CT_view, variable, drawActualCoordinates, CTWC, CTWW, y, CT_tag)
    PETimg, _, _ = slicing(plane, PET_view, variable, drawActualCoordinates, PETWC, PETWW, y, CT_tag)
    resize_shape = CTimg.shape[0:2]
    ratio = (float(PET_tag['SliceThickness']) * resize_shape[0]) / (resize_shape[1] * float(CT_tag['PixelSpacing']))
    CTpil_image = colormapping(CTimg, gray)
    PETpil_image = colormapping(PETimg, binary)
    if mode == 'CT':
        CTpil_image = draw_line(CTpil_image, x, y, plane, height)
        CTpil_image = to_image(CTpil_image)
        CTimage_uri = to_data_uri(CTpil_image)
        dicom_url = CTimage_uri
    elif mode == 'PET':
        PETpil_image = draw_line(PETpil_image, x, y, plane, height)
        PETpil_image = to_image(PETpil_image)
        PETimage_uri = to_data_uri(PETpil_image)
        dicom_url = PETimage_uri
    elif mode == 'Fusion':
        CTpil_image = draw_line(CTpil_image, x, y, plane, height)
        PET2Fusion = PETimg
        Fusionimg = colormapping(PET2Fusion, GE)
        Fusionimg = draw_line(Fusionimg, x, y, plane, height)
        Fusionimg = addWeighted(Fusionimg, 0.5, CTpil_image, 0.5, 0)
        Fusionimg = to_image(Fusionimg)
        Fusionimage = Fusionimg
        Fusionimage_uri = to_data_uri(Fusionimage)
        dicom_url = Fusionimage_uri
    return dicom_url, z, ratio


from django.http import JsonResponse


@csrf_exempt
def DICOM_show1(request):
    No = str(1)


    variable = int(request.POST.get('variable'))
    
    CTWC = int(request.POST.get('CTWC'))
    CTWW = int(request.POST.get('CTWW'))
    PETWC = float(request.POST.get('PETWC'))
    PETWW = float(request.POST.get('PETWW'))
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

    if Category == 'PET':
        thickness = request.session.get('PET_slicethickness_' + No)
        Ori_H = request.session.get('CT_H_' + No)
        Ori_W = request.session.get('CT_W_' + No)
        Ori_D = request.session.get('CT_D_' + No)
        if ActualCoordinates == 'false':
            x, y = convert2draw(x, y, Ori_W, Ori_H, Ori_D, plane, width, height)
        CT_view = request.session.get('CT_view_' + No)
        PET_view = request.session.get('PET_view_' + No)
        CT_view_tag = {
            'ImagePositionPatient_F': request.session.get('CT_view_ImagePositionPatient_F_' + No),
            'ImagePositionPatient_S': request.session.get('CT_view_ImagePositionPatient_S_' + No),
            'D': request.session.get('CT_view_D_' + No),
            'H': request.session.get('CT_view_H_' + No),
            'W': request.session.get('CT_view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
        }
        PET_tag = {
            'SliceThickness': request.session.get('PET_slicethickness_' + No),
        }
        dicom_url, z, ratio = processing_PET(CT_view, PET_view, variable, CTWC, CTWW, PETWC, PETWW, plane, mode, x, y,
                                             height, drawActualCoordinates, CT_view_tag, PET_tag)
        
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
            'D': request.session.get('CT_view_D_' + No),
            'H': request.session.get('CT_view_H_' + No),
            'W': request.session.get('CT_view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
            'SliceThickness': request.session.get('CT_view_slicethickness_' + No),
        }
        contour_list=request.session.get('unet_contour_'+No)
        dicom_url, z, ratio = processing_CT(CT, variable, CTWC, CTWW, plane, x, y, height, drawActualCoordinates,
                                            CT_tag,contour_list)
    elif Category == 'RT':
        thickness = request.session.get('CT_view_slicethickness_' + No)
        Ori_H = request.session.get('CT_view_H_' + No)
        Ori_W = request.session.get('CT_view_W_' + No)
        Ori_D = request.session.get('CT_view_D_' + No)
        if ActualCoordinates == 'false':
            x, y = convert2draw(x, y, Ori_W, Ori_H, Ori_D, plane, width, height)
        CT_view = request.session.get('CT_view_' + No)
        CT_view_tag = {
            'ImagePositionPatient_F': request.session.get('CT_view_ImagePositionPatient_F_' + No),
            'ImagePositionPatient_S': request.session.get('CT_view_ImagePositionPatient_S_' + No),
            'D': request.session.get('CT_view_D_' + No),
            'H': request.session.get('CT_view_H_' + No),
            'W': request.session.get('CT_view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
            'SliceThickness': request.session.get('CT_view_slicethickness_' + No),
        }
        dicom_url, z, ratio = processing_RT(CT_view, variable, CTWC, CTWW, plane, x, y, height, drawActualCoordinates,
                                            CT_view_tag, request.session.get('ROI_index_color_' + No),
                                            request.session.get('ROI_index_' + No))
    print(thickness)
    return JsonResponse({"dicom_url": dicom_url, 'z': z, 'ratio': ratio, 'variable': variable,'thickness':thickness})


@csrf_exempt
def DICOM_show2(request):
    No = str(2)
    variable = int(request.POST.get('variable'))
    
    CTWC = int(request.POST.get('CTWC'))
    CTWW = int(request.POST.get('CTWW'))
    PETWC = float(request.POST.get('PETWC'))
    PETWW = float(request.POST.get('PETWW'))
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

    if Category == 'PET':
        thickness = request.session.get('PET_slicethickness_' + No)
        Ori_H = request.session.get('CT_H_' + No)
        Ori_W = request.session.get('CT_W_' + No)
        Ori_D = request.session.get('CT_D_' + No)
        if ActualCoordinates == 'false':
            x, y = convert2draw(x, y, Ori_W, Ori_H, Ori_D, plane, width, height)
        CT_view = request.session.get('CT_view_' + No)
        PET_view = request.session.get('PET_view_' + No)
        CT_view_tag = {
            'ImagePositionPatient_F': request.session.get('CT_view_ImagePositionPatient_F_' + No),
            'ImagePositionPatient_S': request.session.get('CT_view_ImagePositionPatient_S_' + No),
            'D': request.session.get('CT_view_D_' + No),
            'H': request.session.get('CT_view_H_' + No),
            'W': request.session.get('CT_view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
        }
        PET_tag = {
            'SliceThickness': request.session.get('PET_slicethickness_' + No),
        }
        dicom_url, z, ratio = processing_PET(CT_view, PET_view, variable, CTWC, CTWW, PETWC, PETWW, plane, mode, x, y,
                                             height, drawActualCoordinates, CT_view_tag, PET_tag)
        
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
            'D': request.session.get('CT_view_D_' + No),
            'H': request.session.get('CT_view_H_' + No),
            'W': request.session.get('CT_view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
            'SliceThickness': request.session.get('CT_view_slicethickness_' + No),
        }
        contour_list=request.session.get('unet_contour_'+No)
        dicom_url, z, ratio = processing_CT(CT, variable, CTWC, CTWW, plane, x, y, height, drawActualCoordinates,
                                            CT_tag,contour_list)
    elif Category == 'RT':
        thickness = request.session.get('CT_view_slicethickness_' + No)
        Ori_H = request.session.get('CT_view_H_' + No)
        Ori_W = request.session.get('CT_view_W_' + No)
        Ori_D = request.session.get('CT_view_D_' + No)
        if ActualCoordinates == 'false':
            x, y = convert2draw(x, y, Ori_W, Ori_H, Ori_D, plane, width, height)
        CT_view = request.session.get('CT_view_' + No)
        CT_view_tag = {
            'ImagePositionPatient_F': request.session.get('CT_view_ImagePositionPatient_F_' + No),
            'ImagePositionPatient_S': request.session.get('CT_view_ImagePositionPatient_S_' + No),
            'D': request.session.get('CT_view_D_' + No),
            'H': request.session.get('CT_view_H_' + No),
            'W': request.session.get('CT_view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
            'SliceThickness': request.session.get('CT_view_slicethickness_' + No),
        }
        dicom_url, z, ratio = processing_RT(CT_view, variable, CTWC, CTWW, plane, x, y, height, drawActualCoordinates,
                                            CT_view_tag, request.session.get('ROI_index_color_' + No),
                                            request.session.get('ROI_index_' + No))
    return JsonResponse({"dicom_url": dicom_url, 'z': z, 'ratio': ratio, 'variable': variable,'thickness':thickness})


@csrf_exempt
def DICOM_show3(request):
    No = str(3)
    variable = int(request.POST.get('variable'))
    
    CTWC = int(request.POST.get('CTWC'))
    CTWW = int(request.POST.get('CTWW'))
    PETWC = float(request.POST.get('PETWC'))
    PETWW = float(request.POST.get('PETWW'))
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

    if Category == 'PET':
        thickness = request.session.get('PET_slicethickness_' + No)
        Ori_H = request.session.get('CT_H_' + No)
        Ori_W = request.session.get('CT_W_' + No)
        Ori_D = request.session.get('CT_D_' + No)
        if ActualCoordinates == 'false':
            x, y = convert2draw(x, y, Ori_W, Ori_H, Ori_D, plane, width, height)
        CT_view = request.session.get('CT_view_' + No)
        PET_view = request.session.get('PET_view_' + No)
        CT_view_tag = {
            'ImagePositionPatient_F': request.session.get('CT_view_ImagePositionPatient_F_' + No),
            'ImagePositionPatient_S': request.session.get('CT_view_ImagePositionPatient_S_' + No),
            'D': request.session.get('CT_view_D_' + No),
            'H': request.session.get('CT_view_H_' + No),
            'W': request.session.get('CT_view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
        }
        PET_tag = {
            'SliceThickness': request.session.get('PET_slicethickness_' + No),
        }
        dicom_url, z, ratio = processing_PET(CT_view, PET_view, variable, CTWC, CTWW, PETWC, PETWW, plane, mode, x, y,
                                             height, drawActualCoordinates, CT_view_tag, PET_tag)
        
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
            'D': request.session.get('CT_view_D_' + No),
            'H': request.session.get('CT_view_H_' + No),
            'W': request.session.get('CT_view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
            'SliceThickness': request.session.get('CT_view_slicethickness_' + No),
        }
        contour_list=request.session.get('unet_contour_'+No)
        dicom_url, z, ratio = processing_CT(CT, variable, CTWC, CTWW, plane, x, y, height, drawActualCoordinates,
                                            CT_tag,contour_list)
    elif Category == 'RT':
        thickness = request.session.get('CT_view_slicethickness_' + No)
        Ori_H = request.session.get('CT_view_H_' + No)
        Ori_W = request.session.get('CT_view_W_' + No)
        Ori_D = request.session.get('CT_view_D_' + No)
        if ActualCoordinates == 'false':
            x, y = convert2draw(x, y, Ori_W, Ori_H, Ori_D, plane, width, height)
        CT_view = request.session.get('CT_view_' + No)
        CT_view_tag = {
            'ImagePositionPatient_F': request.session.get('CT_view_ImagePositionPatient_F_' + No),
            'ImagePositionPatient_S': request.session.get('CT_view_ImagePositionPatient_S_' + No),
            'D': request.session.get('CT_view_D_' + No),
            'H': request.session.get('CT_view_H_' + No),
            'W': request.session.get('CT_view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
            'SliceThickness': request.session.get('CT_view_slicethickness_' + No),
        }
        dicom_url, z, ratio = processing_RT(CT_view, variable, CTWC, CTWW, plane, x, y, height, drawActualCoordinates,
                                            CT_view_tag, request.session.get('ROI_index_color_' + No),
                                            request.session.get('ROI_index_' + No))
    return JsonResponse({"dicom_url": dicom_url, 'z': z, 'ratio': ratio, 'variable': variable,'thickness':thickness})


@csrf_exempt
def DICOM_show4(request):
    No = str(4)
    variable = int(request.POST.get('variable'))
    
    CTWC = int(request.POST.get('CTWC'))
    CTWW = int(request.POST.get('CTWW'))
    PETWC = float(request.POST.get('PETWC'))
    PETWW = float(request.POST.get('PETWW'))
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

    if Category == 'PET':
        thickness = request.session.get('PET_slicethickness_' + No)
        Ori_H = request.session.get('CT_H_' + No)
        Ori_W = request.session.get('CT_W_' + No)
        Ori_D = request.session.get('CT_D_' + No)
        if ActualCoordinates == 'false':
            x, y = convert2draw(x, y, Ori_W, Ori_H, Ori_D, plane, width, height)
        CT_view = request.session.get('CT_view_' + No)
        PET_view = request.session.get('PET_view_' + No)
        CT_view_tag = {
            'ImagePositionPatient_F': request.session.get('CT_view_ImagePositionPatient_F_' + No),
            'ImagePositionPatient_S': request.session.get('CT_view_ImagePositionPatient_S_' + No),
            'D': request.session.get('CT_view_D_' + No),
            'H': request.session.get('CT_view_H_' + No),
            'W': request.session.get('CT_view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
        }
        PET_tag = {
            'SliceThickness': request.session.get('PET_slicethickness_' + No),
        }
        dicom_url, z, ratio = processing_PET(CT_view, PET_view, variable, CTWC, CTWW, PETWC, PETWW, plane, mode, x, y,
                                             height, drawActualCoordinates, CT_view_tag, PET_tag)
        
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
            'D': request.session.get('CT_view_D_' + No),
            'H': request.session.get('CT_view_H_' + No),
            'W': request.session.get('CT_view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
            'SliceThickness': request.session.get('CT_view_slicethickness_' + No),
        }
        contour_list=request.session.get('unet_contour_'+No)
        dicom_url, z, ratio = processing_CT(CT, variable, CTWC, CTWW, plane, x, y, height, drawActualCoordinates,
                                            CT_tag,contour_list)
    elif Category == 'RT':
        thickness = request.session.get('CT_view_slicethickness_' + No)
        Ori_H = request.session.get('CT_view_H_' + No)
        Ori_W = request.session.get('CT_view_W_' + No)
        Ori_D = request.session.get('CT_view_D_' + No)
        if ActualCoordinates == 'false':
            x, y = convert2draw(x, y, Ori_W, Ori_H, Ori_D, plane, width, height)
        CT_view = request.session.get('CT_view_' + No)
        CT_view_tag = {
            'ImagePositionPatient_F': request.session.get('CT_view_ImagePositionPatient_F_' + No),
            'ImagePositionPatient_S': request.session.get('CT_view_ImagePositionPatient_S_' + No),
            'D': request.session.get('CT_view_D_' + No),
            'H': request.session.get('CT_view_H_' + No),
            'W': request.session.get('CT_view_W_' + No),
            'PixelSpacing': request.session.get('CT_view_pixelspacing_' + No),
            'SliceThickness': request.session.get('CT_view_slicethickness_' + No),
        }
        dicom_url, z, ratio = processing_RT(CT_view, variable, CTWC, CTWW, plane, x, y, height, drawActualCoordinates,
                                            CT_view_tag, request.session.get('ROI_index_color_' + No),
                                            request.session.get('ROI_index_' + No))
    return JsonResponse({"dicom_url": dicom_url, 'z': z, 'ratio': ratio, 'variable': variable,'thickness':thickness})


from .models import Localization
import datetime


@csrf_exempt
def convertLocation(request):
    height = float(request.POST.get('height'))
    width = float(request.POST.get('width'))
    plane = request.POST.get('plane')
    x = float(request.POST.get('x'))
    y = float(request.POST.get('y'))
    z = float(request.POST.get('z'))
    WindowNo = str(request.POST.get('WindowNo'))

    Ori_H = request.session.get('CT_view_H_' + WindowNo)
    Ori_W = request.session.get('CT_view_W_' + WindowNo)
    Ori_D = request.session.get('CT_view_D_' + WindowNo)
    Position_F = request.session.get('CT_view_ImagePositionPatient_F_' + WindowNo)
    Position_S = request.session.get('CT_view_ImagePositionPatient_S_' + WindowNo)
    x, y, z = convert(x, y, z, Ori_W, Ori_H, Ori_D, plane, width, height, Position_F, Position_S)
    # CT_mod座標
    request.session['Click_X'] = x
    request.session['Click_X'] = y
    request.session['Click_X'] = z
    return JsonResponse({'x': x, 'y': y, 'z': z})


@csrf_exempt
def insertLocation(request):
    Click_X = request.session.get('Click_X')
    Click_Y = request.session.get('Click_X')
    Click_Z = request.session.get('Click_X')
    height = float(request.POST.get('height'))
    width = float(request.POST.get('width'))
    plane = request.POST.get('plane')
    x = float(request.POST.get('x'))
    y = float(request.POST.get('y'))
    z = float(request.POST.get('z'))
    StudyID = request.POST.get('StudyID')
    WindowNo = str(request.POST.get('WindowNo'))
    
    key = request.session['key'].encode()
    fernet = Fernet(key)
    PID = 'null' if (str(request.POST.get('PID')) == '') else fernet.decrypt(request.POST.get('PID').encode()).decode()
    SD = '' if (str(request.POST.get('SD')) == '') else str(request.POST.get('SD'))
    Item = '' if (str(request.POST.get('Item')) == '') else str(request.POST.get('Item'))
    date = '' if (str(request.POST.get('date')) == '') else str(request.POST.get('date'))
    username = 'null' if (str(request.POST.get('username')) == '') else str(request.POST.get('username'))
    SUV = '0' if (str(request.POST.get('SUV')) == '') else str(request.POST.get('SUV'))
    Disease = '' if (str(request.POST.get('Disease')) == '') else str(request.POST.get('Disease'))
    Type = Item.replace(' ', '')

    if Type == 'PET':
        PET_H = request.session.get('PET_H_' + WindowNo)
        PET_W = request.session.get('PET_W_' + WindowNo)
        PET_D = request.session.get('PET_D_' + WindowNo)
        CT_H = request.session.get('CT_view_H_' + WindowNo)
        CT_W = request.session.get('CT_view_W_' + WindowNo)
        CT_D = request.session.get('CT_view_D_' + WindowNo)
        x = (x * (PET_W / CT_W))
        y = (y * (PET_H / CT_H))
        z = (z * (PET_D / CT_D))
        Click_X = (Click_X * (PET_W / CT_W))
        Click_Y = (Click_Y * (PET_H / CT_H))
        Click_Z = (Click_Z * (PET_D / CT_D))

    elif Type == 'CT':
        shift = request.session.get('shiftspacing_' + WindowNo) / request.session.get('CT_pixelspacing_' + WindowNo)
        rate = request.session.get('CT_view_pixelspacing_' + WindowNo) / request.session.get(
            'CT_pixelspacing_' + WindowNo)
        x = math.floor(x * rate + shift)
        y = math.floor(y * rate + shift)
        z = math.floor(z * (request.session.get('CT_D_' + WindowNo) / request.session.get('CT_view_D_' + WindowNo)))
        Click_X = math.floor(Click_X * rate + shift)
        Click_Y = math.floor(Click_Y * rate + shift)
        Click_Z = math.floor(
            Click_Z * (request.session.get('CT_D_' + WindowNo) / request.session.get('CT_view_D_' + WindowNo)))
    elif Type == 'RTPLAN':
        x = math.floor(x)
        y = math.floor(y)
        z = math.floor(z)
        Click_X = math.floor(Click_X)
        Click_Y = math.floor(Click_Y)
        Click_Z = math.floor(Click_Z)
    elif Type == 'LDCT':
        x = math.floor(x)
        y = math.floor(y)
        z = math.floor(z)
        Click_X = math.floor(Click_X)
        Click_Y = math.floor(Click_Y)
        Click_Z = math.floor(Click_Z)
    # x, y, z = convert(x, y, z, Ori_W, Ori_H, Ori_D, plane, width, height, CT_tag)

    x = str(x)
    y = str(y)
    z = str(z)
    Click_X = str(Click_X)
    Click_Y = str(Click_Y)
    Click_Z = str(Click_Z)
    LabelGroup = '' if (str(request.POST.get('LabelGroup')) == '') else str(request.POST.get('LabelGroup'))
    LabelName = '' if (str(request.POST.get('LabelName')) == '') else str(request.POST.get('LabelName'))
    LabelRecord = '' if (str(request.POST.get('LabelRecord')) == '') else str(request.POST.get('LabelRecord'))
    query = '''insert into　Localization (PID,SD,Item,date,username,SUV,x,y,z,LabelGroup,LabelName,LabelRecord,Click_X,Click_Y,Click_Z,Disease,StudyID) 
    values(''' + PID + ",'" + SD + "','" + Item + "','" + date + "','" + username + "'," + SUV + "," + x + "," + y + "," + z + ",'" + LabelGroup + "','" + LabelName + "','" + LabelRecord + "'," + Click_X + "," + Click_Y + "," + Click_Z + "," + Disease + "," + StudyID + ''')'''

    cursor = connections['default'].cursor()
    cursor.execute(query)

    string = request.POST.get('str').split(',')
    Study_Date = request.POST.get('Study_Date').split(',')
    StudyIdIndex = request.session.get('StudyIdIndex')
    Disease = '' if (str(request.POST.get('Disease')) == '') else str(request.POST.get('Disease'))
    key = request.session['key'].encode()
    fernet = Fernet(key)
    PID = 'null' if (str(request.POST.get('PID')) == '') else fernet.decrypt(request.POST.get('PID').encode()).decode()
    string = request.POST.get('str').split(',')
    query = '''select　* from Localization where  PID=%s and (username=%s or username='') and Disease=%s and StudyID in (%s,%s,%s,%s) and date in (%s,%s,%s,%s) order by date,LabelName'''
    cursor = connections['default'].cursor()

    cursor.execute(query,
                   [PID, str(request.POST.get('username')), Disease, string[0], string[1],
                    string[2], string[3],Study_Date[0],Study_Date[1],Study_Date[2],Study_Date[3]])
    response = cursor.fetchall()
    id, PID, SD, Item, date, username, SUV, x, y, z, LabelGroup, LabelName, LabelRecord, StudyID = [], [], [], [], [], [], [], [], [], [], [], [], [], []
    for info in response:
        Type = str(info[3]).replace(' ', '')

        ind = str(list(StudyIdIndex.keys())[list(StudyIdIndex.values()).index(str(info[17]))])

        if Type == 'PET':
            PET_H = request.session.get('PET_H_' + ind)
            PET_W = request.session.get('PET_W_' + ind)
            PET_D = request.session.get('PET_D_' + ind)
            CT_H = request.session.get('CT_view_H_' + ind)
            CT_W = request.session.get('CT_view_W_' + ind)
            CT_D = request.session.get('CT_view_D_' + ind)
            rx = math.ceil((float(info[7]) / (PET_W / CT_W)))
            ry = math.ceil((float(info[8]) / (PET_H / CT_H)))
            rz = math.ceil((float(info[9]) / (PET_D / CT_D)))

        elif Type == 'CT':
            shift = request.session.get('shiftspacing_' + ind) / request.session.get('CT_pixelspacing_' + ind)
            rate = request.session.get('CT_view_pixelspacing_' + ind) / request.session.get('CT_pixelspacing_' + ind)
            rx = math.ceil((float(info[7]) - shift) / rate)
            ry = math.ceil((float(info[8]) - shift) / rate)
            rz = math.ceil(
                float(info[9]) / (request.session.get('CT_D_' + ind) / request.session.get('CT_view_D_' + ind)))
        elif Type == 'RTPLAN':
            rx = math.ceil(float(info[7]))
            ry = math.ceil(float(info[8]))
            rz = math.ceil(float(info[9]))
        elif Type == 'LDCT':
            rx = math.ceil(float(info[7]))
            ry = math.ceil(float(info[8]))
            rz = math.ceil(float(info[9]))
        id.append(info[0])
        PID.append(fernet.encrypt(info[1].encode()).decode())
        SD.append(info[2])
        Item.append(info[3])
        date.append(info[4])
        username.append(info[5])
        if float(info[6]) == 0:
            SUV.append('')
        else:
            SUV.append(round(float(info[6]), 3))
        x.append(rx)
        y.append(ry)
        z.append(rz)
        LabelGroup.append(info[10])
        LabelName.append(info[11])
        LabelRecord.append(info[12])
        StudyID.append(info[17])
    # print('shift:',shift,'| shiftspacing:',shiftspacing,'| CT_view_PixelSpacing:',float(CT_view_tag[0].PixelSpacing[0]),'| CT_PixelSpacing:',float(CT_tag[0].PixelSpacing[0]),'| CT_ImagePosition:',(CT_tag[0].ImagePositionPatient),'| CT_view_ImagePosition:',(CT_view_tag[0].ImagePositionPatient))
    _, indices = np.unique(StudyID, return_inverse=True)
    indices = list(indices.astype('float'))

    return JsonResponse(
        {'id': id, 'PID': PID, 'SD': SD, 'Item': Item, 'date': date, 'username': username, 'SUV': SUV, 'x': x, 'y': y,
         'z': z, 'LabelGroup': LabelGroup, 'LabelName': LabelName, 'LabelRecord': LabelRecord, 'StudyID': StudyID,
         'indices': indices},
        status=200)


@csrf_exempt
def deleteLocation(request):

    query = '''delete from Localization where id=''' + str(request.POST.get('id'))
    cursor = connections['default'].cursor()
    cursor.execute(query)
    StudyIdIndex = request.session.get('StudyIdIndex')
    Disease = '' if (str(request.POST.get('Disease')) == '') else str(request.POST.get('Disease'))
    # response = Localization.objects.filter(pid=request.POST.get('PID'), username=request.POST.get('username'))
    string = request.POST.get('str').split(',')
    Study_Date = request.POST.get('Study_Date').split(',')
    query = '''select　* from Localization where  PID=%s and (username=%s or username='') and Disease=%s and StudyID in (%s,%s,%s,%s) and date in (%s,%s,%s,%s) order by date,LabelName'''
    cursor = connections['default'].cursor()

    key = request.session['key'].encode()
    fernet = Fernet(key)
    PID = 'null' if (str(request.POST.get('PID')) == '') else fernet.decrypt(request.POST.get('PID').encode()).decode()

    cursor.execute(query,
                   [PID, str(request.POST.get('username')), Disease, string[0], string[1],
                    string[2], string[3],Study_Date[0],Study_Date[1],Study_Date[2],Study_Date[3]])
    response = cursor.fetchall()
    id, PID, SD, Item, date, username, SUV, x, y, z, LabelGroup, LabelName, LabelRecord, StudyID = [], [], [], [], [], [], [], [], [], [], [], [], [], []

    for info in response:
        Type = str(info[3]).replace(' ', '')

        ind = str(list(StudyIdIndex.keys())[list(StudyIdIndex.values()).index(str(info[17]))])

        if Type == 'PET':
            PET_H = request.session.get('PET_H_' + ind)
            PET_W = request.session.get('PET_W_' + ind)
            PET_D = request.session.get('PET_D_' + ind)
            CT_H = request.session.get('CT_view_H_' + ind)
            CT_W = request.session.get('CT_view_W_' + ind)
            CT_D = request.session.get('CT_view_D_' + ind)
            rx = math.ceil((float(info[7]) / (PET_W / CT_W)))
            ry = math.ceil((float(info[8]) / (PET_H / CT_H)))
            rz = math.ceil((float(info[9]) / (PET_D / CT_D)))

        elif Type == 'CT':
            shift = request.session.get('shiftspacing_' + ind) / request.session.get('CT_pixelspacing_' + ind)
            rate = request.session.get('CT_view_pixelspacing_' + ind) / request.session.get('CT_pixelspacing_' + ind)
            rx = math.ceil((float(info[7]) - shift) / rate)
            ry = math.ceil((float(info[8]) - shift) / rate)
            rz = math.ceil(
                float(info[9]) / (request.session.get('CT_D_' + ind) / request.session.get('CT_view_D_' + ind)))
        elif Type == 'RTPLAN':
            rx = math.ceil(float(info[7]))
            ry = math.ceil(float(info[8]))
            rz = math.ceil(float(info[9]))
        elif Type == 'LDCT':
            rx = math.ceil(float(info[7]))
            ry = math.ceil(float(info[8]))
            rz = math.ceil(float(info[9]))
        id.append(info[0])
        PID.append(fernet.encrypt(info[1].encode()).decode())
        SD.append(info[2])
        Item.append(info[3])
        date.append(info[4])
        username.append(info[5])
        if float(info[6]) == 0:
            SUV.append('')
        else:
            SUV.append(round(float(info[6]), 3))
        x.append(rx)
        y.append(ry)
        z.append(rz)
        LabelGroup.append(info[10])
        LabelName.append(info[11])
        LabelRecord.append(info[12])
        StudyID.append(info[17])
    # print('shift:',shift,'| shiftspacing:',shiftspacing,'| CT_view_PixelSpacing:',float(CT_view_tag[0].PixelSpacing[0]),'| CT_PixelSpacing:',float(CT_tag[0].PixelSpacing[0]),'| CT_ImagePosition:',(CT_tag[0].ImagePositionPatient),'| CT_view_ImagePosition:',(CT_view_tag[0].ImagePositionPatient))
    _, indices = np.unique(StudyID, return_inverse=True)
    indices = list(indices.astype('float'))
    return JsonResponse(
        {'id': id, 'PID': PID, 'SD': SD, 'Item': Item, 'date': date, 'username': username, 'SUV': SUV, 'x': x, 'y': y,
         'z': z, 'LabelGroup': LabelGroup, 'LabelName': LabelName, 'LabelRecord': LabelRecord, 'StudyID': StudyID,
         'indices': indices},
        status=200)


@csrf_exempt
def selectLocation(request):
    StudyIdIndex = request.session.get('StudyIdIndex')
    Disease = '' if (str(request.POST.get('Disease')) == '') else str(request.POST.get('Disease'))
    # response = Localization.objects.filter(pid=request.POST.get('PID'), username=request.POST.get('username'))
    key = request.session['key'].encode()
    fernet = Fernet(key)
    PID = 'null' if (str(request.POST.get('PID')) == '') else fernet.decrypt(request.POST.get('PID').encode()).decode()
    string = request.POST.get('str').split(',')
    studyDate = request.POST.get('date').split(',')

    query = '''select　* from Localization where  PID=%s and (username=%s or username='') and Disease=%s and StudyID in (%s,%s,%s,%s) and date in (%s,%s,%s,%s) order by date,LabelName'''
    cursor = connections['default'].cursor()

    cursor.execute(query,
                   [PID, str(request.POST.get('username')), Disease, string[0], string[1],
                    string[2], string[3],studyDate[0],studyDate[1],studyDate[2],studyDate[3]])
    response = cursor.fetchall()
    id, PID, SD, Item, date, username, SUV, x, y, z, LabelGroup, LabelName, LabelRecord, StudyID = [], [], [], [], [], [], [], [], [], [], [], [], [], []
    for info in response:
        Type = str(info[3]).replace(' ', '')

        ind = str(list(StudyIdIndex.keys())[list(StudyIdIndex.values()).index(str(info[17]))])

        if Type == 'PET':
            PET_H = request.session.get('PET_H_' + ind)
            PET_W = request.session.get('PET_W_' + ind)
            PET_D = request.session.get('PET_D_' + ind)
            CT_H = request.session.get('CT_view_H_' + ind)
            CT_W = request.session.get('CT_view_W_' + ind)
            CT_D = request.session.get('CT_view_D_' + ind)
            rx = math.ceil((float(info[7]) / (PET_W / CT_W)))
            ry = math.ceil((float(info[8]) / (PET_H / CT_H)))
            rz = math.ceil((float(info[9]) / (PET_D / CT_D)))

        elif Type == 'CT':
            shift = request.session.get('shiftspacing_' + ind) / request.session.get('CT_pixelspacing_' + ind)
            rate = request.session.get('CT_view_pixelspacing_' + ind) / request.session.get('CT_pixelspacing_' + ind)
            rx = math.ceil((float(info[7]) - shift) / rate)
            ry = math.ceil((float(info[8]) - shift) / rate)
            rz = math.ceil(
                float(info[9]) / (request.session.get('CT_D_' + ind) / request.session.get('CT_view_D_' + ind)))
        elif Type == 'RTPLAN':
            rx = math.ceil(float(info[7]))
            ry = math.ceil(float(info[8]))
            rz = math.ceil(float(info[9]))
        elif Type == 'LDCT':
            rx = math.ceil(float(info[7]))
            ry = math.ceil(float(info[8]))
            rz = math.ceil(float(info[9]))
        id.append(info[0])
        PID.append(fernet.encrypt(info[1].encode()).decode())
        SD.append(info[2])
        Item.append(info[3])
        date.append(info[4])
        username.append(info[5])
        if float(info[6]) == 0:
            SUV.append('')
        else:
            SUV.append(round(float(info[6]), 3))
        x.append(rx)
        y.append(ry)
        z.append(rz)
        LabelGroup.append(info[10])
        LabelName.append(info[11])
        LabelRecord.append(info[12])
        StudyID.append(info[17])
    # print('shift:',shift,'| shiftspacing:',shiftspacing,'| CT_view_PixelSpacing:',float(CT_view_tag[0].PixelSpacing[0]),'| CT_PixelSpacing:',float(CT_tag[0].PixelSpacing[0]),'| CT_ImagePosition:',(CT_tag[0].ImagePositionPatient),'| CT_view_ImagePosition:',(CT_view_tag[0].ImagePositionPatient))
    _, indices = np.unique(StudyID, return_inverse=True)
    indices = list(indices.astype('float'))
    return JsonResponse(
        {'id': id, 'PID': PID, 'SD': SD, 'Item': Item, 'date': date, 'username': username, 'SUV': SUV, 'x': x, 'y': y,
         'z': z, 'LabelGroup': LabelGroup, 'LabelName': LabelName, 'LabelRecord': LabelRecord, 'StudyID': StudyID,
         'indices': indices},
        status=200)


@csrf_exempt
def findLocalMax(request):
    x = float(request.POST.get('x'))
    y = float(request.POST.get('y'))
    z = float(request.POST.get('z'))
    PETWC = float(request.POST.get('PETWC'))
    StudyID = str(request.POST.get('StudyID'))
    StudyIdIndex = request.session.get('StudyIdIndex')
    ind = list(StudyIdIndex.keys())[list(StudyIdIndex.values()).index(StudyID)]

    PET = request.session.get('PET_' + str(ind))
    CT_D = request.session.get('CT_view_D_' + str(ind))
    CT_H = request.session.get('CT_view_H_' + str(ind))
    CT_W = request.session.get('CT_view_W_' + str(ind))
    PET_PixelSpacing = request.session.get('PET_pixelspacing_' + str(ind))
    PET_SliceThickness = request.session.get('PET_slicethickness_' + str(ind))

    x, y, z, maxValue = localmax(CT_D, CT_H, CT_W, PET, x, y, z, PET_PixelSpacing, PET_SliceThickness, PETWC)


    # print(x)
    return JsonResponse({'x': x, 'y': y, 'z': z, 'maxValue': maxValue})


@csrf_exempt
def findSUV(request):
    x = float(request.POST.get('x'))
    y = float(request.POST.get('y'))
    z = float(request.POST.get('z'))
    isNotPET = request.POST.get('isNotPET')
    StudyID = request.POST.get('StudyID')
    StudyIdIndex = request.session.get('StudyIdIndex')
    ind = str(list(StudyIdIndex.keys())[list(StudyIdIndex.values()).index(str(StudyID))])

    if not (isNotPET):
        PET_H = request.session.get('PET_H_' + ind)
        PET_W = request.session.get('PET_W_' + ind)
        PET_D = request.session.get('PET_D_' + ind)
        CT_H = request.session.get('CT_view_H_' + ind)
        CT_W = request.session.get('CT_view_W_' + ind)
        CT_D = request.session.get('CT_view_D_' + ind)
        PET_X = round(x * (PET_W / CT_W))
        PET_Y = round(y * (PET_H / CT_H))
        PET_Z = round(z * (PET_D / CT_D))
        PET = request.session.get('PET_' + ind)
        SUV = np.array(h5py.File(PET, "r")['vol'])[PET_Z, PET_Y, PET_X]
        SUV = np.float64(SUV)
    else:
        SUV = ''
    return JsonResponse({'SUV': SUV})


from .models import Drugset, Drugsetlog, Examreporttext, Meditem, Medorder, Visitrecord
from django.db import connections


@csrf_exempt
def ImagePath(request):
    condition = request.POST.get('PID')
    query = '''select ChartNo,ExecDate,TypeName from AllExam left join MedTypeSet on  AllExam.MedType=MedTypeSet.MedType where ChartNo=''' + condition
    cursor = connections['default'].cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    PID = res[0][0]
    MedExecTime = str(res[0][1]).replace('-', '')
    Item = res[0][2]
    request.session['PID'] = PID
    request.session['MedExecTime'] = MedExecTime
    request.session['Item'] = Item
    return JsonResponse({'PID': PID, 'MedExecTime': MedExecTime, 'Item': Item})


@csrf_exempt
def TextReport(request):
    MedExecTime= request.session.get('MedExecTime', 0)
    key = request.session['key'].encode()
    fernet = Fernet(key)
    series_number = fernet.decrypt(request.POST.get('PID').encode()).decode()

    query = '''select TypeName,a.eventDate,a.reportText from allEvents as a inner join medTypeSet as b on a.medType=b.MedType where chartNo=%s and medType <30000　order by eventDate DESC'''
    cursor = connections['default'].cursor()
    cursor.execute(query,[series_number])
    examItem = []
    examDate = []
    examReport = []
    exam = cursor.fetchall()

    for i in range(len(exam)):
        examItem.append(exam[i][0].replace(' ', ''))
        examDate.append(str(exam[i][1]).split(' ')[0])
        examReport.append(exam[i][2])
    datefloat = string2date(examDate)

    # print([MedExecTime])
    MedExecTime_mod = string2date([MedExecTime])
    idx = int(np.argmin(np.abs(datefloat - MedExecTime_mod)))

    return JsonResponse({'examItem': examItem, 'examDate': examDate, 'examReport': examReport, 'idx': idx})


import pandas as pd


def string2date(str):
    str = pd.to_datetime(str)
    str = np.array(str, dtype=np.datetime64)
    str = np.float64(str)
    return str


@csrf_exempt
def LabelGroup(request):
    query = '''
            select SeqNo as 'GroupID',LabelGroup
            from SubjectLabelGroup 
            where SubjectID=''' + str(request.POST.get('SubjectID')) + ''' group by SeqNo,LabelGroup
            '''
    cursor = connections['default'].cursor()
    cursor.execute(query)
    GroupID = []
    LabelGroup = []
    res = cursor.fetchall()
    for i in range(len(res)):
        GroupID.append(res[i][0])
        LabelGroup.append(res[i][1])
    return JsonResponse({'GroupID': GroupID, 'LabelGroup': LabelGroup})


@csrf_exempt
def LabelName(request):
    # print(str(request.POST.get('LabelGroup')))
    query = '''
            select　b.LabelName
            from SubjectLabelGroup as a left outer join SubjectLabelContent as b on a.LabelGroupID=b.LabelGroupID
		　　where  SubjectID=''' + str(request.POST.get('SubjectID')) + ''' and a.SeqNo=''' + str(
        request.POST.get('LabelGroup'))
    cursor = connections['default'].cursor()
    cursor.execute(query)
    LabelName = []
    res = cursor.fetchall()
    for i in range(len(res)):
        LabelName.append(res[i][0])
    return JsonResponse({'LabelName': LabelName})


@csrf_exempt
def PatientImageInfo(request):
    key = request.session['key'].encode()
    fernet = Fernet(key)
    PID = fernet.decrypt(request.POST.get('PID').encode()).decode()


    query = ''' select b.chartNo,a.studyID,a.studyDes,a.studyDate,a.sliceNo,a.eventID from ExamStudySeries_6  
                as a inner join allEvents as b on a.eventID=b.eventID where sliceNo in
                (select MAX(sliceNo) from (
                select eventID,orderNo,studyID,studyDes,seriesID,seriesDes,sliceNo,studyDate
                from ExamStudySeries_6) as a left outer join allEvents as b on a.eventID=b.eventID 
                where b.chartNo=%s group by a.studyID,a.studyDate) and b.chartNo=%s
                group by b.chartNo,a.studyID,a.studyDes,a.studyDate,a.sliceNo,a.eventID
            '''
    cursor = connections['default'].cursor()
    cursor.execute(query, [PID, PID])
    res = cursor.fetchall()
    ChartNo = []
    StudyID = []
    StudyDes = []
    ExecDate = []
    SliceNo = []
    for i in range(len(res)):
        ChartNo.append(fernet.encrypt(str(res[i][0]).encode()).decode())
        StudyID.append(res[i][1])
        StudyDes.append(res[i][2])
        ExecDate.append(res[i][3])
        SliceNo.append(res[i][4])
    return JsonResponse({'ChartNo': ChartNo,
                         'StudyID': StudyID,
                         'StudyDes': StudyDes,
                         'ExecDate': ExecDate,
                         'SliceNo': SliceNo
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
        if plane == 'Axial':
            rt_img = np.int32((h5py.File(Path, "r")['rtss_vol'][variable, :, :] >> ROI_checked[i]) % 2)
        elif plane == 'Coronal':
            rt_img = np.int32((h5py.File(Path, "r")['rtss_vol'][:, variable, :] >> ROI_checked[i]) % 2)

        elif plane == 'Sagittal':
            rt_img = np.int32((h5py.File(Path, "r")['rtss_vol'][:, :, variable] >> ROI_checked[i]) % 2)
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
    print(x,'_',y,'_',z)
    
    img_path = request.session.get('CT_view_' + WindowNo)
    unet_contour_path = img_path.replace(img_path.split('\\')[-1],'')+id+'_'+plane+"_unet.h5"
    for plane in ['Axial','Coronal','Sagittal']:
        unet_contour_path = img_path.replace(img_path.split('\\')[-1],'')+id+'_'+plane+"_unet.h5"
        contour_list=request.session.get('unet_contour_'+WindowNo)
        if unet_contour_path not in contour_list : 
            contour_list.append(unet_contour_path)
            request.session['unet_contour_'+WindowNo]=contour_list
    if not os.path.isfile(unet_contour_path):
        pad_size = 160
        size = 20
        vol = np.array(h5py.File(img_path, "r")['vol'][(z-size):(z+size), (y-size):(y+size), (x-size):(x+size)])
        pad_x = np.repeat(np.array((pad_size - vol.shape[1]) / 2), 2).astype('int')
        pad_y = np.repeat(np.array((pad_size - vol.shape[2]) / 2), 2).astype('int')
        vol = np.pad(vol, pad_width=((0, 0),pad_x, pad_y), mode='constant', constant_values=-2000)
        vol = Window(vol, -550, 1600)
        mask = model_UNet.predict(vol)
        predict = mask.argmax(axis=3)
        print(predict.shape)
        for plane in ['Axial','Coronal','Sagittal']:
            unet_contour_path = img_path.replace(img_path.split('\\')[-1],'')+id+'_'+plane+"_unet.h5"
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
                        print(str((y-int(pad_size/2))+j))
                        hf.create_dataset(str((y-int(pad_size/2))+j), data=json.dumps(contour))
                    elif plane == 'Sagittal':
                        hf.create_dataset(str((x-int(pad_size/2))+j), data=json.dumps(contour))
                    

    return JsonResponse({}, status=200)
    
@csrf_exempt
def window_load(request):
    WindowNo = str(request.POST.get('WindowNo'))
    request.session['unet_contour_'+WindowNo]=[]

    return JsonResponse({}, status=200)   
    