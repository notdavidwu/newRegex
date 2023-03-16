
from cv2 import resize
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core import serializers
from eventDefinition.models import Patientinfo
from eventDefinition.models import Visitrecord
import numpy as np
import pyodbc
import datetime
import pytz
from django.utils import timezone

def connsql(request):
    server = '172.31.6.22' 
    database = 'miniDB' 
    username = 'newcomer' 
    password = 'test81218' 
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
    cursor = conn.cursor()
    cursor.execute("select * from patientInfo where aicNo < 10021")
    data = cursor.fetchall()
    a = Patientinfo.objects.all()
    #return render(request, 'index.html', { 'Patientinfo':result })


    #---------------------------
    result = {'status' : '0'}
    result['human_record'] = []
    for item in data:
        record = {}
        record['aicNo'] = item.aicNo
        record['birthDay'] = item.birthDay
        record['sex'] = item.sex
        result['human_record'].append(record)
    
    return JsonResponse(result)
@csrf_exempt
def confirm(request):
    au = request.session.get('au')
    de_identification = request.session.get('de_identification')
    eventDefinition_edit = request.session.get('eventDefinition_edit')
    # if not request.user.is_authenticated : 
    #     return redirect('/')
    return render(request, 'eventDefinition/confirm.html',{'au':au,'de_identification':de_identification,'eventDefinition_edit':eventDefinition_edit})

def replaceCapitalAndLowCase(statusfilter):
    statusfilter = re.compile("select", re.IGNORECASE).sub("", statusfilter)
    statusfilter = re.compile("update", re.IGNORECASE).sub("", statusfilter)
    statusfilter = re.compile("drop", re.IGNORECASE).sub("", statusfilter)
    statusfilter = re.compile("delete", re.IGNORECASE).sub("", statusfilter)
    statusfilter = re.compile("inner", re.IGNORECASE).sub("", statusfilter)
    statusfilter = re.compile("outer", re.IGNORECASE).sub("", statusfilter)
    statusfilter = re.compile("left", re.IGNORECASE).sub("", statusfilter)
    statusfilter = re.compile("right", re.IGNORECASE).sub("", statusfilter)
    statusfilter = re.compile("join", re.IGNORECASE).sub("", statusfilter)
    statusfilter = re.compile("union", re.IGNORECASE).sub("", statusfilter)
    statusfilter = re.compile("into", re.IGNORECASE).sub("", statusfilter)
    statusfilter = re.compile("match", re.IGNORECASE).sub("", statusfilter)
    statusfilter = re.compile("create", re.IGNORECASE).sub("", statusfilter)
    statusfilter = re.compile("--", re.IGNORECASE).sub("", statusfilter)
    statusfilter = re.compile("as", re.IGNORECASE).sub("", statusfilter)
    if len(statusfilter)>20:
        statusfilter=''
    return statusfilter
import re
@csrf_exempt
def confirmpat(request):
    if request.method == 'GET':
        
        
        # server = '172.31.6.22' 
        # database = 'miniDB' 
        # username = 'newcomer' 
        # password = 'test81218' 
        # conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        # cursor = conn.cursor()
        # cursor.execute("select * from patientInfo where aicNo < 10021")

        #測試創造物件
        #create成功
        # newman = Patientinfo(aicno = '12345',birthday = '2022-01-10', sex = '1')
        # newman.save()

        # data = cursor.fetchall()

        
        # result = {'status' : '0'}
        # result['human_record'] = []
        # for item in data:
        #     record = {}
        #     record['aicNo'] = item.aicNo
        #     record['birthDay'] = item.birthDay
        #     record['sex'] = item.sex
        #     result['human_record'].append(record)
    # return JsonResponse(result)     
        scrollTop = request.session.get('eventDefinition_scrollTop')
    # filter = request.POST.get('filter')
    # Disease = request.POST.get('Disease')

        

        diagChecked = request.GET.get('diagChecked')
        treatChecked = request.GET.get('treatChecked')
        # allpatient = Patientinfo.objects.all()
        # result = {}
        # result['human_record'] = []
        # for item in allpatient:
        #     record = {}
        #     record['aicNo'] = item.aicno
        #     record['birthDay'] = item.birthday
        #     record['sex'] = item.sex
        #     result['human_record'].append(record)
        if diagChecked == '1':
            result = {}
            #測試queryset
            #human = human.queryset.filter(sex='diaChecked')
            # human = human.objects.filter(sex='diaChecked')
            # result['human_record'] = []
            # for item in human:
            #         record = {}
            #         record['aicNo'] = item.aicno
            #         record['birthDay'] = item.birthday
            #         record['sex'] = item.sex
            #         result['human_record'].append(record)

            

            
            #可以執行
            result['human_record'] = []
            #male = Patientinfo.objects.filter(aicno__gte = '11111')
            male = Patientinfo.objects.filter(sex = '2')
            for item in male:
                record = {}
                record['aicNo'] = item.aicno
                record['birthDay'] = item.birthday
                record['sex'] = item.sex
                result['human_record'].append(record)
        elif treatChecked == '1':
            result = {}
            result['human_record'] = []
            female = Patientinfo.objects.filter(sex = '1')
            for item in female:
                record = {}
                record['aicNo'] = item.aicno
                record['birthDay'] = item.birthday
                record['sex'] = item.sex
                result['human_record'].append(record)
        else:
            allpatient = Patientinfo.objects.all()
            result = {}
            result['human_record'] = []
            for item in allpatient:
                record = {}
                record['aicNo'] = item.aicno
                record['birthDay'] = item.birthday
                record['sex'] = item.sex
                result['human_record'].append(record)

    return JsonResponse({'data': result['human_record'],'scrollTop':scrollTop})
            # record = {}
            # record['aicNo'] = male.aicno
            # record['birthDay'] = male.birthday
            # record['sex'] = male.sex
            # result['human_record'].append(record)

    
    # treatChecked = request.POST.get('treatChecked')
    # fuChecked = request.POST.get('fuChecked')
    # ambiguousChecked = request.POST.get('ambiguousChecked')
    # pdConfirmed = request.POST.get('pdConfirmed')
    # statusfilterValueSum = int(np.sum(np.array([diagChecked,treatChecked,fuChecked,ambiguousChecked,pdConfirmed]).astype(int)))


    # cursor = connections['miniDB'].cursor()

    # query = 'EXEC EventDefinition_getPatient @filter=%s,@diseaseID=%s,@diagChecked=%s,@treatChecked=%s,@fuChecked=%s,@ambiguousChecked=%s,@pdConfirmed=%s,@statusfilterValueSum=%s'
    # cursor.execute(query,[filter,Disease,diagChecked,treatChecked,fuChecked,ambiguousChecked,pdConfirmed,statusfilterValueSum])
    # query = 'EXEC connsql'
    # cursor.execute(query)
    # result = cursor.fetchall()

    
    # chartNo=list(map(lambda row:row[1],result))
    # chartNoString=''
    # if len(chartNo)==0:
    #     chartNoString=''
    # else:
    #     chartNoString = ','.join(map(str, chartNo))
    # eventUnChecked_query = '''
    #     EXEC [EventDefinition_eventUnChecked] @chartNo=%s
    # '''
    # cursor = connections['practiceDB'].cursor()
    # cursor.execute(eventUnChecked_query,[chartNoString])
    # eventUnChecked_num = []
    # res = cursor.fetchall()
    # for row in res:
    #     eventUnChecked_num.append(row[1])

    # i=0
    # examID=''
    # examID = list(cursor.fetchall())

    #上面的data
    # for row in result:

    #     data += f'''
    #     <tr><td>
    #     '''
        # if filter=='0':
        #     examID += f'''
        #         <input type="radio" onclick="getMedtype();GetTime()" data-chartNo="{row[1]}" name="confirmPID" id={row[0]} data-isDone={int(row[4])}>
        #     '''
        #     if row[2] is True:
        #         examID += f'''<label for={row[0]}><p data-checked={row[3]} class="PatientListID exclude">{str(row[1])} ({eventUnChecked_num[i]})</p><p class="ID">{row[0]}</p></label>'''
        #     else:
        #         examID += f'''<label for={row[0]}><p data-checked={row[3]} class="PatientListID ">{str(row[1])} ({eventUnChecked_num[i]})</p><p class="ID">{row[0]}</p></label>'''
        # else:    
        #     examID += f'''
        #         <input type="radio" onclick="getMedtype();GetTime()" data-chartNo="{row[1]}" name="confirmPID" id={row[0]} data-isDone=1>
        #     '''
        #     examID += f'''<label for={row[0]}><p class="PatientListID ">{str(row[1])} ({eventUnChecked_num[i]})</p><p class="ID">{row[0]}</p></label>'''
        # examID += f'''</td></tr>'''    
        # i+=1
        # cursor.close()
    


