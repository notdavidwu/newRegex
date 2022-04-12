from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import pathlib
import os
import platform 
import numpy as np
import time
from collections import OrderedDict
def pool(request):
    au = request.session.get('au',0)
    if au == 0 : 
        return redirect('/')

    
    de_identification = request.session.get('de_identification')
    print(de_identification)
    diseaseCode = request.session.get('diseaseCode',0)
    ScrollTop = request.session.get('scrollTop',0)
    Filter = request.session.get('filter',0)
    return render(request, 'pool/pool.html',{'de_identification':de_identification,'au':au,'diseaseCode':diseaseCode,'ScrollTop':ScrollTop,'Filter':Filter})

@csrf_exempt
def Disease(request):
    au = '%' if (str(request.POST.get('username')) == 'AIC') else  request.POST.get('username')+'%'
    query = '''select distinct b.* from auth_disease as a
            inner join diseaseGroup as b on a.disease=b.DiseaseNo
            where username like %s 
            '''
    cursor = connections['AIC'].cursor()
    cursor.execute(query,[au])
    DiseaseNo = []
    Disease = []
    res = cursor.fetchall()
    for i in range(len(res)):
        DiseaseNo.append(res[i][0])
        Disease.append(res[i][1])
    return JsonResponse({'DiseaseNo': DiseaseNo,'Disease': Disease})


@csrf_exempt
def getPreviousAction(request):
    diseaseCode = request.session.get('diseaseCode',1)
    ScrollTop = request.session.get('scrollTop',0)
    Filter = request.session.get('filter',0)
    return JsonResponse({'diseaseCode':diseaseCode,'ScrollTop':ScrollTop,'Filter':Filter})

def SQL(cursor,filter,hospital,Disease,username):
    if filter=='0':
        query = f"""
            select * from correlationPatientDisease as a
            inner join allEvents as b on a.chartNo=b.chartNo
            inner join ExamStudySeries_5 as c on b.eventID=c.eventID
            where a.diseaseNo = {Disease} 
        """
        if len(hospital)!=0:
            query += f"""and b.hospital = {hospital}　"""
        
        query += f"""order by a.chartNo"""
        cursor.execute(query)
    elif filter=='1':
        query = f"""
        select * from (
            select *,ISNULL(PID,0) as 'checked' from(
                select a.* from correlationPatientDisease as a
                inner join allEvents as b on a.chartNo=b.chartNo
                inner join ExamStudySeries_5 as c on b.eventID=c.eventID
                where a.diseaseNo = {Disease} """
        if(len(hospital))!=0:
            query += f"""and b.hospital=1"""
        query += f"""
            ) as a 
            left join (
                select distinct PID from annotation where Disease  = {Disease} and username = '{username}'
            ) as b on a.chartNo=b.PID
        ) as c where checked=0 order by chartNo
        """
        cursor.execute(query)
    elif filter=='2':
        query = '''
        select a.PID,a.Disease,b.sno from annotation as a
        inner join correlationPatientDisease as b on a.PID=b.chartNo
        where a.Disease=%s and a.username=%s and b.diseaseNo=%s
        order by b.sno
        '''
        cursor.execute(query,[Disease,username,Disease])
    return cursor
@csrf_exempt
def SubjectPatientList(request):
    Disease=request.POST.get('Disease')
    filter=request.POST.get('filter')
    username=request.POST.get('username')
    hospital=str(request.POST.get('hospital'))
    request.session['diseaseCode']=Disease
    request.session['filter']=filter
    PID_previous_select = str(request.session.get('PID',0))
    cursor = connections['AIC'].cursor()
    cursor = SQL(cursor,filter,hospital,Disease,username)
    sno=[]
    PatientListID=[]
    res = cursor.fetchall()
    object = ''
    for i in range(len(res)):
        PatientListID.append(str(res[i][0]))
        sno.append(str(res[i][2]))
    PatientListID=list(OrderedDict.fromkeys(PatientListID))    
    sno=list(OrderedDict.fromkeys(sno)) 
    for i in range(len(PatientListID)):
        object += f"""
            <tr><td>
                <input type="radio" onclick="TimeReport()" name="Patient" id="Patient{i}">
                <label for="Patient{i}">
                    <p class="ID">{str(sno[i])}</p>
                    <p class="PatientListID">{str(PatientListID[i])}</p>
                </label>
            </td></tr>
        """
    return JsonResponse({'PatientListID': PatientListID,'object':object,'PID_previous_select':PID_previous_select})

