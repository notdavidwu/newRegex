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
    if not request.user.is_authenticated : 
        return redirect('/')
    de_identification = request.session.get('de_identification')
    diseaseCode = request.session.get('diseaseCode',0)
    ScrollTop = request.session.get('scrollTop',0)
    Filter = request.session.get('filter',0)
    return render(request, 'pool/pool.html',{'de_identification':de_identification,'au':au,'diseaseCode':diseaseCode,'ScrollTop':ScrollTop,'Filter':Filter})

@csrf_exempt
def Disease(request):
    cursor = connections['practiceDB'].cursor()
    query = '''select * from diseasetList order by diseaseID'''
    cursor.execute(query,[])
    diseaseNo = []
    diseaseName = []
    res = cursor.fetchall()
    for i in range(len(res)):
        diseaseNo.append(res[i][0])
        diseaseName.append(res[i][1])
    return JsonResponse({'diseaseNo': diseaseNo,'diseaseName': diseaseName})



@csrf_exempt
def topic(request):
    cursor = connections['practiceDB'].cursor()
    au = request.POST.get('username')
    diseaseNo = request.POST.get('diseaseNo')
    if request.user.is_superuser:
        query = '''SELECT topicNo,topicName FROM [researchTopic] where diseaseID=%s order by topicNo'''
        cursor.execute(query,[diseaseNo])
    else:
        query = '''select distinct b.* from Django.dbo.auth_disease as a
                inner join researchTopic as b on a.disease=b.topicNo
                where username = %s and diseaseID=%s order by topicNo
                '''
        cursor.execute(query,[au,diseaseNo])
    
    topicNo = []
    topicName = []
    res = cursor.fetchall()
    for i in range(len(res)):
        topicNo.append(res[i][0])
        topicName.append(res[i][1])

    return JsonResponse({'topicNo': topicNo,'topicName': topicName})


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
            inner join examStudy as c on b.eventID=c.eventID
            where a.topicNo = {Disease} {f" and c.hospitalID = {int(hospital)}　" if len(hospital)!=0 else '' }
            order by a.chartNo
        """
        cursor.execute(query)

    elif filter=='1':
        query = f"""
        select * from (
            select *,ISNULL(b.annotation_chartNo,0) as 'checked' from(
                select a.* from correlationPatientDisease as a
                inner join allEvents as b on a.chartNo=b.chartNo
                inner join examStudy as c on b.eventID=c.eventID
                where a.topicNo = {Disease}  {f" and c.hospitalID = {int(hospital)}　" if len(hospital)!=0 else '' }
                ) as a 
            left join (
                select distinct chartNo as annotation_chartNo from AIC.dbo.annotation_new where topicNo  = {Disease} and username = '{username}'
            ) as b on a.chartNo=b.annotation_chartNo
        ) as c where checked=0 order by chartNo
        """
        cursor.execute(query)

    elif filter=='2':
        query = '''
        select b.sno,a.chartNo,a.topicNo from AIC.dbo.annotation_new as a
        inner join correlationPatientDisease as b on a.chartNo=b.chartNo
        where a.topicNo=%s and a.username=%s and b.topicNo=%s
        order by b.sno
        '''
        cursor.execute(query,[Disease,username,Disease])
    return cursor
@csrf_exempt
def SubjectPatientList(request):
    topic=request.POST.get('topic')
    filter=request.POST.get('filter')
    username=request.POST.get('username')
    hospital=str(request.POST.get('hospital'))
    request.session['diseaseCode']=topic
    request.session['filter']=filter
    PID_previous_select = str(request.session.get('PID',0))
    cursor = connections['practiceDB'].cursor()
    cursor = SQL(cursor,filter,hospital,topic,username)
    sno=[]
    PatientListID=[]
    res = cursor.fetchall()
    object = ''
    for i in range(len(res)):
        PatientListID.append(str(res[i][1]))
        sno.append(str(res[i][0]))
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
    topicNo=request.POST.get('topic')
    username=request.POST.get('username')
    hospital=str(request.POST.get('hospital'))+'%'
    cursor = connections['practiceDB'].cursor()
    print(topicNo,username)
    query = """
        select count(distinct a.chartNo),'1' AS seq
        from correlationPatientDisease as a 
            inner join allEvents as f on a.chartNo=f.chartNo
            inner join examStudy as g on f.eventID=g.eventID
            where a.topicNo=%s and hospitalID like '0'
        UNION
        select count(chartNo) ,'2' AS seq from (
            select *,ISNULL(annotation_chartNo,0) as checked from (
                select distinct　c.chartNo from(
                    select distinct　b.chartNo from examStudy as a inner join allEvents as b on a.eventID=b.eventID where hospitalID like '0'
                        ) as c inner join correlationPatientDisease as d on c.chartNo=d.chartNo　where d.topicNo=%s
                ) as all_list
                left outer join (
                    select distinct chartNo as annotation_chartNo from AIC.dbo.annotation_new where topicNo=%s and username=%s
                ) as located on all_list.chartNo=located.annotation_chartNo 
            ) as list
        where checked=0
        UNION
        select count(distinct chartNo) ,'3' AS seq from AIC.dbo.annotation_new where topicNo=%s and username=%s
        ORDER BY seq ASC
    """
    cursor.execute(query,[topicNo,topicNo,topicNo,username,topicNo,username])
    res = cursor.fetchall()
    all = res[0][0]
    unlabeled = res[1][0]
    labeled = res[2][0]
    return JsonResponse({'all': all,'unlabeled':unlabeled,'labeled':labeled})

def searchFilePath(chartNo,eventDate,studyID,seriesID):
    cursor = connections['AIC'].cursor()
    searchQuery='''SELECT [filePath] FROM [ExamStudySeries_6] WHERE [chartNo]=%s and [eventDate]=%s and [studyID]=%s and [seriesID]=%s'''
    cursor.execute(searchQuery,[chartNo,eventDate,studyID,seriesID])
    filePath = cursor.fetchall()[0][0]
    return filePath

@csrf_exempt
def PatientList(request):
    chartNo = request.POST.get('PID')
    scrollTop = request.POST.get('scrollTop')
    request.session['PID']=chartNo
    request.session['scrollTop']=scrollTop
    
    query =  '''
    select * from (
    select distinct b.chartNo,e.studyDate,d.typeName,f.procedureName,b.eventID,e.category,e.isReady, e.studyID,g.seriesID,g.seriesDes,g.sliceNo,g.note,ROW_NUMBER() OVER (PARTITION BY e.eventID ORDER BY g.sliceNo DESC) as rank
    from allEvents as b 
    left join eventDefinitions as c on b.eventID=c.eventID
    inner join medTypeSet as d on  b.medType=d.medType
    inner join examStudy as e on b.eventID=e.eventID
    inner join examSeries as g on e.storageID=g.storageID
    left join clinicalProcedures as f on c.procedureID=f.procedureID
    where b.chartNo=%s 
    ) as result where rank=1
    order by studyDate DESC
    '''

    # query2 = '''
    #     select studyID,seriesID,seriesDes from ExamStudySeries_6 where sliceNo in
    #             (select MAX(sliceNo) from (
    #             select eventID,studyID,category,seriesID,seriesDes,sliceNo
    #             from ExamStudySeries_6) as a left outer join allEvents as b on a.eventID=b.eventID 
    #             where b.eventID=%s ) and eventID=%s group by studyID,seriesID,seriesDes
    #     '''
    # queryMRI = '''
    #     select top(1)* from ExamStudySeries_6 where eventID=%s and seriesDes in ('T1WI_CE','T1WI')　order by seriesDes DESC
    # '''

    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[chartNo])
    PID = []
    MedExecTime = []
    Item = []
    phase = []
    Check = []
    StudyID = []
    SeriesID=[]
    StudyDes=[]
    SeriesDes=[]
    viewplane=[]
    res = cursor.fetchall()
    # for j in range(len(res)):
    #     cursor2 = connections['AIC'].cursor()
    #     cursor2.execute(query2, [res[j][4],res[j][4]])
    #     res2 = cursor2.fetchall()
    #     if res2 != []:
    #         StudyID = (res2[0][0])
    #         SeriesID = (res2[0][1])
    #         Study.append(StudyID)
    #         Series.append(SeriesID)
    #         SeriesDes.append(res2[0][2])
    #     else:
    #         Study.append(0)
    #         Series.append(0)
    #         SeriesDes.append(0)

    #     filePath = searchFilePath(res[j][0],res[j][1],StudyID,SeriesID)
    #     if platform.system()!='Windows':
    #         fileDir = os.path.join('/home','user','netapp',filePath)
    #     else:
    #         fileDir= os.path.join('//172.31.6.6/share1/NFS/image_v2',filePath)

    #     fileDir = fileDir.replace('-', '')
    #     fileDir = fileDir.replace(' ', '')

    #     fileExt = "*.h5"

    #     if len(list(pathlib.Path(fileDir).glob(fileExt))) == 0:
    #         Check.append('N')
    #     else:
    #         Check.append('Y')

    for i in range(len(res)):
        PID.append(res[i][0])
        MedExecTime.append(str(res[i][1]))
        Item.append(res[i][2])
        phase.append(res[i][3])
        StudyDes.append(res[i][5])
        if res[i][6]==0:
            Check.append('N')
        else:
            Check.append('Y')
        StudyID.append(res[i][7])
        SeriesID.append(res[i][8])
        SeriesDes.append(res[i][9])
        viewplane.append(res[i][11])
    return JsonResponse({'PID': PID, 'MedExecTime': MedExecTime,'StudyID':StudyID ,'SeriesID':SeriesID,'Item': Item,'StudyDes':StudyDes,'SeriesDes':SeriesDes, 'phase': phase, 'Check': Check,'viewplane':viewplane},
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
    viewplane = request.POST.get('viewplane')
    print(viewplane)
    request.session['PID'] = PID
    request.session['MedExecTime'] = MedExecTime
    request.session['Item'] = Item
    request.session['StudyID'] = StudyID
    request.session['SeriesID'] = SeriesID
    request.session['SeriesDes'] = SeriesDes
    request.session['Disease'] = Disease
    request.session['viewplane'] = viewplane
    return JsonResponse({})
    #return render(request, 'DICOM/DICOM.html', {'PID':PID,'MedExecTime':MedExecTime,'Item':Item})