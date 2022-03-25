from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import pathlib
import os
import platform 
import csv,codecs
def warehousing(request):
    au = request.session.get('au')
    diseaseCode = request.session.get('diseaseCode',0)
    ScrollTop = request.session.get('scrollTop',0)
    Filter = request.session.get('filter',0)
    return render(request, 'warehousing/warehousing.html',{'au':au,'diseaseCode':diseaseCode,'ScrollTop':ScrollTop,'Filter':Filter})

@csrf_exempt
def Disease(request):
    query = '''select * from diseaseGroup'''
    cursor = connections['default'].cursor()
    cursor.execute(query)
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

@csrf_exempt
def SubjectPatientList(request):
    Disease=request.POST.get('Disease')
    filter=request.POST.get('filter')
    username=request.POST.get('username')
    hospital=str(request.POST.get('hospital'))+'%'
    request.session['diseaseCode']=Disease
    request.session['filter']=filter
    PID_previous_select = str(request.session.get('PID',0))
    cursor = connections['default'].cursor()
    if filter=='0':
        query = '''
                select distinct a.chartNo
                from correlationPatientDisease as a 
                    inner join allEvents as f on a.chartNo=f.chartNo
                    inner join ExamStudySeries_5 as g on f.eventID=g.eventID
                    where a.diseaseNo=%s and f.hospital like %s　order by a.chartNo
        '''
        cursor.execute(query,[Disease,hospital])
    elif filter=='1':
        query = '''
        select distinct chartNo from (
            select *,ISNULL(PID,0) as checked from (
			    select distinct　c.chartNo from(
				    select distinct　b.chartNo from ExamStudySeries_5 as a inner join allEvents as b on a.eventID=b.eventID where hospital like %s
				        ) as c inner join correlationPatientDisease as d on c.chartNo=d.chartNo　where d.diseaseNo=%s
                ) as all_list
                left outer join (
                    select distinct PID from Localization where Disease=%s and username=%s
                ) as located on all_list.chartNo=located.PID 
            ) as list
        where checked=0 order by chartNo
        '''
        cursor.execute(query,[hospital,Disease,Disease,username])
    elif filter=='2':
        query = '''
        select distinct chartNo from (
            select *,ISNULL(PID,0) as checked from (
			    select distinct　c.chartNo from(
				    select distinct　b.chartNo from ExamStudySeries_5 as a inner join allEvents as b on a.eventID=b.eventID where hospital like %s
				        ) as c inner join correlationPatientDisease as d on c.chartNo=d.chartNo　where d.diseaseNo=%s
                ) as all_list
                left outer join (
                    select distinct PID from Localization where Disease=%s and username=%s
                ) as located on all_list.chartNo=located.PID 
            ) as list
        where checked<>0 order by chartNo
        '''
        cursor.execute(query,[hospital,Disease,Disease,username])
    
    PatientListID=[]
    res = cursor.fetchall()
    for i in range(len(res)):
        PatientListID.append(str(res[i][0]))
    
    return JsonResponse({'PatientListID': PatientListID,'PID_previous_select':PID_previous_select})

@csrf_exempt
def Patient_num(request):
    Disease=request.POST.get('Disease')
    username=request.POST.get('username')
    hospital=str(request.POST.get('hospital'))+'%'
    cursor = connections['default'].cursor()
    query = '''
            select count(distinct a.chartNo)
            from correlationPatientDisease as a 
                inner join allEvents as f on a.chartNo=f.chartNo
                inner join ExamStudySeries_5 as g on f.eventID=g.eventID
                where a.diseaseNo=%s and hospital like %s
    '''
    cursor.execute(query,[Disease,hospital])
    res = cursor.fetchall()
    all = res
    query = '''
        select count(chartNo) from (
            select *,ISNULL(PID,0) as checked from (
			    select distinct　c.chartNo from(
				    select distinct　b.chartNo from ExamStudySeries_5 as a inner join allEvents as b on a.eventID=b.eventID where hospital like %s
				        ) as c inner join correlationPatientDisease as d on c.chartNo=d.chartNo　where d.diseaseNo=%s
                ) as all_list
                left outer join (
                    select distinct PID from Localization where Disease=%s and username=%s
                ) as located on all_list.chartNo=located.PID 
            ) as list
        where checked=0
    '''
    cursor.execute(query,[hospital,Disease,Disease,username])
    res = cursor.fetchall()
    unlabeled = res
    query = '''
        select count(chartNo) from (
            select *,ISNULL(PID,0) as checked from (
			    select distinct　c.chartNo from(
				    select distinct　b.chartNo from ExamStudySeries_5 as a inner join allEvents as b on a.eventID=b.eventID where hospital like %s
				        ) as c inner join correlationPatientDisease as d on c.chartNo=d.chartNo　where d.diseaseNo=%s
                ) as all_list
                left outer join (
                    select distinct PID from Localization where Disease=%s and username=%s
                ) as located on all_list.chartNo=located.PID 
            ) as list
        where checked<>0
    '''
    cursor.execute(query,[hospital,Disease,Disease,username])
    res = cursor.fetchall()
    labeled = res
    return JsonResponse({'all': all,'unlabeled':unlabeled,'labeled':labeled})


