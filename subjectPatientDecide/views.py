
from unittest import result
from cv2 import resize
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import numpy as np
import csv,codecs

@csrf_exempt
def subjectPatientDecide(request):
    au = request.session.get('au')
    
    # if not request.user.is_authenticated or not request.user.is_superuser:
    #     return redirect('/')
    return render(request, 'subjectPatientDecide/subjectPatientDecide.html',{'au':au})

@csrf_exempt
def getPatient(request):
    query,parameter = patientSQL(request)
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,parameter)
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
def getTopic(request):
    cursor = connections['practiceDB'].cursor()
    query = '''
        select * from diseasetList as a
        inner join researchTopic as b on a.diseaseID=b.diseaseID
        order by a.diseaseID,topicNo
    '''
    cursor.execute(query,[])
    result = cursor.fetchall()
    disease = []
    topicNo = []
    topicName = []
    for row in result:
        disease.append(row[1])
        topicNo.append(row[2])
        topicName.append(row[3])
    disease_unique = np.unique(np.array(disease)).tolist()

    return JsonResponse({'disease_unique':disease_unique,'disease':disease,'topicNo':topicNo,'topicName':topicName})

def patientSQL(request):
    diseaseID = request.POST.getlist('diseaseID[]')
    caSeqNo = request.POST.getlist('caSeqNo[]')
    diagChecked = request.POST.getlist('diagChecked[]')
    treatChecked = request.POST.getlist('treatChecked[]')
    fuChecked = request.POST.getlist('fuChecked[]')
    ambiguousChecked = request.POST.getlist('ambiguousChecked[]')
    pdConfirmed = request.POST.getlist('pdConfirmed[]')
    n_loop = len(diseaseID)
    parameter = []
    sum_filter = []
    query = ''
    for i in range(n_loop):
        total_filter = int(diagChecked[i])+int(treatChecked[i])+int(fuChecked[i])+int(ambiguousChecked[i])+int(pdConfirmed[i])
        sum_filter.append(total_filter)
        if total_filter!=0:
            parameter += list(np.array([diseaseID[i],caSeqNo[i],diagChecked[i],treatChecked[i],fuChecked[i],ambiguousChecked[i],pdConfirmed[i]]))
        else:
            parameter += list(np.array([diseaseID[i],caSeqNo[i]]))
    if sum_filter[0]!=0:
        query += '''
        SELECT DISTINCT A0.* FROM(
            SELECT [chartNo] FROM [practiceDB].[dbo].[PatientDisease] 
            where [diseaseID]=%s and [caSeqNo]=%s and [diagChecked]=%s 
            and [treatChecked]=%s and [fuChecked]=%s and [ambiguousChecked]=%s 
            and [pdConfirmed]=%s
        ) AS A0
        '''
    else:
        query += '''
        SELECT DISTINCT A0.* FROM(
            SELECT [chartNo] FROM [practiceDB].[dbo].[PatientDisease] 
            where [diseaseID]=%s and [caSeqNo]=%s 
        ) AS A0
        '''
    for i in range(1,n_loop):
        if sum_filter[i]!=0:
            query += f'''
                INNER JOIN(
                    SELECT [chartNo] FROM [practiceDB].[dbo].[PatientDisease] 
                    where [diseaseID]=%s and [caSeqNo]=%s and [diagChecked]=%s 
                    and [treatChecked]=%s and [fuChecked]=%s and [ambiguousChecked]=%s 
                    and [pdConfirmed]=%s
                ) AS A{i} ON A0.chartNo=A{i}.chartNo
            '''
        else:
            query += f'''
                INNER JOIN(
                    SELECT [chartNo] FROM [practiceDB].[dbo].[PatientDisease] 
                    where [diseaseID]=%s and [caSeqNo]=%s 
                ) AS A{i} ON A0.chartNo=A{i}.chartNo
            '''

    return query,parameter