@csrf_exempt
def Disease(request):
    query = '''select * from diseasetList'''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query)
    DiseaseNo = []
    Disease = []
    res = cursor.fetchall()
    for i in range(len(res)):
        DiseaseNo.append(res[i][0])
        Disease.append(res[i][1])
    return JsonResponse({'DiseaseNo': DiseaseNo,'Disease': Disease})

@csrf_exempt
def updateEventConfirm(request):
    cursor = connections['practiceDB'].cursor()
    eventID=request.POST.get('eventID')
    disable=request.POST.get('disable')
    query='UPDATE allEvents SET eventChecked=%s WHERE eventID=%s'
    cursor.execute(query,[disable,eventID])
    return JsonResponse({}) 
@csrf_exempt
def confirmpat2(request):
    PID=request.POST.get('ID')
    excludeFilter = request.POST.get('excludeFilter')
    scrollTop = request.POST.get('scrollTop')
    medtype= request.POST.getlist('medtype[]')
    if len(medtype)==0:
        medtype=''
    else:
        medtype = ','.join(map(str, medtype))
    request.session['eventDefinition_scrollTop']=scrollTop
    query = '''EXEC EventDefinition_getPatientEvent_2 @chartNo = %s, @filter = %s, @medtype=%s'''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[PID,excludeFilter,medtype])
    objectArray=[]
    MedType=[]
    eventID=[]
    eventCheckedArray=[]
    con = cursor.fetchall()
    for i in range(len(con)):
        MedType.append(con[i][3])
        eventID.append(con[i][6])
        eventChecked = con[i][7]
        eventCheckedArray.append(eventChecked)
        note = con[i][8]
        if eventChecked is None:
            eventChecked=True
        if note is None:
            note=''
        
        object = f'''<tr><td>'''

        object += f'''<input type="radio" onclick="GetReport();getCurrentEventProcedure();" name="timePID" data-extractFactor=0 data-eventCheck={eventChecked} id=timePID{i}>
                    <label for=timePID{i}>'''
        object += f'''
        <div class="pdID">{i}</div>
        <div class="eventID">{con[i][6]}</div>
        <div class="ChartNo">{con[i][0]}</div>
        <div class="OrderNo">{con[i][1]}</div>
        <div class="edate">{con[i][2]}</div>
        <div class="medType">{con[i][3]}</div>
        <div class="type2">{con[i][4]}</div>
        <div class="eventChecked">🔔</div>
        <div class="note"><input type="text" class="form-control eventNote" onchange="updateEventNote()" value="{note}"></div>
        <div class="menu"></div>
        <p class="report2">{con[i][5]}</p>
        ''' 

        object += f'''</label></tr></td>'''
        objectArray.append(object)
    query= '''
	select distinct eventID_F
	from allEvents as a
	inner join medTypeSet as b on a.medType=b.medType
	where a.chartNo=%s  and eventID_F is not null
    '''
    cursor.execute(query,[PID])
    eventID_F=[]
    res = cursor.fetchall()
    for i in range(len(res)):
        eventID_F.append(res[i][0])
    cursor.close()
    return JsonResponse({'eventID':eventID,'MedType':MedType ,'objectArray':objectArray,'eventID_F':eventID_F,'eventCheckedArray':eventCheckedArray})

@csrf_exempt
def getCancerRegistData(request):
    chartNo = request.POST.get('chartNo')
    query = ''' 
            select disease,caSeqNo,c.caregExecDate,d.procedureName
                from PatientDisease as a
                inner join diseasetList as b on a.diseaseID=b.diseaseID
                inner join eventDefinitions as c on a.PD=c.PDID
                inner join clinicalProcedures as d on c.procedureID=d.procedureID
                where chartNo=%s and c.caregExecDate is not NULL order by c.caregExecDate
            '''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[chartNo])
    PD ,chartNo,disease,caSeqNo =[],[],[],[]
    res=cursor.fetchall()
    for row in res:
        PD.append(row[0])
        chartNo.append(row[1])
        disease.append(row[2])
        caSeqNo.append(row[3])
    return JsonResponse({'PD':PD,'chartNo':chartNo,'disease':disease,'caSeqNo':caSeqNo})

@csrf_exempt
def addInducedEvent(request):
    ind=request.POST.getlist('ind[]')
    eventID_list=request.POST.getlist('eventID[]')
    index_list=request.POST.getlist('index[]')
    index_result=[]
    objectList = []
    cursor = connections['practiceDB'].cursor()
    eventID_str=''
    if len(eventID_list)==0:
        eventID_str=''
    else:
        eventID_str = ','.join(map(str, eventID_list))
    query= '''
    EXEC EventDefinition_getInducedEvent2 @eventID_F=%s
    '''
    cursor.execute(query,[eventID_str])
    result = cursor.fetchall()

    
    for i,row in enumerate(result):
        index_collapse = ind[eventID_list.index(str(row[9]))]
        index_result.append(index_list[eventID_list.index(str(row[9]))])
        object=''
        object += f'''<tr><td class="hiddenRow" onclick="showReport()">'''
        object += f'''
        <div  class="accordian-body collapse collapse{index_collapse} " id="collapse{index_collapse}" >'''

        object += f'''
        <div class="pdID">?</div>
        <div class="eventID">{row[7]}</div>
        <div class="ChartNo">{row[0]}</div>
        <div class="OrderNo">{row[1]}</div>
        <div class="edate">{row[2]}</div>
        <div class="medType">{row[3]}</div>
        <div class="type2">{row[4].replace(' ','')}</div>
        ''' 
        if row[3] == 30001 or row[3]==30002:
            object += f'''<p class="report2">{row[5]}</p>'''
        else:
            object += f'''
                <div class="note"><input type="text" class="form-control eventNote" onchange="updateEventNote()" value="{row[8]}"></div>
                <div class="menu"></div>
                <p class="report2">{row[6]}</p>'''
        object += f'''
        <button type="button" class="btn-close close" aria-label="Close" onclick="deleteEvent_F()">
        </div></button></td></tr>
        '''
        objectList.append(object)
    cursor.close()
    return JsonResponse({'objectList':objectList,'index_result':index_result})

