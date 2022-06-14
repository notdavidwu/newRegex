
from cv2 import resize
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import numpy as np

@csrf_exempt
def subjectPatientDecide(request):
    au = request.session.get('au')
    de_identification = request.session.get('de_identification')
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('/')
    return render(request, 'subjectPatientDecide/subjectPatientDecide.html',{'au':au,'de_identification':de_identification})

@csrf_exempt
def getPatient(request):
    diseaseID = request.POST.get('diseaseID')
    caSeqNo = request.POST.get('caSeqNo')
    diagChecked = request.POST.get('diagChecked')
    treatChecked = request.POST.get('treatChecked')
    fuChecked = request.POST.get('fuChecked')
    ambiguousChecked = request.POST.get('ambiguousChecked')
    pdConfirmed = request.POST.get('pdConfirmed')
    query = '''
    SELECT [chartNo] FROM [practiceDB].[dbo].[PatientDisease] 
    where [diseaseID]=%s and [caSeqNo]=%s and [diagChecked]=%s 
    and [treatChecked]=%s and [fuChecked]=%s and [ambiguousChecked]=%s 
    and [pdConfirmed]=%s
    '''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[diseaseID,caSeqNo,diagChecked,treatChecked,fuChecked,ambiguousChecked,pdConfirmed])
    result = cursor.fetchall()
    chartNo = []
    for row in result:
        chartNo.append(row[0])
    return JsonResponse({'chartNo':chartNo})

@csrf_exempt
def getDisease(request):
    cursor = connections['practiceDB'].cursor()
    query = 'select * from diseasetList'
    cursor.execute(query,[])
    result = cursor.fetchall()
    diseaseID = []
    disease = []
    for row in result:
        diseaseID.append(row[0])
        disease.append(row[1])
    return JsonResponse({'diseaseID':diseaseID,'disease':disease})

@csrf_exempt
def getImageClinicalProcedures(request):
    query='''SELECT distinct c.* FROM [practiceDB].[dbo].[eventGroup] as a 
            inner join ProcedureEvent as b on a.groupNo=b.groupNo
            inner join clinicalProcedures as c on b.procedureID=c.procedureID'''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[])
    result = cursor.fetchall()
    procedureID=[]
    procedureName=[]
    for row in result:
        procedureID.append(row[0])
        procedureName.append(row[1])
    return JsonResponse({'procedureID':procedureID,'procedureName':procedureName})

@csrf_exempt
def getRegistTopicList(request):
    query = 'select * from researchTopic'
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[])
    result = cursor.fetchall()
    topicNo = []
    topicName = []
    for row in result:
        topicNo.append(row[0])
        topicName.append(row[1])
    return JsonResponse({'topicName':topicName})

def insertTopic(cursor,topicName,diseaseID):
    print(topicName,diseaseID)
    query_searchTopicNo = "select topicNo from researchTopic where topicName=%s"
    cursor.execute(query_searchTopicNo,[topicName])
    result = cursor.fetchall()
    if(len(result)==0):
        query_insertTopic = "insert into researchTopic(topicName,diseaseID) output INSERTED.topicNo values(%s,%s)"
        cursor.execute(query_insertTopic,[topicName,diseaseID])
        topicNo = cursor.fetchall()[0][0]
    else:
        topicNo = result[0][0]
    return topicNo