@csrf_exempt
def getMedType(request):
    cursor = connections['practiceDB'].cursor()
    query_getEventGroup = 'SELECT * FROM eventGroup ORDER BY groupNo'
    cursor.execute(query_getEventGroup,[])
    groupNo = []
    groupName = []
    for row in cursor.fetchall():
        groupNo.append(row[0])
        groupName.append(row[1])
    query = '''
        SELECT EG.groupNo,RES.medType,MTS.typeName,COUNT(RES.medType) AS '人' FROM(
        SELECT B.medType,B.chartNo FROM(
    '''
    SQL,parameter = patientSQL(request)
    query += SQL

    query +='''
    ) AS A0
        INNER JOIN allEvents AS B ON A0.chartNo=B.chartNo
        GROUP BY B.medType,B.chartNo
    ) AS RES 
    INNER JOIN medTypeSet AS MTS ON RES.medType=MTS.medType
    INNER JOIN eventGroup AS EG ON MTS.groupNo=EG.groupNo
    GROUP BY RES.medType,MTS.typeName,EG.groupNo
    ORDER BY EG.groupNo,RES.medType
    '''
    print(query)
    cursor.execute(query,parameter)
    result = cursor.fetchall()
    medTypeGroupNo = []
    medType = []
    typeName = []
    n_chartNo = []
    for row in result:
        medTypeGroupNo.append(row[0])
        medType.append(row[1])
        typeName.append(row[2])
        n_chartNo.append(row[3])
    return JsonResponse({'groupNo':groupNo,'groupName':groupName,'medTypeGroupNo':medTypeGroupNo,'medType':medType,'typeName':typeName,'n_chartNo':n_chartNo})
@csrf_exempt
def getPatientWithAdvanceCondition(request):
    cursor = connections['practiceDB'].cursor()
    medtype1 = request.POST.getlist('medType1[]')
    medtype2 = request.POST.getlist('medType2[]')
    diffDay = request.POST.getlist('diffDay[]')

    SQL,parameter = patientSQL(request)
    parameterOld=parameter.copy()
    print(parameterOld)
    query='''
    SELECT distinct A.chartNo FROM(
    SELECT * FROM allEvents WHERE chartNo in(
    '''
    query += SQL
    query +='''
        ) AND medType=%s) AS A 
        INNER JOIN(
        SELECT * FROM(
        SELECT * FROM allEvents WHERE chartNo in(
        '''
    query += SQL
    query +=') AND medType=%s) AS B ) AS B ON A.chartNo=B.chartNo and datediff(day, A.eventDate, B.eventDate) between 0 and %s'
    
    parameter += medtype1
    print(parameter)
    print(parameterOld)
    parameterOld += medtype2
    print(parameterOld)
    parameterNew = parameter + parameterOld
    parameterNew += diffDay
    print(parameterNew)
    cursor.execute(query,parameterNew)
    result = cursor.fetchall()
    chartNo = []
    for row in result:
        chartNo.append(row[0])
    print(chartNo)
    return JsonResponse({'chartNo':chartNo})

@csrf_exempt
def getPatientWithMedType(request):
    cursor = connections['practiceDB'].cursor()
    medType = request.POST.getlist('medType[]')
    query = '''
    SELECT chartNo FROM (
        SELECT chartNo,COUNT(medType) AS 'total' FROM(
            SELECT B.chartNo ,B.medType FROM(
    '''
    SQL,parameter = patientSQL(request)
    query += SQL
    query +=') AS A '
    query +='INNER JOIN allEvents AS B ON A.chartNo=B.chartNo WHERE B.medType in ('
    for ind in range(len(medType)):
        if ind == 0:
            query += '%s'
        else:
            query += ',%s'
    query +=')'
    query +=''' 
            GROUP BY B.chartNo ,B.medType
        ) AS Aggr
        GROUP BY chartNo
    ) AS Result
    WHERE total = %s
    ORDER BY chartNo
    '''

    parameter += medType
    parameter += [len(medType)]
    cursor.execute(query,parameter)
    result = cursor.fetchall()
    chartNo = []
    for row in result:
        chartNo.append(row[0])

    return JsonResponse({'chartNo':chartNo})