@csrf_exempt
def Phase(request):
    query = '''select [procedureID], [procedureName] from [clinicalProcedures] order by procedureID asc '''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query)
    phase=''
    res = cursor.fetchall()
    for i in range(len(res)):
        phase += f"""<option value='{res[i][0]}'>{res[i][1]}</option>"""
    return JsonResponse({'phase': phase})

@csrf_exempt
def deleteDefinition(request):
    sno = request.POST.get('sno')
    query = 'DELETE FROM eventDefinition WHERE sno=%s'
    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query,[sno])

    return JsonResponse({'sno':sno})



@csrf_exempt
def updatePhase(request):
    EDID = 'NULL' if request.POST.get('EDID')=='-1' else request.POST.get('EDID')
    PDID = request.POST.get('PDID')
    eventID = request.POST.get('eventID')
    procedureID = request.POST.get('procedureID')
    originSeqNo = request.POST.get('originSeqNo')
    chartNo = request.POST.get('chartNo')
    username = request.POST.get('username')
    cursor = connections['practiceDB'].cursor()
    if PDID == 'Infinity':
        query = 'select PD from PatientDisease where chartNo = %s and caSeqNo = %s'
        cursor.execute(query,[chartNo,originSeqNo])
        PDID = cursor.fetchall()[0][0]
    if procedureID=='0':
        query = 'DELETE FROM eventDefinitions WHERE EDID=%s'
        cursor.execute(query,[EDID])
        EDID = -1
        PDID = -1
        originSeqNo = 0
    else:
        if EDID == 'NULL': #insert

            if request.user.is_superuser:
                query = 'INSERT eventDefinitions (eventID,PDID,procedureID) OUTPUT INSERTED .EDID VALUES (%s,%s,%s)'
                cursor.execute(query,[eventID,PDID,procedureID])
            else:
                query = 'INSERT eventDefinitions (eventID,PDID,procedureID,username) OUTPUT INSERTED .EDID VALUES (%s,%s,%s,%s)'
                cursor.execute(query,[eventID,PDID,procedureID,username])
            EDID = cursor.fetchall()[0]
        else: #update
            query = 'UPDATE eventDefinitions SET procedureID=%s WHERE EDID=%s'
            cursor.execute(query,[procedureID,EDID])
    updateAllevent_query='''
        declare @eventID int
        set @eventID=%s
        update allEvents set eventChecked=1 where eventID = @eventID
        update allEvents set eventChecked=1 where eventID_F = @eventID
    '''
    cursor.execute(updateAllevent_query,[eventID])
    return JsonResponse({'sno':[EDID],'originSeqNo':[originSeqNo],'PDID':PDID})
@csrf_exempt
def updateInterval(request):
    EDID = 'NULL' if request.POST.get('EDID')=='-1' else request.POST.get('EDID')
    PDID = request.POST.get('PDID')
    chartNo = request.POST.get('chartNo')
    eventID = request.POST.get('eventID')
    procedureID = request.POST.get('procedureID')
    seqNo = request.POST.get('seqNo')
    username = request.POST.get('username')
    cursor = connections['practiceDB'].cursor()
    if seqNo=='0':
        query = 'DELETE FROM eventDefinitions WHERE EDID=%s'
        cursor.execute(query,[EDID])
        EDID = -1
        PDID = -1
        procedureID = 0
    else:
        query = 'select PD from PatientDisease where chartNo = %s and caSeqNo = %s'
        cursor.execute(query,[chartNo,seqNo])
        PDID = cursor.fetchall()[0][0]
        if EDID == 'NULL': #insert
            if request.user.is_superuser:
                query = 'INSERT eventDefinitions (eventID,PDID,procedureID) OUTPUT INSERTED .EDID VALUES (%s,%s,%s)'
                cursor.execute(query,[eventID,PDID,procedureID])
            else:
                query = 'INSERT eventDefinitions (eventID,PDID,procedureID,username) OUTPUT INSERTED .EDID VALUES (%s,%s,%s,%s)'
                cursor.execute(query,[eventID,PDID,procedureID,username])
            EDID = cursor.fetchall()[0]
        else: #update
            query = 'UPDATE eventDefinitions SET PDID=%s WHERE EDID=%s'
            cursor.execute(query,[PDID,EDID])
    updateAllevent_query='''
        declare @eventID int
        set @eventID=%s
        update allEvents set eventChecked=1 where eventID = @eventID
        update allEvents set eventChecked=1 where eventID_F = @eventID
    '''
    cursor.execute(updateAllevent_query,[eventID])
    return JsonResponse({'sno':[EDID],'seqNo':[seqNo],'PDID':PDID,'procedureID':procedureID})

@csrf_exempt
def searchNote(request):
    chartNo = request.POST.get('chartNo')
    IND = request.POST.get('IND')
    eventID = request.POST.get('eventID')
    query = '''
        select D.disease,C.event,E.tagName,A.seqNo from eventDefinition as A
            inner join(
                select * from PatientDisease where chartNo=%s
            ) as B on A.pdID=B.pdID
            inner join eventGroup as C on A.eventNo=C.eventNo
            inner join diseaseGroup as D on B.diseaseNo=D.diseaseNo
            inner join eventTag as E on A.eventTag = E.eventTag and A.eventNo=E.eventNo
            where eventID=%s Order by B.diseaseNo ASC
        '''

    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query,[chartNo,eventID])
    res = cursor.fetchall()
    object=''
    for i in range(len(res)):
        object += f'''<p style="font-weight: bold">{res[i][0].replace('  ','')}: {res[i][1].replace('  ','')}—{res[i][2].replace('  ','')}—{res[i][3]}</p>'''
    return JsonResponse({'IND':IND,'object':object})

@csrf_exempt
def searchPhaseAndInterval(request):
    eventID = request.POST.get('eventID')
    chartNo = request.POST.get('chartNo')
    query = '''
    select * from (
    select b.caSeqNo,c.EDID,c.eventID,c.procedureID
    from diseasetList as a inner join PatientDisease as b on a.diseaseID=b.diseaseID
        inner join eventDefinitions as c on b.PD=c.PDID
        inner join ProcedureEvent as d on c.procedureID=d.procedureID
        inner join medTypeSet as e on d.groupNo=e.groupNo
        left outer join allEvents as f on b.chartNo=f.chartNo and e.medType=f.medType
        left outer join eventDetails as g on f.eventID=g.eventID
    where b.chartNo=%s and f.eventDate is not null  and descriptionType=3 and DATEDIFF(DAY, c.caregExecDate, f.eventDate) between -5 and 5
    ) as res where res.eventID=%s
    '''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[chartNo,eventID])
    res = cursor.fetchall()
    caSeqNo = []
    EDID = []
    procedureID = []
    eventID = []

    if len(res)!=0:
        for row in res:
            caSeqNo.append(row[0])
            EDID.append(row[1])
            eventID.append(row[2])
            procedureID.append(row[3])
    else:
        EDID=[-1]
        eventID=[NULL]
        caSeqNo=[1]
        procedureID=[1]
    

    return JsonResponse({'caSeqNo':caSeqNo,'EDID':EDID,'eventID':eventID,'procedureID':procedureID})

