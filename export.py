from genericpath import isfile
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

def searchFilePath(chartNo,eventDate,studyID,seriesID):
    cursor = connect.cursor(as_dict=True)
    searchQuery='''
    select filePath from practiceDB.dbo.examStudy as a
    inner join practiceDB.dbo.examSeries as b on a.storageID=b.storageID
    where chartNo=%(chartNo)s and  studyDate=%(eventDate)s and studyID=%(studyID)s and seriesID=%(seriesID)s
    '''
    cursor.execute(searchQuery,{'chartNo': chartNo,'eventDate':eventDate,'studyID':studyID,'seriesID':seriesID})
    filePath = cursor.fetchall()
    return filePath

'''
Connect mssql by using pymssql
Cursor is a key element
Using Cursor and query can control database 
'''
connect = pymssql.connect(
    host='172.31.6.22',
    user='E1306',
    password='izumo203203',
    database='AIC'
)

root=r'\\172.31.6.6\share1\NFS\image'


'''
First, searching PatientID 
'''
list_file_dir = input('請輸入清單位置:')
saveFilePath = list_file_dir
user='export'

list_file_csv = list(pathlib.Path(list_file_dir).glob("*.csv"))
list_file_xlsx = list(pathlib.Path(list_file_dir).glob("*.xlsx"))
if len(list_file_csv)!=0:
    list_data = pd.read_csv(list_file_csv[0])
elif len(list_file_xlsx)!=0:
    list_data = pd.read_excel(list_file_xlsx[0])
print(list_data)
PatientListID = list_data.iloc[:,0].values.tolist()
if list_data.shape[1]>1:
    list_date = list_data.iloc[:,1].tolist()
    list_date = list(map(lambda x:str(x).split(' ')[0],list_date))
    print(list_date)
columns = list_data.columns[0]


if columns=='chartNo':
    topicNo = input('請輸入研究主題編號:')
    tumorType = input('請輸出病灶類型([Primary tumor] or [Lymph node],不指定輸出兩者):')+'%'

if len(topicNo)==0:
    diseaseID = input('請輸入癌症編號:')

chartNo_array,studyDate_array,studyID_array,seriesID_array,SUV_array,x_array,y_array,z_array,tumorType_array,pixelSpacing_array,sliceThickness_array=[],[],[],[],[],[],[],[],[],[],[]