@csrf_exempt
def getPatientWithProcedure(request):
    cursor = connections['practiceDB'].cursor()
    procedure = request.POST.getlist('procedure[]')
    query = '''
    SELECT chartNo FROM (
    SELECT chartNo,COUNT(procedureID) AS 'total' FROM(
    SELECT B.chartNo ,C.procedureID FROM(
    '''
    SQL,parameter = patientSQL(request)
    query += SQL
    query +=') AS A '
    query +='''
    INNER JOIN allEvents AS B ON A.chartNo=B.chartNo
    INNER JOIN eventDefinitions AS C ON B.eventID=C.eventID
    WHERE C.procedureID in ('''
    for ind in range(len(procedure)):
        if ind == 0:
            query += '%s'
        else:
            query += ',%s'
    query +=')'
    query +=''' 
            GROUP BY B.chartNo ,C.procedureID
        ) AS Aggr
        GROUP BY chartNo
    ) AS Result
    WHERE total = %s
    ORDER BY chartNo
    '''

    parameter += procedure
    parameter += [len(procedure)]
    cursor.execute(query,parameter)
    result = cursor.fetchall()
    chartNo = []
    for row in result:
        chartNo.append(row[0])
    return JsonResponse({'chartNo':chartNo})

@csrf_exempt
def getPatientWithMedTypeAndProcedure(request):
    cursor = connections['practiceDB'].cursor()
    procedure = request.POST.getlist('procedure[]')
    medType = request.POST.getlist('medType[]')
    query = '''
    SELECT chartNo FROM (
    SELECT chartNo,COUNT(medType) AS 'total_medType',COUNT(procedureID) AS 'total_procedureID' FROM(
    SELECT distinct B.chartNo,medType,procedureID FROM(
    '''
    SQL,parameter = patientSQL(request)
    query += SQL
    query +=') AS A '
    query +='''
    INNER JOIN allEvents AS B ON A.chartNo=B.chartNo
    INNER JOIN eventDefinitions AS C ON B.eventID=C.eventID
    WHERE medType in ('''
    for ind in range(len(medType)):
        if ind == 0:
            query += '%s'
        else:
            query += ',%s'
    query +=') and procedureID in ('
    for ind in range(len(procedure)):
        if ind == 0:
            query += '%s'
        else:
            query += ',%s'
    query +=')'
    query +=''' 
    ) AS Aggr
    GROUP BY chartNo
    ) AS Result
    WHERE total_medType=%s and total_procedureID=%s
    '''
    
    
    parameter += medType
    parameter += procedure
    parameter += [len(medType)]
    parameter += [len(procedure)]
    parameter = list(map(int, parameter))

    cursor.execute(query,parameter)
    result = cursor.fetchall()
    chartNo = []
    for row in result:
        chartNo.append(row[0])
    return JsonResponse({'chartNo':chartNo})

@csrf_exempt
def getImageClinicalProcedures(request):
    cursor = connections['practiceDB'].cursor()
    query='''
    SELECT RES.procedureID,CP.procedureName,COUNT(RES.chartNo) AS '人' 
    FROM(
        SELECT C.procedureID,B.chartNo FROM(
    '''
    SQL,parameter = patientSQL(request)
    query += SQL

    query +='''
        ) AS A0
        INNER JOIN allEvents AS B ON A0.chartNo=B.chartNo
        INNER JOIN eventDefinitions AS C ON B.eventID=C.eventID
        GROUP BY C.procedureID,B.chartNo
    ) AS RES
    INNER JOIN clinicalProcedures AS CP ON RES.procedureID = CP.procedureID 
    GROUP BY RES.procedureID,CP.procedureName
    ORDER BY RES.procedureID'''
    cursor.execute(query,parameter)
    result = cursor.fetchall()
    procedureID=[]
    procedureName=[]
    n_chartNo = []
    for row in result:
        procedureID.append(row[0])
        procedureName.append(row[1])
        n_chartNo.append(row[2])
    return JsonResponse({'procedureID':procedureID,'procedureName':procedureName,'n_chartNo':n_chartNo})

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