@csrf_exempt
def searchRecord(request):
    IND = request.POST.get('IND')
    chartNo = request.POST.get('chartNo')
    eventID_list = request.POST.getlist('eventID[]')
    username = request.POST.get('username')
    query = 'EXEC [EventDefinition_searchRecord_2] @chartNo=%s, @eventID=%s,@username=%s'
    eventID_str=''
    if len(eventID_list)==0:
        eventID_str=''
    else:
        eventID_str = ','.join(map(str, eventID_list))

    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[chartNo,eventID_str,username])
    res = cursor.fetchall()

    caSeqNo = []
    EDID = []
    PDID = []
    procedureID = []
    eventID = []
    eventID_F = []
    editor = []
    if len(res)!=0:
        Record = len(res)
        for row in res:
            caSeqNo.append(row[0])
            EDID.append(row[1])
            eventID.append(row[2])
            procedureID.append(row[3])
            eventID_F.append(row[4])
            PDID.append(row[5])
            editor.append(row[9])
    else:
        Record = 1
        EDID=[-1]
        eventID=[0]
        caSeqNo=[0]
        procedureID=[0]
        eventID_F=[0]
        PDID = ['-1']
        editor = ['NoRecord']

    return JsonResponse({'IND':IND,'Record':Record,'caSeqNo':caSeqNo,'EDID':EDID,'eventID':eventID,'procedureID':procedureID,'eventID_F':eventID_F,'PDID':PDID,'editor':editor})

@csrf_exempt
def updateCancerRegist(request):
    EDID = request.POST.get('EDID')
    eventID = request.POST.get('eventID')
    query = 'UPDATE eventDefinitions SET eventID=%s WHERE EDID=%s'
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[eventID,EDID])
    updateAllevent_query='''
        declare @eventID int
        set @eventID=%s
        update allEvents set eventChecked=1 where eventID = @eventID
        update allEvents set eventChecked=1 where eventID_F = @eventID
    '''
    cursor.execute(updateAllevent_query,[eventID])
    return JsonResponse({})

@csrf_exempt
def updateInducedEvent(request):
    eventID_F = request.POST.get('eventID_F')
    eventID = request.POST.get('eventID')
    query = 'update allEvents set eventID_F=%s where eventID=%s'
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[eventID_F,eventID])
    updateAllevent_query='''
        declare @eventID int
        set @eventID=%s
        update allEvents set eventChecked=1 where eventID = @eventID
        update allEvents set eventChecked=1 where eventID_F = @eventID
    '''
    cursor.execute(updateAllevent_query,[eventID])
    return JsonResponse({})

@csrf_exempt
def deleteEvent_F(request):
    eventID = request.POST.get('eventID')
    query = 'update allEvents set eventID_F=NULL where eventID=%s'
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[eventID])
    return JsonResponse({})

@csrf_exempt
def getClinicalProcedures(request):
    # query = '''
    #     EXEC eventDefinition_getClinicalProcedures_2
    # '''
    # cursor = connections['miniDB'].cursor()
    # cursor.execute(query,[])
    # result = cursor.fetchall()
    #取得65 up or below
    age = request.GET.get('age')
    #65以上
    if age == '1':
        #現在日期
        now = timezone.now()

        #取得現在年月日
        year = now.year
        month = now.month
        day = now.day

        #計算65年前
        years_65_ago = datetime.datetime((year - 65), month, day, 0, 0, 0, 0, pytz.UTC)

        old = Patientinfo.objects.filter(birthday__range=[years_65_ago,now])
        
        result = []
        for item in old:
            record = {}
            record['aicNo'] = item.aicno
            record['birthDay'] = item.birthday
            record['sex'] = item.sex
            result['human_record'].append(record)
    #65以下
    elif age == '0':
        age= '0'
    selection = ''
    # for row in result:
    #     selection += f'<option data-medtype="{row[0]}" value={row[1]}>{row[2]}</option>'
    return JsonResponse({'result':result['human_record']})

@csrf_exempt
def getNum(request):
    cursor = connections['practiceDB'].cursor()
    disease = request.POST.get('disease')
    diagChecked = request.POST.get('diagChecked')
    treatChecked = request.POST.get('treatChecked')
    fuChecked = request.POST.get('fuChecked')
    ambiguousChecked = request.POST.get('ambiguousChecked')
    pdConfirmed = request.POST.get('pdConfirmed')
    statusfilterValueSum = int(np.sum(np.array([diagChecked,treatChecked,fuChecked,ambiguousChecked,pdConfirmed]).astype(int)))
    cursor = connections['practiceDB'].cursor()
    query = 'EXEC EventDefinition_getPatientNum @diseaseID=%s,@diagChecked=%s,@treatChecked=%s,@fuChecked=%s,@ambiguousChecked=%s,@pdConfirmed=%s,@statusfilterValueSum=%s'
    cursor.execute(query,[disease,diagChecked,treatChecked,fuChecked,ambiguousChecked,pdConfirmed,statusfilterValueSum])
    num=[]
    res = cursor.fetchall()
    for row in res:
        num.append(row[0])
    return JsonResponse({'num':num})


@csrf_exempt
def updatePatientStatus(request):
    scrollTop = request.POST.get('scrollTop')
    request.session['eventDefinition_scrollTop']=scrollTop

    PDSet = request.POST.getlist('PD[]')
    diagCheckedSet = request.POST.getlist('diagChecked[]')
    treatCheckedSet = request.POST.getlist('treatChecked[]')
    fuCheckedSet = request.POST.getlist('fuChecked[]')
    pdConfirmedSet = request.POST.getlist('pdConfirmed[]')
    ambiguousCheckedSet = request.POST.getlist('ambiguousChecked[]')
    ambiguousNoteSet = request.POST.getlist('ambiguousNote[]')
    query = '''UPDATE PatientDisease SET diagChecked = %s,treatChecked=%s,fuChecked=%s,pdConfirmed=%s,ambiguousChecked=%s,ambiguousNote=%s where PD = %s'''
    cursor = connections['practiceDB'].cursor()
    for diagChecked,treatChecked,fuChecked,pdConfirmed,ambiguousChecked,ambiguousNote,PD in zip(diagCheckedSet,treatCheckedSet,fuCheckedSet,pdConfirmedSet,ambiguousCheckedSet,ambiguousNoteSet,PDSet):
        cursor.execute(query,[diagChecked,treatChecked,fuChecked,pdConfirmed,ambiguousChecked,ambiguousNote,PD])
    return JsonResponse({})

