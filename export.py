import pymssql
import pathlib
import pydicom
import os
import pathlib
import numpy as np
import h5py
import xml.etree.ElementTree as ET
from scipy.io import savemat
import pandas as pd
import math
from tqdm import tqdm, trange
'''
Connect mssql by using pymssql
Cursor is a key element
Using Cursor and query can control database 
'''
connect = pymssql.connect(
    host='172.31.6.157',
    user='TEST',
    password='81218',
    database='AICH'
)

root=r'\\172.31.6.6\share1\NFS\image'


'''
First, searching PatientID 
'''
list_file_dir = input('請輸入清單位置:')
user=input('請輸入所標註帳號:')
diseaseNo = input('請輸入研究主題編號:')
saveFilePath = input('請輸入儲存影像路徑:')
date1 = input('請輸入標註日期範圍(前)，格式:yyyy-mm-dd:')
date2 = input('請輸入標註日期範圍(後)，格式:yyyy-mm-dd:')
list_file = list(pathlib.Path(list_file_dir).glob("*.csv"))[0]
PatientListID=pd.read_csv(list_file,header=None).iloc[:,0].values.tolist()


cursor = connect.cursor(as_dict=True)
for i in tqdm(range(len(PatientListID))):
    #取得標記資料
    query = '''
    select * from Localization where PID=%(var1)s and username=%(var2)s and Disease=%(var3)s 
     and CONVERT(date,[date]) >= %(var4)s　and　CONVERT(date,[date]) <= %(var5)s
    '''
    cursor.execute(query, {'var1': PatientListID[i],'var2':user,'var3':diseaseNo,'var4':date1,'var5':date2})

    SD = []


    for row in cursor:
        SD.append(row['StudyID'])

    if len(SD)!=0:#代表有標記資料


        query = '''
        select PID ,SD,StudyID,seriesID from Localization where PID=%(var1)s and username=%(var2)s and Disease=%(var3)s and CONVERT(date,[date]) >= %(var4)s　and　CONVERT(date,[date]) <= %(var5)s group by PID,SD,StudyID,seriesID''' #取得影像位置資料
        cursor.execute(query, {'var1': PatientListID[i],'var2':user,'var3':diseaseNo,'var4':date1,'var5':date2})
        res = cursor.fetchall()

        for j in range(len(res)):
            

            PID = str(res[j]['PID'])
            MedExecTime = str(res[j]['SD'].replace('-',''))
            StudyID = str(res[j]['StudyID'])
            seriesID = str(res[j]['seriesID'])
            fileDir = os.path.join(r'\\172.31.6.6\share1\NFS\image',PID,MedExecTime,StudyID,seriesID)
            fileDir = fileDir.replace('-','')
            fileDir = fileDir.replace(' ', '')

            saveFiledir = os.path.join(saveFilePath,'image',PID,MedExecTime,StudyID,seriesID)
            pathlib.Path(saveFiledir).mkdir(parents=True, exist_ok=True)

            tempPath = list(pathlib.Path(fileDir).glob('*PETCT.h5'))

            paths = sorted([os.path.join(filename) for filename in tempPath])[0]
            with h5py.File(paths, "r") as f:
                a_group_key = list(f.keys())
                CT_header = f['CT_header']
                PET_header = f['PET_header']
                CT_tag = []
                PET_tag = []
                for header in CT_header:
                    CT_tag.append(pydicom.dataset.Dataset.from_json(header))      
                for header in PET_header:
                    PET_tag.append(pydicom.dataset.Dataset.from_json(header))         
                PET = np.array(f['PET_vol'])


            tempPath = list(pathlib.Path(fileDir).glob('*PETCTmod_Axial.h5'))
            paths = sorted([os.path.join(filename) for filename in tempPath])[0]
            with h5py.File(paths, "r") as f:
                CT_view = np.array(f['PETCT_vol'])[:, 1, :, :] #0是PET 1是CT_mod


            query = '''
            select * from Localization where PID=%(var1)s and username=%(var2)s and Disease=%(var3)s and StudyID=%(var4)s and seriesID=%(var5)s
            '''
            cursor.execute(query, {'var1': PID,'var2':user,'var3':diseaseNo,'var4':StudyID,'var5':seriesID})
            data = cursor.fetchall()
            #print('PID:',PID,' user:',user,' diseaseNo:',diseaseNo,' StudyID:',StudyID,' seriesID:',seriesID)
            Main = ET.Element('Main')
            Image_Info = ET.SubElement(Main, 'Image_Info')
            PatientID = ET.SubElement(Image_Info, 'PatientID')
            PatientID.text = str(PET_tag[0].PatientID)
            SeriesDescription = ET.SubElement(Image_Info, 'SeriesDescription')
            SeriesDescription.text = str(PET_tag[0].SeriesDescription)
            SeriesNumber = ET.SubElement(Image_Info, 'SeriesNumber')
            SeriesNumber.text =str(PET_tag[0].SeriesNumber)
            SeriesDate = ET.SubElement(Image_Info, 'SeriesDate')
            SeriesDate.text =str(PET_tag[0].ContentDate)
            SeriesTime = ET.SubElement(Image_Info, 'SeriesTime')
            SeriesTime.text =str(PET_tag[0].SeriesTime)
            SliceThickness = ET.SubElement(Image_Info, 'SliceThickness')
            SliceThickness.text =str(PET_tag[0].SliceThickness)
            Pixel_Spacing = ET.SubElement(Image_Info, 'Pixel_Spacing')
            Pixel_Spacing.text =str(PET_tag[0].PixelSpacing[0])
            CT_Pixel_Spacing = ET.SubElement(Image_Info, 'CT_Pixel_Spacing')
            CT_Pixel_Spacing.text =str(CT_tag[0].PixelSpacing[0])
            for ind, row in enumerate(data):
                Tumor_Area = ET.SubElement(Main, 'Tumor_Area')
                Tumor_Area.set('X', str(row['Click_X']))
                Tumor_Area.set('Y', str(row['Click_Y']))
                Tumor_Area.set('Z', str(row['Click_Z']))
                Tumor_Area.set('Area_size', '7cm')
                Tumor_Area.set('UserName', str(row['username']))
                Tumor_Center = ET.SubElement(Tumor_Area, 'Tumor_Center')
                Tumor_Center.set('C_Type', 'LocalMax')
                Tumor_Center.set('UserName', str(row['username']))
                Tumor_Center.set('memo', str(row['LabelName'][0:5]).replace(' ','_')+'_'+str(row['LabelRecord']).replace(' ','_')+'_'+str(ind))
                Tumor_Center.set('X', str(math.floor(float(row['x']))))
                Tumor_Center.set('Y', str(math.floor(float(row['y']))))
                Tumor_Center.set('Z', str(math.floor(float(row['z']))))
                Tumor_Center.text = str(row['SUV'])
            trees = ET.ElementTree(Main)
            filename = str(PET_tag[0].PatientID)+'_'+str(PET_tag[0].ContentDate)+'_'+str(PET_tag[0].SeriesNumber)+'_SOPT_log.xml'
            trees.write(os.path.join(saveFiledir,filename))

            filename = str(PET_tag[0].PatientID) + '_' + str(PET_tag[0].ContentDate) + '_' + str(
                PET_tag[0].SeriesNumber) + '_CT_Body.mat'
            newCT = CT_view.copy()
            newCT = newCT.transpose(1,2,0)
            CT_mat={'Data':np.float64(newCT)}
            savemat(os.path.join(saveFiledir,filename),CT_mat,do_compression=True)
            filename = str(PET_tag[0].PatientID) + '_' + str(PET_tag[0].ContentDate) + '_' + str(
                PET_tag[0].SeriesNumber) + '_PET_Body.mat'
            newPET=PET.copy()
            newPET = newPET.transpose(1,2,0)
            PET_mat={'Data':np.float64(newPET)}
            savemat(os.path.join(saveFiledir,filename),PET_mat,do_compression=True)
'''
PID去examList尋找 PID DATE ITEM
需要目的地影像的位置，存XML檔
<Main>
  <Image_Info>
    <PatientID>269678</PatientID>
    <SeriesDescription>p7421s0_wb_ctac.img: LOR-RAMLA</SeriesDescription>
    <SeriesNumber>565280</SeriesNumber>
    <SeriesDate>20170922</SeriesDate>
    <SeriesTime>123642.00</SeriesTime>
    <SliceThickness>4</SliceThickness>
    <Pixel_Spacing>4</Pixel_Spacing>
    <CT_Pixel_Spacing>1.171875</CT_Pixel_Spacing>
  </Image_Info>
  <Tumor_Area X="69" Y="71" Z="116" Area_size="7cm" UserName="esumi">
    <Tumor_Center C_Type="LocalMax" UserName="esumi" memo="eee" X="74" Y="76" Z="121">0.724576370501408</Tumor_Center>
  </Tumor_Area>
</Main>


'''