def insertAnnotation(cursor,topicNo,diseaseID,chartNo):
    query_insertAnnotation='''
    declare @topicNo int ,@diseaseID int ,@chartNo int
    set @topicNo = %s
    set @diseaseID = %s
    set @chartNo = %s
    insert into AIC.dbo.annotation_new(chartNo,studyDate,imageType,updateTime,username,SUV,x,y,z,labelSubject,labelGroup,labelName,labelRecord,topicNo,fromWhere,studyID,seriesID,doctor_confirm)
    select a.* from(
    select distinct chartNo,studyDate,imageType,GETDATE() as 'date' ,username,SUV,x,y,z,labelSubject,labelGroup,labelName,'' as 'labelRecord',@topicNo as 'topicNo', NULL as 'fromWhere' ,studyID,seriesID,NULL as 'doctor_confirm' 
    from AIC.dbo.annotation_new where topicNo in (select topicNo from researchTopic where diseaseID=@diseaseID ) and chartNo=@chartNo
    ) as a
    left outer join(
            select * from AIC.dbo.annotation_new where topicNo =@topicNo
    ) as b on a.chartNo=b.chartNo and a.studyDate=b.studyDate and a.SUV=b.SUV and a.x=b.x and a.y=b.y and a.z=b.z and a.studyID=b.studyID and a.seriesID=b.seriesID
    where b.chartNo is null
    '''
    for pid in chartNo:
        cursor.execute(query_insertAnnotation,[topicNo,diseaseID,pid])

def insertCorrelationPatientDisease(cursor,topicNo,chartNo):
    query_insertAnnotation='''
    declare @topicNo int ,@diseaseID int ,@chartNo int
    set @topicNo = %s
    set @chartNo = %s
    insert into correlationPatientDisease(chartNo,topicNo)
    select a.chartNo,@topicNo as topicNo from (select @chartNo as 'chartNo') as a
    left outer join (
        select * from correlationPatientDisease where topicNo=@topicNo
    ) as b on a.chartNo=b.chartNo
    where b.chartNo is null
    '''
    for pid in chartNo:
        cursor.execute(query_insertAnnotation,[topicNo,pid])
    

@csrf_exempt
def addCorrelationPatientListAndAnnotation(request):
    diseaseID = request.POST.get('diseaseID')
    chartNo = request.POST.getlist('chartNo[]')
    topicName = request.POST.get('topicName')
    cursor = connections['practiceDB'].cursor()
    topicNo = insertTopic(cursor,topicName,diseaseID)
    insertCorrelationPatientDisease(cursor,topicNo,chartNo)
    insertAnnotation(cursor,topicNo,diseaseID,chartNo)
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
    query = 'delete from aic.dbo.annotation_new where topicNo=%s'
    cursor.execute(query,[topicNo])

def deleteCorrelationPatientDisease(cursor,topicNo):
    query = 'delete from correlationPatientDisease where topicNo = %s'
    cursor.execute(query,[topicNo])

from ssh_main import call_api

@csrf_exempt
def downloadCSV(request):
    candicate = request.session.get('candicate')
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type = 'text/csv')
    response.charset = 'utf-8-sig'
    response['Content-Disposition'] = 'attachment; filename=output.csv'
    # Create the CSV writer using the HttpResponse as the "file"
    writer = csv.writer(response)
    writer.writerow(['chartNo'])
    for chartNo in candicate:
        writer.writerow([chartNo])



    return response

@csrf_exempt
def uploadCandicate(request):
    candicate = request.POST.getlist('candicate[]')
    request.session['candicate'] = candicate
    return JsonResponse({})

@csrf_exempt
def fileConversion(request):
    candicate = request.POST.getlist('candicate[]')
    chartNoString = '('
    chartNoString += "),(".join(map(str, candicate))
    chartNoString += ')'
    query = f'''                            --所有事件
            SELECT storageID FROM examStudy AS a 
            INNER JOIN(SELECT chartNo FROM (VALUES {chartNoString}) AS a(chartNo)) AS b ON a.chartNo = b.chartNo 
            WHERE isReady = 0
            '''
    cursor = connections['practiceDB'].cursor()        
    cursor.execute(query,[])
    result = cursor.fetchall()
    storageIDArray = []
    for row in result:
        storageIDArray.append(row[0])

    call_api(storageIDArray)   
    num = len(storageIDArray) 
    return JsonResponse({'num':num})

@csrf_exempt
def getTopicPatient(request):
    topicNo = request.POST.get('topicNo')
    cursor = connections['practiceDB'].cursor()
    query = '''
    select chartNo from correlationPatientDisease where topicNo=%s
    '''
    cursor.execute(query,[topicNo])
    result = cursor.fetchall()
    chartNo = []
    for row in result:
        chartNo.append(row[0])
    return JsonResponse({'chartNo':chartNo})