@csrf_exempt
def getPatientStatus(request):
    cursor = connections['practiceDB'].cursor()
    chartNo = request.POST.get('chartNo')
    disease = request.POST.get('diseaseId')
    query='''
    select PD, a.diseaseID, caSeqNo, diagChecked, treatChecked, fuChecked, pdConfirmed, ambiguousNote, ambiguousChecked
    from PatientDisease as a 
    inner join diseasetList as b on a.diseaseID=b.diseaseID
    where a.chartNo=%s
    '''
    cursor.execute(query,[chartNo])
    PD,disease,caSeqNo,diagChecked,treatChecked,fuChecked,pdConfirmed,ambiguousNote,ambiguousChecked=[],[],[],[],[],[],[],[],[]
    res = cursor.fetchall()
    for row in res:
        PD.append(row[0])
        disease.append(row[1])
        caSeqNo.append(row[2])
        diagChecked.append(False if row[3] is None else row[3])
        treatChecked.append(False if row[4] is None else row[4])
        fuChecked.append(False if row[5] is None else row[5])
        pdConfirmed.append(False if row[6] is None else row[6])
        ambiguousNote.append('' if row[7] is None else row[7])
        ambiguousChecked.append(False if row[8] is None else row[8])

    return JsonResponse({'PD':PD,'disease':disease,'caSeqNo':caSeqNo,'diagChecked':diagChecked,'treatChecked':treatChecked,'fuChecked':fuChecked,'pdConfirmed':pdConfirmed,'ambiguousNote':ambiguousNote,'ambiguousChecked':ambiguousChecked})

@csrf_exempt
def searchExtractedEventFactorCode(request):
    medType = request.POST.get('medType')
    diseaseId = request.POST.get('diseaseId')
    eventID = request.POST.get('eventID')
    pd = request.POST.get('pd')
    procedureID = request.POST.get('procedureID')
    eventFactorCode=[]
    version=[]
    if procedureID!=0:
        '''---------------取得與medtype相對應的form格式id--------------'''
        cursor = connections['practiceDB'].cursor()
        getEventFactorID='''
        select eventFactorCode,version,count(eventID) as 'isRecorded' from(
            SELECT distinct a.eventFactorCode,a.version,d.eventID
            FROM [practiceDB].[dbo].[eventFactorCode] as a
            inner join medTypeSet as b on a.groupNo=b.groupNo
            left outer join eventFactor as c on a.eventFactorCode=c.eventFactorCode
            left outer join (
            select * from extractedFactors where eventID=%s
            ) as d on c.eventFactorID=d.factorID 
            where medType=%s and diseaseID=%s and a.procedureID=%s 
        ) as result
        group by eventFactorCode,version
        '''
        cursor.execute(getEventFactorID,[eventID,medType,diseaseId,procedureID])
        eventFactorID_result = cursor.fetchall()
        eventFactorCode=[]
        version=[]
        isRecorded = []
        for row in eventFactorID_result:
            eventFactorCode.append(row[0])
            version.append(row[1])
            isRecorded.append(row[2])
    return JsonResponse({'eventFactorCode':eventFactorCode,'version':version,'isRecorded':isRecorded})

@csrf_exempt
def formGenerator(request):
    cursor = connections['practiceDB'].cursor()
    eventID = request.POST.get('eventID')
    eventFactorCode = request.POST.get('eventFactorCode')
    form = request.POST.get('form')

    formObject=''
    dictionary={}
    if len(eventFactorCode)!=0:
        eventFactorID=eventFactorCode
        '''---------------查詢有無紀錄--------------'''
        searchRecord = '''SELECT * FROM [practiceDB].[dbo].[extractedFactors] where eventID=%s'''
        cursor.execute(searchRecord,[eventID])
        recordedOrNot = len(cursor.fetchall())
        '''---------------取得大標題--------------'''
        print(eventFactorID,eventID,recordedOrNot)
        mainSubjectQuery='''
        exec [EventDefinition_mainSubject] @eventFactorCode=%s, @eventID=%s
        '''
        cursor.execute(mainSubjectQuery,[eventFactorID,eventID])

        
        mainSubjectSet = cursor.fetchall()
        formObject = '<div class="formStructure">'
        num=0
        for ind1,mainSubject in enumerate(mainSubjectSet):
            formObject += f'<div data-prepareAdd=0 onmousedown="record()" data-Seq={mainSubject[4]} class="mainBlock mainBlock{mainSubject[5]}" >'
            formObject += f'<b data-eventFactorID={mainSubject[0]} data-itemType={mainSubject[2]} data-labeled={mainSubject[3]}>{mainSubject[1]}</b>'
            if mainSubject[2].replace(' ','')=='text':
                formObject += f'<ul><li><input data-recorded=0 type={mainSubject[2]}></li></ul>'
            structureQuery='''
            select b.*
            from eventFactor as a 
            left outer join eventFactor as b on a.F_eventFactorID=0 and a.eventFactorID=b.F_eventFactorID
            where b.eventFactorID is not null and a.eventFactorID=%s
            '''
            cursor.execute(structureQuery,[mainSubject[0]])
            structureSet = cursor.fetchall()
            
            
            for structure in structureSet:
                formObject += '<ul>'
                num += 1
                type = structure[4].replace(' ','')
                stop = structure[7]
                if type=='text':
                    formObject += f'''
                    <li>
                        <label for="item_{form}_{num}">{structure[3]}：
                        <input type={type} name="formStructure_[1]_[{ind1}][{structure[6]}]" data-recorded=0 data-eventFactorID={structure[0]} id="item_{form}_{num}"></label>
                    </li>
                    '''
                elif type=='date':
                    formObject += f'''<li><input onclick="myFunction()" data-recorded=0 data-checked=0 type={type} data-eventFactorID={structure[0]} name="formStructure_[1]_[{ind1}][{structure[6]}]" id="item_{form}_{num}" value="{structure[3]}"></li>'''  
                elif type=='NE':
                    formObject += f'''<li class="H_{stop}"><label for="item_{form}_{num}">{structure[3]}</label></li>'''
                else:
                    formObject += f'''<li><input onclick="myFunction()" data-recorded=0 data-checked=0 type={type} data-eventFactorID={structure[0]} name="formStructure_[1]_[{ind1}][{structure[6]}]" id="item_{form}_{num}"><label for="item_{form}_{num}">{structure[3]}</label></li>'''

                factorID=structure[0]
                if stop != True:
                    formObject,num = subForm(dictionary,3,ind1,num,factorID,formObject,cursor,form)
                    
                formObject += '</ul>'
            formObject += '</div>'

        formObject += '</div>'
    return JsonResponse({'formObject':formObject})