def insertAnnotation(cursor,topicNo,diseaseID,caSeqNo,diagChecked,treatChecked,fuChecked,ambiguousChecked,pdConfirmed):
    query_insertAnnotation='''
    insert into annotation(chartNo,studyDate,imageType,date,SUV,x,y,z,labelGroup,labelName,labelRecord,topicNo,fromWhere,studyID,seriesID,doctor_confirm)
    select a.* from(
        select distinct b.chartNo,b.studyDate,b.imageType,GETDATE() as 'date' ,b.SUV,b.x,b.y,b.z,b.labelGroup,labelName,'' as 'labelRecord',%s as 'topicNo', NULL as 'fromWhere' ,b.studyID,b.seriesID,NULL as 'doctor_confirm'
        from(
            SELECT [chartNo] FROM [practiceDB].[dbo].[PatientDisease] 
            where [diseaseID]=%s and [caSeqNo]=%s and [diagChecked]=%s 
            and [treatChecked]=%s and [fuChecked]=%s and [ambiguousChecked]=%s
            and [pdConfirmed]=%s
        ) as a
        inner join(
            select * from annotation where topicNo in (select topicNo from researchTopic where diseaseID=6)
        ) as b on a.chartNo=b.chartNo
    ) as a
    left outer join(
        select * from annotation where topicNo =%s
    ) as b on a.chartNo=b.chartNo and a.studyDate=b.studyDate and a.SUV=b.SUV and a.x=b.x and a.y=b.y and a.z=b.z and a.studyID=b.studyID and a.seriesID=b.seriesID
    where b.chartNo is null
    '''
    cursor.execute(query_insertAnnotation,[topicNo,diseaseID,caSeqNo,diagChecked,treatChecked,fuChecked,ambiguousChecked,pdConfirmed,topicNo])

def insertCorrelationPatientDisease(cursor,topicNo,diseaseID,caSeqNo,diagChecked,treatChecked,fuChecked,ambiguousChecked,pdConfirmed):
    query_insertAnnotation='''
    insert into correlationPatientDisease(chartNo,diseaseNo)
    select a.chartNo,%s as diseaseNo
    from(
        SELECT [chartNo] FROM [practiceDB].[dbo].[PatientDisease] 
        where [diseaseID]=%s and [caSeqNo]=%s and [diagChecked]=%s 
        and [treatChecked]=%s and [fuChecked]=%s and [ambiguousChecked]=%s
        and [pdConfirmed]=%s
    ) as a 
    left outer join(
        select * from correlationPatientDisease where diseaseNo=%s
    ) as b on a.chartNo=b.chartNo
    where b.sno is null
    '''
    cursor.execute(query_insertAnnotation,[topicNo,diseaseID,caSeqNo,diagChecked,treatChecked,fuChecked,ambiguousChecked,pdConfirmed,topicNo])

@csrf_exempt
def addCorrelationPatientListAndAnnotation(request):
    diseaseID = request.POST.get('diseaseID')
    caSeqNo = request.POST.get('caSeqNo')
    diagChecked = request.POST.get('diagChecked')
    treatChecked = request.POST.get('treatChecked')
    fuChecked = request.POST.get('fuChecked')
    ambiguousChecked = request.POST.get('ambiguousChecked')
    pdConfirmed = request.POST.get('pdConfirmed')
    topicName = request.POST.get('topicName')
    cursor = connections['practiceDB'].cursor()
    topicNo = insertTopic(cursor,topicName,diseaseID)
    insertCorrelationPatientDisease(cursor,topicNo,diseaseID,caSeqNo,diagChecked,treatChecked,fuChecked,ambiguousChecked,pdConfirmed)
    insertAnnotation(cursor,topicNo,diseaseID,caSeqNo,diagChecked,treatChecked,fuChecked,ambiguousChecked,pdConfirmed)
    return JsonResponse({})

@csrf_exempt
def deleteCorrelationPatientListAndAnnotation(request):
    topicName = request.POST.get('topicName')
    cursor = connections['practiceDB'].cursor()
    topicNo = deleteTopic(cursor,topicName)
    deleteCorrelationPatientDisease(cursor,topicNo)
    deleteAnnotation(cursor,topicNo)
    return JsonResponse({})

def deleteTopic(cursor,topicName):
    query = 'delete from researchTopic OUTPUT deleted.topicNo where topicName=%s'
    cursor.execute(query,[topicName])
    topicNo = cursor.fetchall()[0][0]
    return topicNo

def deleteAnnotation(cursor,topicNo):
    query = 'delete from annotation where topicNo=%s'
    cursor.execute(query,[topicNo])

def deleteCorrelationPatientDisease(cursor,topicNo):
    query = 'delete from correlationPatientDisease where diseaseNo = %s'
    cursor.execute(query,[topicNo])