from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import pathlib
import os
import platform 
import csv,codecs
from matplotlib import pyplot as plt
from base64 import b64encode
from io import BytesIO
import numpy as np
from PIL.Image import fromarray
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


    query='''
        declare @startDate datetime,@endDate datetime
        set @startDate=%s
        set @endDate=%s
        select a.category,count(a.category)
        from examStudy as a
        where studyDate between @startDate and @endDate 
        group by a.category
    '''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[startDate,endDate])
    result = cursor.fetchall()
    categoryList = list(map(lambda row:row[0].replace(' ',''),result))
    imageNumList = list(map(lambda row:int(row[1]),result))
    print(categoryList)
    print(imageNumList)
    ind = np.arange(len(categoryList))
    fig, ax = plt.subplots(figsize=(10, 10))
    color = ['#BDC0BA','#D7B98E','#E87A90','#58B2DC','#90B44B','#A5A051','#91B493','#8F77B5']
    plot = ax.bar(ind, imageNumList, label='image',tick_label=categoryList, color=color,  edgecolor='#BDC0BA')
    ax.axhline(0, color='grey', linewidth=0.8)
    ax.bar_label(plot, label_type='center')

    

    fig.canvas.draw()
    image = np.array(fig.canvas.renderer.buffer_rgba())
    image = to_image(image)
    image = to_data_uri(image)

    return JsonResponse({
        'chartNo': chartNo,
        'studyDate': studyDate,
        'category': category,
        'studyID': studyID,
        'seriesID': seriesID,
        'storageID': storageID,
        'eventID':eventID,
        'report': report,
        'image':image,
    })

def to_image(numpy_img):
    img = fromarray(numpy_img)
    return img

def to_data_uri(pil_img):
    data = BytesIO()
    pil_img.save(data, "png")  # pick your format
    data64 = b64encode(data.getvalue())
    return u'data:img/png;base64,' + data64.decode('UTF-8')

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