def subForm(dictionary,depth,ind1,num,factorID,formObject,cursor,form):
    
    step = depth
    query =f'''
    select a{depth}.*
    from eventFactor as a1 
    left outer join eventFactor as a2 on a1.F_eventFactorID=0 and a1.eventFactorID=a2.F_eventFactorID
    '''
    for i in range(3,step+1):
        query +=f'''
            left outer join eventFactor as a{i} on a{i-1}.F_eventFactorID<>0 and a{i-1}.eventFactorID=a{i}.F_eventFactorID
        '''
    query +=f'where a2.eventFactorID is not null and a{i-1}.'
    query +='eventFactorID=%s'
    cursor.execute(query,[factorID])
    result = cursor.fetchall()
    dictionary.update({f"structureSet{depth}":result})
    formObject += '<ul>'
    for structure in dictionary[f"structureSet{depth}"]:
        stop = structure[7]
        num += 1
        type = structure[4].replace(' ','')
        if type=='text':
            formObject += f'''<li class="H_{stop}"><label for="item_{form}_{num}">{structure[3]}：</label><input onclick="myFunction()" data-recorded=0 data-checked=0 type={type} data-eventFactorID={structure[0]} name=formStructure_[1]_[{ind1}][{structure[6]}] id="item_{form}_{num}"></li>'''
        elif type=='NE':
            formObject += f'''<li class="H_{stop}"><label for="item_{form}_{num}">{structure[3]}</label></li>'''
        else:
            formObject += f'''<li class="H_{stop}"><input onclick="myFunction()" data-recorded=0 data-checked=0 type={type} name=formStructure_[1]_[{ind1}][{structure[6]}] data-eventFactorID={structure[0]} id="item_{form}_{num}"><label for="item_{form}_{num}">{structure[3]}</label></li>'''
        factorID=structure[0]
        if stop != True:
            formObject,num = subForm(dictionary,depth+1,ind1,num,factorID,formObject,cursor,form)
    formObject += '</ul>'
    
    return formObject,num

@csrf_exempt
def insertExtractedFactors(request):
    cursor = connections['practiceDB'].cursor()
    eventID = request.POST.get('eventID')
    eventFactorCode = request.POST.get('version')
    procedure = request.POST.get('procedure')
    insertSeq = request.POST.getlist('insertSeq[]')
    insertIDArray = request.POST.getlist('insertIDArray[]')
    insertValArray = request.POST.getlist('insertValArray[]')
    insertRecordedArray = request.POST.getlist('insertRecordedArray[]')

    queryDelete='''DELETE 
    FROM [practiceDB].[dbo].[extractedFactors] where factorID in 
    (select eventFactorID from eventFactor where eventFactorCode=%s)
    and eventID=%s and procedureID=%s'''
    cursor.execute(queryDelete,[eventFactorCode,eventID,procedure])

    query = '''select * from extractedFactors where eventID=%s and factorID=%s and procedureID=%s and seq=%s'''
    for factorID,factorValue,Recorded,seq in zip(insertIDArray,insertValArray,insertRecordedArray,insertSeq):
        cursor.execute(query,[eventID,factorID,procedure,seq])
        if len(cursor.fetchall())==0: # =0, insert this data
            queryInsert='''insert into extractedFactors (eventID,factorID,factorValue,procedureID,seq) VALUES(%s,%s,%s,%s,%s)'''
            cursor.execute(queryInsert,[eventID,factorID,factorValue,procedure,seq])

    return JsonResponse({})

@csrf_exempt
def searchExtractedFactorsRecord(request):
    cursor = connections['practiceDB'].cursor()
    eventID = request.POST.get('eventID')
    procedure = request.POST.get('procedure')
    seqArray = request.POST.getlist('seq[]')
    idArray = request.POST.getlist('idArray[]')
    classArray = request.POST.getlist('classArray[]')

    factorIdString=''
    factorIdString += ",".join(map(str, idArray))
    seqString=''
    seqString += ",".join(map(str, seqArray))

    query='''select factorID,factorValue,seq from extractedFactors where eventID=%s and factorID in (%s) and procedureID=%s and seq in (%s)'''%(eventID,factorIdString,procedure,seqString)

    factorIdRecorded = []
    factorValueRecorded = []
    seqRecorded = []
    classRecorded = []
    cursor.execute(query,[])
    result = cursor.fetchall()
    classArray = np.array(classArray)
    idArray = np.array(idArray)
    for row in result:
        className = classArray[np.where(idArray==str(row[0]))][0]
        seqRecorded.append(row[2])
        classRecorded.append(className)
        factorIdRecorded.append(row[0])
        factorValueRecorded.append(row[1])
    
    return JsonResponse({'seqRecorded':seqRecorded,'classRecorded':classRecorded,'factorIdRecorded':factorIdRecorded,'factorValueRecorded':factorValueRecorded})

@csrf_exempt
def getExtractedFactorsRecordSeq(request):
    eventID = request.POST.get('eventID')
    procedureID = request.POST.get('procedureID')
    eventFactorCode = request.POST.get('eventFactorCode')
    cursor = connections['practiceDB'].cursor()

    query='''
        select distinct seq from [extractedFactors] as a
        inner join eventFactor as b on a.factorID = b.eventFactorID
        where eventID = %s and procedureID = %s and eventFactorCode=%s
    '''
    cursor.execute(query,[eventID,procedureID,eventFactorCode])
    result = cursor.fetchall()
    seq=[]
    for row in result :
        seq.append(row[0])

    return JsonResponse({'seq':seq})

@csrf_exempt
def searchEventFactorCode(request):
    groupNo = request.POST.get('groupNo')
    diseaseID = request.POST.get('diseaseID')
    procedureID = request.POST.get('procedureID')
    version = request.POST.get('version')
    cursor = connections['practiceDB'].cursor()
    query='select eventFactorCode from eventFactorCode where groupNo=%s and diseaseID=%s and procedureID=%s and version=%s'
    maxQuery='select max(eventFactorCode) from eventFactorCode'

    cursor.execute(query,[groupNo,diseaseID,procedureID,version])
    result = cursor.fetchall()
    if len(result)!=0:
        eventFactorCode = result[0][0]
    else:
        cursor.execute(maxQuery,[])
        eventFactorCode = int(cursor.fetchall()[0][0])+1
    return JsonResponse({'eventFactorCode':eventFactorCode})

@csrf_exempt
def getFromStructure(request):
    cursor = connections['practiceDB'].cursor()
    eventFactorCode = request.POST.get('eventFactorCode')
    query='''SELECT *  FROM [practiceDB].[dbo].[eventFactor] where [eventFactorCode]=%s order by eventFactorID'''
    cursor.execute(query,[eventFactorCode])
    eventFactorID,eventFactorCode,serialNo,factorName,itemType,labeled,F_eventFactorID,isLeaf=[],[],[],[],[],[],[],[]
    result = cursor.fetchall()
    for row in result:
        eventFactorID.append(row[0])
        eventFactorCode.append(row[1])
        serialNo.append(row[2])
        factorName.append(row[3])
        itemType.append(row[4])
        labeled.append(row[5])
        F_eventFactorID.append(row[6])
        isLeaf.append(row[7])
    return JsonResponse({'eventFactorID':eventFactorID,'eventFactorCode':eventFactorCode,'serialNo':serialNo,'factorName':factorName,'itemType':itemType,'labeled':labeled,'F_eventFactorID':F_eventFactorID,'isLeaf':isLeaf})

@csrf_exempt
def deleteExtractedFactor(request):
    cursor = connections['practiceDB'].cursor()
    eventFactorCode = request.POST.get('eventFactorCode')
    query = '''
    delete a from extractedFactors as a 
    inner join [eventFactor] as b on a.factorID=b.eventFactorID
    where [eventFactorCode]=%s
    ''' 
    cursor.execute(query,[eventFactorCode])
    return JsonResponse({})