@csrf_exempt
def Patient_num(request):
    Disease=request.POST.get('Disease')
    username=request.POST.get('username')
    hospital=str(request.POST.get('hospital'))+'%'
    cursor = connections['AIC'].cursor()
    query = f"""
        select count(distinct a.chartNo),'1' AS seq
        from correlationPatientDisease as a 
            inner join allEvents as f on a.chartNo=f.chartNo
            inner join ExamStudySeries_5 as g on f.eventID=g.eventID
            where a.diseaseNo={Disease} and hospital like '{hospital}'
        UNION
        select count(chartNo) ,'2' AS seq from (
            select *,ISNULL(PID,0) as checked from (
			    select distinct　c.chartNo from(
				    select distinct　b.chartNo from ExamStudySeries_5 as a inner join allEvents as b on a.eventID=b.eventID where hospital like '{hospital}'
				        ) as c inner join correlationPatientDisease as d on c.chartNo=d.chartNo　where d.diseaseNo={Disease}
                ) as all_list
                left outer join (
                    select distinct PID from annotation where Disease={Disease} and username='{username}'
                ) as located on all_list.chartNo=located.PID 
            ) as list
        where checked=0
        UNION
        select count(distinct PID) ,'3' AS seq from annotation where Disease={Disease} and username='{username}'
        ORDER BY seq ASC
    """
    cursor.execute(query)
    res = cursor.fetchall()
    all = res[0][0]
    unlabeled = res[1][0]
    labeled = res[2][0]
    return JsonResponse({'all': all,'unlabeled':unlabeled,'labeled':labeled})



@csrf_exempt
def PatientList(request):
    condition = request.POST.get('PID')
    scrollTop = request.POST.get('scrollTop')
    request.session['PID']=condition
    request.session['scrollTop']=scrollTop
    
    query =  '''
  select b.chartNo,b.eventDate,d.TypeName,f.Enent,b.eventID,e.studyDes from allEvents as b 
		left join EventDefinition as c on b.eventID=c.eventID
		inner join medTypeSet as d on  b.medType=d.MedType
        inner join ExamStudySeries_5 as e on b.eventID=e.eventID
		left join ClinicalEvents as f on c.EventID=f.EventID
        where b.chartNo=%s
        group by b.chartNo,b.eventDate,d.TypeName,f.Enent,b.eventID,e.studyDes
		order by b.eventDate DESC
    '''

    query2 = '''
        select studyID,seriesID,seriesDes from ExamStudySeries_5 where sliceNo in
                (select MAX(sliceNo) from (
                select eventID,orderNo,studyID,studyDes,seriesID,seriesDes,sliceNo
                from ExamStudySeries_5) as a left outer join allEvents as b on a.eventID=b.eventID 
                where b.eventID=%s ) and eventID=%s group by studyID,seriesID,seriesDes
        '''
    queryMRI = '''
        select top(1)* from ExamStudySeries_5 where eventID=%s and seriesDes in ('T1WI_CE','T1WI')　order by seriesDes DESC
    '''

    cursor = connections['AIC'].cursor()
    cursor.execute(query,[condition])
    PID = []
    MedExecTime = []
    Item = []
    phase = []
    Check = []
    Study = []
    Series=[]
    StudyDes=[]
    SeriesDes=[]
    res = cursor.fetchall()
    for j in range(len(res)):
        cursor2 = connections['AIC'].cursor()
        cursor2.execute(query2, [res[j][4],res[j][4]])
        res2 = cursor2.fetchall()
        if res2 != []:
            StudyID = (res2[0][0])
            SeriesID = (res2[0][1])
            Study.append(StudyID)
            Series.append(SeriesID)
            SeriesDes.append(res2[0][2])
        else:
            Study.append(0)
            Series.append(0)
            SeriesDes.append(0)
        if platform.system()!='Windows':
            fileDir = os.path.join('/home','user','netapp','image',str(res[j][0]),str(res[j][1]),str(StudyID),str(SeriesID))
        else:
            fileDir = os.path.join('D:','image',str(res[j][0]),str(res[j][1]),str(StudyID),str(SeriesID))
        
        fileDir = fileDir.replace('-', '')
        fileDir = fileDir.replace(' ', '')

        fileExt = "*.h5"

        if len(list(pathlib.Path(fileDir).glob(fileExt))) == 0:
            Check.append('N')
        else:
            Check.append('Y')

    for i in range(len(res)):
        PID.append(res[i][0])
        MedExecTime.append(res[i][1])
        Item.append(res[i][2])
        phase.append(res[i][3])
        StudyDes.append(res[i][5])
    
    return JsonResponse({'PID': PID, 'MedExecTime': MedExecTime,'StudyID':Study ,'SeriesID':Series,'Item': Item,'StudyDes':StudyDes,'SeriesDes':SeriesDes, 'phase': phase, 'Check': Check},
                        status=200)

from cryptography.fernet import Fernet
@csrf_exempt
def Session(request):
    PID = request.POST.get('PID')
    MedExecTime = request.POST.get('MedExecTime')
    Item = request.POST.get('Item')
    StudyID = request.POST.get('StudyID')
    SeriesID = request.POST.get('SeriesID')
    SeriesDes = request.POST.get('SeriesDes')
    Disease = request.POST.get('Disease')
    request.session['PID'] = PID
    request.session['MedExecTime'] = MedExecTime
    request.session['Item'] = Item
    request.session['StudyID'] = StudyID
    request.session['SeriesID'] = SeriesID
    request.session['SeriesDes'] = SeriesDes
    request.session['Disease'] = Disease
    return JsonResponse({})
    #print(PID)
    #return render(request, 'DICOM/DICOM.html', {'PID':PID,'MedExecTime':MedExecTime,'Item':Item})