cursor = connect.cursor(as_dict=True)
for i in tqdm(range(len(PatientListID))):
    if columns=='chartNo':
        #取得標記資料
        if len(topicNo)!=0:
            query = '''
            select distinct [chartNo],[studyDate],[x],[y],[z],[labelGroup],[labelName],[studyID],[seriesID] 
            from annotation_new where [chartNo]=%(PatientListID)s and topicNo=%(topicNo)s 
            and labelGroup like %(tumorType)s and studyDate = %(studyDate)s
            '''
            cursor.execute(query, {'PatientListID': PatientListID[i],'studyDate':str(list_date[i]),'topicNo':topicNo,'tumorType':tumorType})
        elif len(diseaseID)!=0:
            query = '''
            select distinct [chartNo],[studyDate],[x],[y],[z],[labelGroup],[labelName],[studyID],[seriesID] 
            from annotation_new as a
            inner join practiceDB.dbo.researchTopic as b on a.topicNo=b.topicNo
            where chartNo=%(PatientListID)s and diseaseID=%(diseaseID)s 
            and labelGroup like %(tumorType)s and studyDate = %(studyDate)s
            '''
            cursor.execute(query, {'PatientListID': PatientListID[i],'studyDate':str(list_date[i]),'diseaseID':diseaseID,'tumorType':tumorType})
        else:
            query = '''
            select distinct [chartNo],[studyDate],[x],[y],[z],[labelGroup],[labelName],[studyID],[seriesID] 
            from annotation_new where [chartNo]=%(PatientListID)s 
            and labelGroup like %(tumorType)s and studyDate = %(studyDate)s
            '''
            cursor.execute(query, {'PatientListID': PatientListID[i],'tumorType':tumorType,'studyDate':str(list_date[i])})
        studyID = []
        for row in cursor:
            studyID.append(row['studyID'])

        if len(studyID)!=0:#代表有標記資料
            if len(topicNo)!=0:
                query = '''
                    select distinct [chartNo],[studyDate],[studyID],[seriesID] 
                    from annotation_new where [chartNo]=%(var1)s and topicNo=%(var2)s and 
                    labelGroup like %(tumorType)s and studyDate = %(studyDate)s
                ''' #取得影像位置資料
                cursor.execute(query, {'var1': PatientListID[i],'var2':topicNo,'tumorType':tumorType,'studyDate':str(list_date[i])})
            elif len(diseaseID)!=0:
                query = '''
                select distinct [chartNo],[studyDate],[x],[y],[z],[labelGroup],[studyID],[seriesID] 
                from annotation_new as a
                inner join practiceDB.dbo.researchTopic as b on a.topicNo=b.topicNo
                where chartNo=%(PatientListID)s and diseaseID=%(diseaseID)s 
                and labelGroup like %(tumorType)s and studyDate = %(studyDate)s
                '''
                cursor.execute(query, {'PatientListID': PatientListID[i],'studyDate':str(list_date[i]),'diseaseID':diseaseID,'tumorType':tumorType})
            else:
                query = '''
                select distinct [chartNo],[studyDate],[x],[y],[z],[labelGroup],[studyID],[seriesID] 
                from annotation_new where [chartNo]=%(PatientListID)s 
                and labelGroup like %(tumorType)s and studyDate = %(studyDate)s
                '''
                cursor.execute(query, {'PatientListID': PatientListID[i],'tumorType':tumorType,'studyDate':str(list_date[i])})
            res = cursor.fetchall()

            for j in range(len(res)):
                chartNo = str(res[j]['chartNo'])
                
                MedExecTime = str(res[j]['studyDate'].replace('-',''))
                studyDate = str(res[j]['studyDate'])
                studyID = str(res[j]['studyID'])
                seriesID = str(res[j]['seriesID'])
                path = searchFilePath(chartNo,MedExecTime,studyID,seriesID)

                fileDir = os.path.join(r'\\172.31.6.6\share1\NFS\image_v2',path[0]['filePath'])
                fileDir = fileDir.replace('-','')
                fileDir = fileDir.replace(' ', '')
                saveFiledir = os.path.join(saveFilePath,'image',chartNo,MedExecTime,studyID,seriesID)
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



                if len(topicNo)!=0:
                    query = '''
                        select distinct
                        [chartNo]
                        ,[studyDate]
                        ,[x]
                        ,[y]
                        ,[z]
                        ,[SUV]
                        ,[labelGroup]
                        ,[labelName]
                        ,[studyID]
                        ,[seriesID] 
                        from annotation_new where [chartNo]=%(var1)s and topicNo=%(var2)s and 
                        labelGroup like %(tumorType)s and studyID=%(studyID)s and seriesID=%(seriesID)s and studyDate = %(studyDate)s
                    ''' #取得影像位置資料
                    cursor.execute(query, {'var1': chartNo,'var2':topicNo,'tumorType':tumorType,'studyID':studyID,'seriesID':seriesID,'studyDate':studyDate})
                elif len(diseaseID)!=0:
                    query = '''
                    select distinct
                    [chartNo]
                    ,[studyDate]
                    ,[x]
                    ,[y]
                    ,[z]
                    ,[SUV]
                    ,[labelGroup]
                    ,[labelName]
                    ,[studyID]
                    ,[seriesID] 
                    from annotation_new as a
                    inner join practiceDB.dbo.researchTopic as b on a.topicNo=b.topicNo
                    where chartNo=%(PatientListID)s and diseaseID=%(diseaseID)s 
                    and labelGroup like %(tumorType)s and studyID=%(studyID)s and seriesID=%(seriesID)s and studyDate = %(studyDate)s
                    '''
                    cursor.execute(query, {'PatientListID': chartNo,'diseaseID':diseaseID,'tumorType':tumorType,'studyID':studyID,'seriesID':seriesID,'studyDate':studyDate})
                else:
                    query = '''
                    select distinct
                    [chartNo]
                    ,[studyDate]
                    ,[x]
                    ,[y]
                    ,[z]
                    ,[SUV]
                    ,[labelGroup]
                    ,[labelName]
                    ,[studyID]
                    ,[seriesID] 
                    from annotation_new where [chartNo]=%(PatientListID)s 
                    and labelGroup like %(tumorType)s and studyID=%(studyID)s and seriesID=%(seriesID)s and studyDate = %(studyDate)s
                    '''
                    cursor.execute(query, {'PatientListID': chartNo,'tumorType':tumorType,'studyID':studyID,'seriesID':seriesID,'studyDate':studyDate})
                
                data = cursor.fetchall()
                PET_ImagePositionPatient_first = list(map(lambda  coordinate:float(coordinate) ,PET_tag[0].ImagePositionPatient))
                PET_ImagePositionPatient_second = list(map(lambda  coordinate:float(coordinate) ,PET_tag[1].ImagePositionPatient))
                SliceThickness = abs(PET_ImagePositionPatient_first[2]-PET_ImagePositionPatient_second[2])
                PET_PixelSpacing = PET_tag[0].PixelSpacing[0]
                CT_PixelSpacing = CT_tag[0].PixelSpacing[0]
                Main = ET.Element('Main')
                Image_Info = ET.SubElement(Main, 'Image_Info')
                PatientID = ET.SubElement(Image_Info, 'PatientID')
                PatientID.text = str(PET_tag[0].PatientID)
                SeriesDescription = ET.SubElement(Image_Info, 'SeriesDescription')
                SeriesDescription.text = str(PET_tag[0].SeriesDescription)
                StudyNumber = ET.SubElement(Image_Info, 'StudyNumber')
                StudyNumber.text =str(studyID)
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
                    x,y,z,SUV,labelName = row['x'],row['y'],row['z'],row['SUV'],row['labelName']
                    Tumor_Area = ET.SubElement(Main, 'Tumor_Area')
                    Tumor_Area.set('X', str(x))
                    Tumor_Area.set('Y', str(y))
                    Tumor_Area.set('Z', str(z))
                    Tumor_Area.set('Area_size', '7cm')
                    Tumor_Area.set('UserName', str(user))
                    Tumor_Center = ET.SubElement(Tumor_Area, 'Tumor_Center')
                    Tumor_Center.set('C_Type', 'LocalMax')
                    Tumor_Center.set('UserName', str(user))
                    Tumor_Center.set('memo', str(labelName[0:5]).replace(' ','_')+'_'+str(ind))
                    Tumor_Center.set('X', str(math.floor(float(row['x']))))
                    Tumor_Center.set('Y', str(math.floor(float(row['y']))))
                    Tumor_Center.set('Z', str(math.floor(float(row['z']))))
                    Tumor_Center.text = str(row['SUV'])

                    chartNo_array.append(chartNo)
                    studyDate_array.append(MedExecTime)
                    studyID_array.append(studyID)
                    seriesID_array.append(seriesID)
                    SUV_array.append(SUV)
                    x_array.append(math.floor(float(x)))
                    y_array.append(math.floor(float(y)))
                    z_array.append(math.floor(float(z)))
                    tumorType_array.append(labelName)
                    pixelSpacing_array.append(PET_PixelSpacing)
                    sliceThickness_array.append(SliceThickness)
                trees = ET.ElementTree(Main)
                filename = f'{chartNo}_{studyDate}_{seriesID}_SOPT_log.xml' 
                trees.write(os.path.join(saveFiledir,filename))

                filename = f'{chartNo}_{studyDate}_{seriesID}_CT_Body.mat'   
                newCT = CT_view.copy()
                newCT = newCT.transpose(1,2,0)
                CT_mat={'Data':np.float64(newCT),'Info':{'pixelSpacing':CT_PixelSpacing,'SliceThickness':SliceThickness}}
                savemat(os.path.join(saveFiledir,filename),CT_mat,do_compression=True)

                filename = f'{chartNo}_{studyDate}_{seriesID}_PET_Body.mat'
                newPET=PET.copy()
                newPET = newPET.transpose(1,2,0)
                PET_mat={'Data':np.float64(newPET),'Info':{'pixelSpacing':PET_PixelSpacing,'SliceThickness':SliceThickness}}
                savemat(os.path.join(saveFiledir,filename),PET_mat,do_compression=True)

    else:
        query = '''select * from annotation_new where id=%(PatientListID)s'''
        cursor.execute(query, {'PatientListID': PatientListID[i]})
        res = cursor.fetchall()
        for row in res:
            chartNo,studyID,seriesID,studyDate,SUV,x,y,z,labelName = row['chartNo'],row['studyID'],row['seriesID'],row['studyDate'],row['SUV'],row['x'],row['y'],row['z'],row['labelName']
            studyDateFormat = studyDate.replace('-','')
            xml_filename = f'{chartNo}_{studyDateFormat}_{studyID}_{seriesID}.xml'
            xml_filepath = os.path.join(saveFilePath,str(chartNo),str(studyDateFormat),str(studyID),str(seriesID),xml_filename)
            saveFiledir = os.path.join(saveFilePath,'image',str(chartNo),str(studyDateFormat),str(studyID),str(seriesID))
            if os.path.isfile(os.path.join(saveFilePath,str(chartNo),str(studyDateFormat),str(studyID),str(seriesID),xml_filename)):
                tree=ET.parse(xml_filepath)
                root=tree.getroot()
                paragraphs = root.findall('Tumor_Area')
                Main = ET.Element('Main')
                Tumor_Area = ET.SubElement(Main, 'Tumor_Area')
                Tumor_Area.set('X', str(x))
                Tumor_Area.set('Y', str(y))
                Tumor_Area.set('Z', str(z))
                Tumor_Area.set('Area_size', '7cm')
                Tumor_Area.set('UserName', str(user))
                Tumor_Center = ET.SubElement(Tumor_Area, 'Tumor_Center')
                Tumor_Center.set('C_Type', 'LocalMax')
                Tumor_Center.set('UserName', str(user))
                Tumor_Center.set('memo', str(labelName[0:5]).replace(' ','_')+'_'+str(len(paragraphs)+1))
                Tumor_Center.set('X', str(math.floor(float(x))))
                Tumor_Center.set('Y', str(math.floor(float(y))))
                Tumor_Center.set('Z', str(math.floor(float(z))))
                Tumor_Center.text = str(SUV)
                trees = ET.ElementTree(Main)
                root.append(Tumor_Area)
                filename = f'{chartNo}_{studyDateFormat}_{seriesID}_SOPT_log.xml' 
                trees.write(os.path.join(saveFiledir,filename))
            else:
                path = searchFilePath(chartNo,studyDate,studyID,seriesID)
                
                fileDir = os.path.join(r'\\172.31.6.6\share1\NFS\image_v2',path[0]['filePath'])
                fileDir = fileDir.replace('-','')
                fileDir = fileDir.replace(' ', '')
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

                PET_ImagePositionPatient_first = list(map(lambda  coordinate:float(coordinate) ,PET_tag[0].ImagePositionPatient))
                PET_ImagePositionPatient_second = list(map(lambda  coordinate:float(coordinate) ,PET_tag[1].ImagePositionPatient))
                SliceThickness = abs(PET_ImagePositionPatient_first[2]-PET_ImagePositionPatient_second[2])

                PET_PixelSpacing = PET_tag[0].PixelSpacing[0]
                CT_PixelSpacing = CT_tag[0].PixelSpacing[0]

                Main = ET.Element('Main')
                Image_Info = ET.SubElement(Main, 'Image_Info')
                PatientID = ET.SubElement(Image_Info, 'PatientID')
                PatientID.text = str(PET_tag[0].PatientID)
                SeriesDescription = ET.SubElement(Image_Info, 'SeriesDescription')
                SeriesDescription.text = str(PET_tag[0].SeriesDescription)
                StudyNumber = ET.SubElement(Image_Info, 'StudyNumber')
                StudyNumber.text =str(studyID)
                SeriesNumber = ET.SubElement(Image_Info, 'SeriesNumber')
                SeriesNumber.text =str(PET_tag[0].SeriesNumber)
                SeriesDate = ET.SubElement(Image_Info, 'SeriesDate')
                SeriesDate.text =str(PET_tag[0].ContentDate)
                SeriesTime = ET.SubElement(Image_Info, 'SeriesTime')
                SeriesTime.text =str(PET_tag[0].SeriesTime)
                SliceThickness = ET.SubElement(Image_Info, 'SliceThickness')
                SliceThickness.text =str(SliceThickness)
                Pixel_Spacing = ET.SubElement(Image_Info, 'Pixel_Spacing')
                Pixel_Spacing.text =str(PET_PixelSpacing)
                CT_Pixel_Spacing = ET.SubElement(Image_Info, 'CT_Pixel_Spacing')
                CT_Pixel_Spacing.text =str(CT_PixelSpacing)

                
                Tumor_Area = ET.SubElement(Main, 'Tumor_Area')
                Tumor_Area.set('X', str(x))
                Tumor_Area.set('Y', str(y))
                Tumor_Area.set('Z', str(z))
                Tumor_Area.set('Area_size', '7cm')
                Tumor_Area.set('UserName', str(user))
                Tumor_Center = ET.SubElement(Tumor_Area, 'Tumor_Center')
                Tumor_Center.set('C_Type', 'LocalMax')
                Tumor_Center.set('UserName', str(user))
                Tumor_Center.set('memo', str(labelName[0:5]).replace(' ','_')+'_'+str(1))
                Tumor_Center.set('X', str(math.floor(float(x))))
                Tumor_Center.set('Y', str(math.floor(float(y))))
                Tumor_Center.set('Z', str(math.floor(float(z))))
                Tumor_Center.text = str(SUV)

                trees = ET.ElementTree(Main)
                filename = f'{chartNo}_{studyDate}_{seriesID}_SOPT_log.xml' 
                trees.write(os.path.join(saveFiledir,filename))

                filename = f'{chartNo}_{studyDate}_{seriesID}_CT_Body.mat'   
                newCT = CT_view.copy()
                newCT = newCT.transpose(1,2,0)
                CT_mat={'Data':np.float64(newCT),'Info':{'pixelSpacing':CT_PixelSpacing,'SliceThickness':SliceThickness}}

                savemat(os.path.join(saveFiledir,filename),CT_mat,do_compression=True)

                filename = f'{chartNo}_{studyDate}_{seriesID}_PET_Body.mat'
                newPET=PET.copy()
                newPET = newPET.transpose(1,2,0)
                PET_mat={'Data':np.float64(newPET),'Info':{'pixelSpacing':PET_PixelSpacing,'SliceThickness':SliceThickness}}
                savemat(os.path.join(saveFiledir,filename),PET_mat,do_compression=True)

                chartNo_array.append(chartNo)
                studyDate_array.append(MedExecTime)
                studyID_array.append(studyID)
                seriesID_array.append(seriesID)
                SUV_array.append(SUV)
                x_array.append(math.floor(float(x)))
                y_array.append(math.floor(float(y)))
                z_array.append(math.floor(float(z)))
                tumorType_array.append(labelName)
                pixelSpacing_array.append(PET_PixelSpacing)
                sliceThickness_array.append(SliceThickness)
final_result=pd.DataFrame(
    np.vstack([chartNo_array,studyDate_array,studyID_array,seriesID_array,SUV_array,x_array,y_array,z_array,tumorType_array,pixelSpacing_array,sliceThickness_array]).T
    ,columns=['chartNo','studyDate','studyID','seriesID','SUV','x','y','z','tumorType','pixelSpacing','sliceThickness']
    )
final_result.to_csv(f'{saveFilePath}\\annotation.csv')