@csrf_exempt
def updateFromStructure(request):
    cursor = connections['practiceDB'].cursor()
    code = request.POST.getlist('code[]')
    eventFactorIDSet = request.POST.getlist('eventFactorID[]')
    eventFactorCode = request.POST.get('eventFactorCode')
    serialNoSet = request.POST.getlist('serialNo[]')
    factorNameSet = request.POST.getlist('factorName[]')
    itemTypeSet = request.POST.getlist('itemType[]')
    labeledSet = request.POST.getlist('labeled[]')
    F_eventFactorIDSet = request.POST.getlist('F_eventFactorID[]')
    isLeafSet = request.POST.getlist('isLeaf[]')

    selectQuery = 'select * from [eventFactorCode] where [eventFactorCode]=%s and [groupNo]=%s and [diseaseID]=%s and [procedureID]=%s and [version]=%s'
    cursor.execute(selectQuery,[code[0],code[1],code[2],code[3],code[4]])
    if len(cursor.fetchall())==0:
        insertQuery='insert into eventFactorCode values(%s,%s,%s,%s,%s)'
        cursor.execute(insertQuery,[code[0],code[1],code[2],code[3],code[4]])
    print(eventFactorCode)
    deleteQuery = 'delete from eventFactor where eventFactorCode=%s'
    cursor.execute(deleteQuery,[eventFactorCode])
    
    for eventFactorID,serialNo,factorName,itemType,labeled,F_eventFactorID,isLeaf in zip(eventFactorIDSet,serialNoSet,factorNameSet,itemTypeSet,labeledSet,F_eventFactorIDSet,isLeafSet):
        insertQuery='insert into eventFactor values(%s,%s,%s,%s,%s,%s,%s,%s)'
        print(eventFactorID,eventFactorCode,serialNo,factorName,itemType,labeled,F_eventFactorID,isLeaf)
        cursor.execute(insertQuery,[eventFactorID,eventFactorCode,serialNo,factorName,itemType,labeled,F_eventFactorID,isLeaf])

    return JsonResponse({})

@csrf_exempt
def getEventFactorCode(request):
    cursor = connections['practiceDB'].cursor()
    queryEventFactorCode='''
    SELECT distinct eventFactorCode
    FROM [practiceDB].[dbo].[eventFactorCode] as a
    inner join clinicalProcedures as b on a.procedureID=b.procedureID
    inner join diseasetList as c on a.diseaseID=c.diseaseID
    order by eventFactorCode
    '''
    queryGroupNo='''
    select * from eventGroup
    '''
    queryDiseaseID='''
    SELECT distinct diseaseID,disease
    FROM   diseasetList
    '''
    queryProcedureID='''
    SELECT distinct procedureID,procedureName
    FROM clinicalProcedures
    '''
    queryVersion='''
    SELECT distinct a.version
    FROM [practiceDB].[dbo].[eventFactorCode] as a
    inner join clinicalProcedures as b on a.procedureID=b.procedureID
    inner join diseasetList as c on a.diseaseID=c.diseaseID
    '''
    result_EventFactorCode = cursor.execute(queryEventFactorCode)
    eventFactorCode,groupNo,groupName,diseaseID,disease,procedureID,procedureName,version = [],[],[],[],[],[],[],[]
    for row in result_EventFactorCode:
        eventFactorCode.append(row[0])
    result_GroupNo = cursor.execute(queryGroupNo)
    for row in result_GroupNo:
        groupNo.append(row[0])
        groupName.append(row[1])
    result_DiseaseID = cursor.execute(queryDiseaseID)
    for row in result_DiseaseID:
        diseaseID.append(row[0])
        disease.append(row[1])
    result_ProcedureID = cursor.execute(queryProcedureID)
    for row in result_ProcedureID:
        procedureID.append(row[0])
        procedureName.append(row[1])
    result_Version = cursor.execute(queryVersion)
    for row in result_Version:
        version.append(row[0])

    return JsonResponse({
        'eventFactorCode':eventFactorCode,
        'groupNo':groupNo,'groupName':groupName,
        'diseaseID':diseaseID,'disease':disease,
        'procedureID':procedureID,'procedureName':procedureName,
        'version':version
        })

@csrf_exempt
def getNewEventFactorID(request):
    cursor = connections['practiceDB'].cursor()
    query = 'SELECT  MAX([eventFactorID])+1 FROM [practiceDB].[dbo].[eventFactor]'
    cursor.execute(query,[])
    newEventFactorID = cursor.fetchall()[0][0]
    return JsonResponse({'newEventFactorID':newEventFactorID})

@csrf_exempt
def getSeqNoOption(request):
    #取病患編號
    paitentnum = request.POST.get('patientNum')

    # #找資料表
    # patient = Visitrecord.objects.filter(aicno=paitentnum)
    # result = []
    # for item in patient:
    #         record = {}
    #         record['visitdate'] = item.visitdate
    #         result['human_record'].append(record)
    # query = '''
    # SELECT * FROM miniDB.dbo.fVisitRecord(patientnum)
    # '''
    # cursor = connections['miniDB'].cursor()
    # cursor.execute(query,[VisitNo])
    # result = cursor.fetchall()
    # seqNo=''
    # for row in result:
    #     seqNo += f'<option value={row[0]}>{row[0]}</option>'
    # return JsonResponse({'seqNo':seqNo})
    server = '172.31.6.22' 
    database = 'miniDB' 
    username = 'newcomer' 
    password = 'test81218' 
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
    cursor = conn.cursor()
    result = cursor.execute("select * from miniDB.dbo.fVisitRecord(98862)")
    patient = cursor.fetchall()
    result = {}
    result['human_record'] = [] 
    
    
    for item in patient:
        record = {}
        record['visitNo'] = item.VisitNo
        result['human_record'].append(record)
    return JsonResponse({'data': result['human_record']})

@csrf_exempt
def addPatientDiease(request):
    chartNo=request.POST.get('chartNo')
    query = 'insert  into [PatientDisease] (chartNo,diseaseID) output inserted.PD values(%s,%s) '
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[chartNo,1])
    PD = cursor.fetchall()[0][0]
    return JsonResponse({'PD':PD})

@csrf_exempt
def deletelePatientDisease(request):
    PDID = request.POST.get('PDID')
    query = 'delete from PatientDisease where PD=%s;delete from eventDefinitions where PDID=%s;'
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[PDID,PDID])
    return JsonResponse({})

@csrf_exempt
def updateDiseaseAndSeq(request):
    PDID = request.POST.get('PDID')
    diseaseID = request.POST.get('diseaseID')
    caSeqNo = request.POST.get('caSeqNo')
    query = 'update [PatientDisease] set diseaseID=%s,caSeqNo=%s where PD=%s'
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[diseaseID,caSeqNo,PDID])
    return JsonResponse({})

@csrf_exempt
def updateEventNote(request):
    eventID = request.POST.get('eventID')
    note = request.POST.get('note')
    query = 'update allEvents set note=%s where eventID=%s'
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[note,eventID])
    return JsonResponse({})


