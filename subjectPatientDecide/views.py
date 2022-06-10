
from cv2 import resize
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import numpy as np

@csrf_exempt
def subjectPatientDecide(request):
    au = request.session.get('au')
    de_identification = request.session.get('de_identification')
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