def searchSQL(condition):
    query =  '''
        select chartNo,eventDate,studyID,seriesID,TypeName from(
        select a.chartNo,a.eventDate,a.TypeName,a.eventID,a.studyDes,a.studyID,a.seriesID,a.seriesDes,a.sliceNo from (
            select b.chartNo,b.eventDate,d.TypeName,b.eventID,e.studyDes,studyID,seriesID,seriesDes,sliceNo from allEvents as b 
                    inner join medTypeSet as d on  b.medType=d.MedType
                    inner join ExamStudySeries_5 as e on b.eventID=e.eventID
                    inner join correlationPatientDisease as g on g.chartNo=b.chartNo
                    where g.diseaseNo=%s
        ) as a
        inner join (
            select b.chartNo,b.eventDate,d.TypeName,b.eventID,e.studyDes,studyID,MAX(sliceNo) as 'slice' from allEvents as b 
                    inner join medTypeSet as d on  b.medType=d.MedType
                    inner join ExamStudySeries_5 as e on b.eventID=e.eventID
                    inner join correlationPatientDisease as g on g.chartNo=b.chartNo
                    where g.diseaseNo=%s
                    group by b.chartNo,b.eventDate,d.TypeName,b.eventID,e.studyDes,studyID
        )as b on a.chartNo=b.chartNo and a.eventDate=b.eventDate and a.eventID=b.eventID and a.TypeName=b.TypeName and a.studyDes=b.studyDes
        and a.studyID=b.studyID and a.sliceNo=b.slice
        ) as a
        order by a.chartNo,a.eventDate ASC
    '''

    cursor = connections['default'].cursor()
    cursor.execute(query,[condition,condition])
    PID = []
    MedExecTime = []
    Item = []
    Check = []
    Study = []
    Series=[]
    res = cursor.fetchall()
    for j in range(len(res)):
        if platform.system()!='Windows':
            fileDir = os.path.join('/home','user','netapp','image',str(res[j][0]),str(res[j][1]),str(res[j][2]),str(res[j][3]))
        else:
            fileDir = os.path.join('D:','image',str(res[j][0]),str(res[j][1]),str(res[j][2]),str(res[j][3]))
        
        fileDir = fileDir.replace('-', '')
        fileDir = fileDir.replace(' ', '')
        fileExt = "*.h5"
        if len(list(pathlib.Path(fileDir).glob(fileExt))) == 0:
            Check.append('N')
        else:
            Check.append('Y')

        PID.append(res[j][0])
        MedExecTime.append(res[j][1])
        Study.append(res[j][2])
        Series.append(res[j][3])
        Item.append(res[j][4])
    return PID, MedExecTime,Study ,Series, Item,  Check

@csrf_exempt
def PatientList(request):
    condition = request.POST.get('PID')
    scrollTop = request.POST.get('scrollTop')
    request.session['condition'] = condition
    request.session['PID']=condition
    request.session['scrollTop']=scrollTop
    PID, MedExecTime,Study ,Series, Item,  Check =searchSQL(condition)

    return JsonResponse({'PID': PID, 'MedExecTime': MedExecTime,'StudyID':Study ,'SeriesID':Series,'Item': Item, 'Check': Check},
                        status=200)


@csrf_exempt
def downloadCSV(request):
    condition = request.session.get('condition')
    PID, MedExecTime,Study ,Series, Item,  Check = searchSQL(condition)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type = 'text/csv')
    response.charset = 'utf-8-sig'
    response['Content-Disposition'] = 'attachment; filename=output.csv'
    # Create the CSV writer using the HttpResponse as the "file"
    writer = csv.writer(response)
    writer.writerow(['PID', 'MedExecTime','Item','Study' ,'Series','Check'])
    for (pid, date,study,series,item,check) in zip( PID, MedExecTime,Study ,Series, Item,  Check):
        writer.writerow([pid, date,item,study,series,check])
    return response

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