@csrf_exempt
def isDone(request):
    chartNo = request.POST.get('chartNo')
    isDone = request.POST.get('isDone')
    query = 'update PatientDisease set isDone=%s where chartNo=%s'
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[isDone,chartNo])
    return JsonResponse({})


@csrf_exempt
def getTopic(request):
    disease = request.POST.get('disease')
    cursor = connections['practiceDB'].cursor()
    query = 'select * from researchTopic where diseaseID=%s order by topicNo'
    cursor.execute(query,[disease])
    result = cursor.fetchall()
    topic = []
    topicNo = []
    diseaseID = []
    for row in result:
        topicNo.append(row[0])
        topic.append(row[1])
        diseaseID.append(row[2])
    return JsonResponse({'topic':topic,'topicNo':topicNo,'diseaseID':diseaseID})

@csrf_exempt
def getTopicRecord(request):
    chartNo = request.POST.get('chartNo')
    cursor = connections['practiceDB'].cursor()
    query = '''select a.* FROM researchTopic as a 
                inner join correlationPatientDisease as b on a.topicNo=b.topicNo
                where b.chartNo=%s
            '''
    cursor.execute(query,[chartNo])
    result = cursor.fetchall()
    topicNo = []
    for row in result:
        topicNo.append(row[0])
    return JsonResponse({'topicNo':topicNo})
@csrf_exempt
def getTopicPatientNum(request):
    disease = request.POST.get('disease')
    cursor = connections['practiceDB'].cursor()
    query = '''
        EXEC [EventDefinition_getTopicPatientNum] @diseaseID=%s
            '''
    cursor.execute(query,[disease])
    result = cursor.fetchall()
    topic = []
    topicNo = []
    num = []
    for row in result:
        topicNo.append(row[0])
        topic.append(row[1])
        num.append(row[2])
    return JsonResponse({'topic':topic,'topicNo':topicNo,'num':num})

def insertAnnotation(cursor,topicNo,diseaseID,chartNo):
    query_insertAnnotation='''
    insert into annotation(chartNo,studyDate,imageType,date,SUV,x,y,z,labelGroup,labelName,labelRecord,topicNo,fromWhere,studyID,seriesID,doctor_confirm)
    select a.* from(
    select distinct chartNo,studyDate,imageType,GETDATE() as 'date' ,SUV,x,y,z,labelGroup,labelName,'' as 'labelRecord',%s as 'topicNo', NULL as 'fromWhere' ,studyID,seriesID,NULL as 'doctor_confirm' 
    from annotation where topicNo in (select topicNo from researchTopic where diseaseID=%s ) and chartNo=%s
    ) as a
    left outer join(
            select * from annotation where topicNo =%s
    ) as b on a.chartNo=b.chartNo and a.studyDate=b.studyDate and a.SUV=b.SUV and a.x=b.x and a.y=b.y and a.z=b.z and a.studyID=b.studyID and a.seriesID=b.seriesID
    where b.chartNo is null
    '''

    cursor.execute(query_insertAnnotation,[topicNo,diseaseID,chartNo,topicNo])

def insertCorrelationPatientDisease(cursor,topicNo,chartNo):
    query_insertAnnotation='''
    insert into correlationPatientDisease(chartNo,topicNo)
    select a.chartNo,%s as topicNo from (select %s as 'chartNo') as a
    left outer join (
        select * from correlationPatientDisease where topicNo=%s
    ) as b on a.chartNo=b.chartNo
    where b.chartNo is null
    '''
    cursor.execute(query_insertAnnotation,[topicNo,chartNo,topicNo])

def deleteAnnotation(cursor,topicNo,chartNo):
    query = 'delete from annotation where topicNo=%s and chartNo=%s'
    cursor.execute(query,[topicNo,chartNo])

def deleteCorrelationPatientDisease(cursor,topicNo,chartNo):
    query = 'delete from correlationPatientDisease where topicNo = %s and chartNo=%s'
    cursor.execute(query,[topicNo,chartNo])

@csrf_exempt
def processCorrelationPatientListAndAnnotation(request):
    chartNo = request.POST.get('chartNo')
    topicNo_set = request.POST.getlist('topicNo[]')
    diseaseID_set = request.POST.getlist('diseaseID[]')
    annotated_set = request.POST.getlist('annotated[]')
    checked_set = request.POST.getlist('checked[]')
    cursor = connections['practiceDB'].cursor()
    
    for topicNo,diseaseID,annotated,checked in zip(topicNo_set,diseaseID_set,annotated_set,checked_set):
        if int(annotated)==1 and int(checked)==0:
            deleteCorrelationPatientDisease(cursor,topicNo,chartNo)
        elif int(annotated)==0 and int(checked)==1:
            insertCorrelationPatientDisease(cursor,topicNo,chartNo)
    return JsonResponse({})

@csrf_exempt
def addTTP(request):
    eventID = request.POST.get('eventID')
    diseaseID = request.POST.get('diseaseID')
    cursor = connections['practiceDB'].cursor()
    query = '''
        declare @eventID int
        set @eventID=%s

        insert into allEvents(chartNo, orderNo, orderSource, medType, eventDate)
        select chartNo, YEAR(GETDATE())*10000+MONTH(GETDATE())*100+DAY(GETDATE()), 'AIC', 31006, DATEADD(second, 1, eventDate)
        from allEvents
        where eventID=@eventID

        insert into eventDefinitions (PDID, procedureID, eventID)
        select a.PD, 50, SCOPE_IDENTITY()
        from PatientDisease as a inner join allEvents as b on a.chartNo=b.chartNo
        where a.diseaseID=%s and b.eventID=@eventID
    '''
    cursor.execute(query,[eventID,diseaseID])
    return JsonResponse({})

@csrf_exempt
def batchDefinite(request):
    startTherapy = request.POST.get('startTherapy')
    endTherapy = request.POST.get('endTherapy')
    seqNo = request.POST.get('seqNo')
    therapy = request.POST.get('therapy')
    chartNo = request.POST.get('chartNo')
    cursor = connections['practiceDB'].cursor()

    query = 'EXEC %s @seqNo=%s , @pid=%s , @startTherapy=%s , @endTherapy=%s '
    cursor.execute(query,[therapy,seqNo,chartNo,startTherapy,endTherapy])
    return JsonResponse({})

@csrf_exempt
def confirmDone(request):
    eventIDArray = request.POST.getlist('eventIDArray[]')
    query = '''
        declare @eventID int
        set @eventID=%s
        update allEvents set eventChecked=1 where eventID = @eventID
        update allEvents set eventChecked=1 where eventID_F = @eventID
    '''
    cursor = connections['practiceDB'].cursor()
    for eventID in eventIDArray:
        cursor.execute(query,[eventID])
    return JsonResponse({})

@csrf_exempt
def getMedtype(request):
    chartNo = request.POST.get('chartNo')
    query = '''
        select distinct b.medType,b.typeName from allEvents as a
        inner join medTypeSet as b on a.medType=b.medType
        where chartNo=%s and eventSource<2
    '''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[chartNo])
    result = cursor.fetchall()
    medtype = list(map(lambda row:row[0],result))
    typename = list(map(lambda row:row[1].replace(' ',''),result))
    return JsonResponse({'medtype':medtype,'typename':typename})