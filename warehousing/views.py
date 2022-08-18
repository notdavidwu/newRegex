from django.shortcuts import render,HttpResponse,redirect
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
def imageList(request):
    startDate = request.POST.get('startDate') + ' 00:00:00.000'
    endDate = request.POST.get('endDate') + ' 23:59:59.000'
    query='''
        declare @startDate datetime,@endDate datetime
        set @startDate=%s
        set @endDate=%s
        select distinct a.chartNo,a.studyDate,a.category,a.studyID,a.storageID,a.eventID 
        from examStudy as a
        left join eventDetails as b on a.eventID=b.eventID
        where studyDate between @startDate and @endDate 
    '''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[startDate,endDate])
    result = cursor.fetchall()
    chartNo,studyDate,category,studyID,seriesID,storageID,eventID,report=[],[],[],[],[],[],[],[]
    for row in result:
        chartNo.append(row[0])
        studyDate.append(row[1])
        category.append(row[2])
        studyID.append(row[3])
        storageID.append(row[4])
        eventID.append(row[5])

    for id in eventID:
        if id !=0:
            report.append('')
        else:
            report.append('')
    return JsonResponse({
        'chartNo': chartNo,
        'studyDate': studyDate,
        'category': category,
        'studyID': studyID,
        'seriesID': seriesID,
        'storageID': storageID,
        'eventID':eventID,
        'report': report
    })
@csrf_exempt
def addPatientList(request):
    chartNo = request.POST.get('chartNo')
    print(chartNo)
    query='''
        insert patientList (chartNo)
        select a.chartNo from (select %s as chartNo) as a
        left join patientList as b  on a.chartNo=b.chartNo
        where b.chartNo is null
    '''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[chartNo])
    return JsonResponse({})

@csrf_exempt
def disease(request):
    query = '''select * from diseasetList'''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    objectArray=''
    for i in range(len(res)):
        objectArray+=f'<option value="{res[i][0]}">{res[i][1]}</option>'
    return JsonResponse({'objectArray': objectArray})

@csrf_exempt
def session(request):
    warehousing_chartNo = request.POST.getlist('chartNo[]')
    warehousing_eventID = request.POST.getlist('eventID[]')
    request.session['warehousing_chartNo'] = warehousing_chartNo
    request.session['warehousing_eventID'] = warehousing_eventID
    return JsonResponse({})

