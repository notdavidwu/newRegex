from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from itertools import chain

@csrf_exempt
def confirm(request):
    au = request.session.get('au')
    de_identification = request.session.get('de_identification')
    return render(request, 'poolConfirm/confirm.html',{'au':au,'de_identification':de_identification})


@csrf_exempt
def confirmpat(request):
    Disease = request.POST.get('Disease')
    query = '''select distinct chartNo from PatientDisease where diseaseNo = %s order by chartNo asc'''
    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query,[Disease])
    examID=''
    #examID = list(cursor.fetchall())
    for i,row in enumerate(cursor):
        examID += f'''
        <tr><td>
        <input type="radio" onclick="GetTime()" name="confirmPID" id={i}>
        <label for={i}><p class="PatientListID">{str(row[0])}</p><p class="ID">{i}</p></label>
        </td></tr>
        '''
        
    return JsonResponse({'examID': examID})

@csrf_exempt
def Disease(request):
    query = '''select * from diseaseGroup'''
    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query)
    DiseaseNo = []
    Disease = []
    res = cursor.fetchall()
    for i in range(len(res)):
        DiseaseNo.append(res[i][0])
        Disease.append(res[i][1])
    return JsonResponse({'DiseaseNo': DiseaseNo,'Disease': Disease})

@csrf_exempt
def confirmpat2(request):
    PID=request.POST.get('ID')
    query = '''
        select a.chartNo,a.orderNo,a.eventDate, a.medType,b.typeName,c.eventTag,c.eventText,a.eventID,d.pdID
        from allEvents as a 
        inner join medTypeSet as b on a.medType=b.medType
		inner join eventDetails as c on a.eventID=c.eventID
        inner join PatientDisease as d on a.chartNo=d.chartNo
        where a.chartNo=%s and c.eventTag like %s and a.eventFID=0 
        order by a.eventDate desc
    '''
    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query,[PID,'3%'])
    objectArray=[]
    MedType=[]
    eventID=[]
    con = cursor.fetchall()
    for i in range(len(con)):
        MedType.append(con[i][3])
        eventID.append(con[i][7])
        object = f'''<tr><td>'''
        if con[i][3] == 30001 or con[i][3]==30002:
            object += f'''<input type="radio" onclick="GetReport()" name="timePID" id=timePID{i} disabled>
                            <label for=timePID{i}>'''
        else:
            object += f'''<input type="radio" onclick="GetReport()" name="timePID" id=timePID{i}>
                            <label for=timePID{i}>'''
        object += f'''
        <div class="pdID"> {con[i][8]} </div>
        <div class="eventID"> {con[i][7]} </div>
        <div class="ChartNo"> {con[i][0]} </div>
        <div class="OrderNo"> {con[i][1]} </div>
        <div class="edate"> {con[i][2]} </div>
        <div class="type2"> {con[i][4].replace(' ','')} </div>
        ''' 
        if con[i][3] == 30001 or con[i][3]==30002:
            object += f'''
                <p class="report2">{con[i][5]}</p>
            '''
        else:
            object += f'''
                <div class="note"></div>
                <div class="menu"></div>
                <p class="report2">{con[i][6]}</p>
            '''
        print(object) 
        objectArray.append(object)
    return JsonResponse({'eventID':eventID,'MedType':MedType ,'objectArray':objectArray})
@csrf_exempt
def Phase(request):
    eventNo=request.POST.get('eventNo')
    query = '''select eventTag, tagName from eventTag where eventNo=%s order by eventTag asc '''
    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query,[eventNo])
    EventID=[]
    Event=[]
    res = cursor.fetchall()
    for i in range(len(res)):
        EventID.append(res[i][0])
        Event.append(res[i][1])

    return JsonResponse({'PhaseID': EventID,'PhaseName': Event})

@csrf_exempt
def deleteDefinition(request):
    sno = request.POST.get('sno')
    query = 'DELETE FROM eventDefinition WHERE sno=%s'
    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query,[sno])

    return JsonResponse({'sno':sno})

@csrf_exempt
def eventGroup(request):
    query = '''select * from eventGroup order by eventNo asc '''
    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query)
    EventID=[]
    Event=[]
    res = cursor.fetchall()
    for i in range(len(res)):
        EventID.append(res[i][0])
        Event.append(res[i][1])
    return JsonResponse({'PhaseID': EventID,'PhaseName': Event})

@csrf_exempt
def ignore(request):
    eventID=request.POST.get('eventID')
    diseaseNo = request.POST.get('diseaseNo')
    query = '''Select Ignore from Ignore WHERE eventID=%s  AND diseaseNo=%s'''
    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query,[eventID,diseaseNo])
    res = cursor.fetchall()
    if len(res)==0:
        Ignore = 1
        query = '''insert into Ignore (eventID,Ignore,diseaseNo) values(%s,%s,%s)'''
        cursor = connections['dbDesigning'].cursor()
        cursor.execute(query,[eventID,Ignore,diseaseNo])
    else:
        Ignore = res[0][0]
        if Ignore == 0:
            Ignore = 1
            query = '''UPDATE Ignore SET Ignore=1 WHERE eventID=%s  AND diseaseNo=%s'''
            cursor = connections['dbDesigning'].cursor()
            cursor.execute(query,[eventID,diseaseNo])
        elif Ignore == 1:
            Ignore = 0
            query = '''UPDATE Ignore SET Ignore=0 WHERE eventID=%s  AND diseaseNo=%s'''
            cursor = connections['dbDesigning'].cursor()
            cursor.execute(query,[eventID,diseaseNo])
    return JsonResponse({'Ignore':Ignore})
@csrf_exempt
def updatePhase(request):
    sno = request.POST.get('sno')
    pdID = request.POST.get('pdID')
    eventID = request.POST.get('eventID')
    eventNo = request.POST.get('eventNo')
    eventTag = request.POST.get('eventTag')
    seqNo = request.POST.get('seqNo')

    if sno=='-1': #insert
        query = 'INSERT eventDefinition (pdID,eventID,eventNo,eventTag,seqNo) OUTPUT INSERTED .sno VALUES (%s,%s,%s,%s,%s)'
        cursor = connections['dbDesigning'].cursor()
        cursor.execute(query,[pdID,eventID,eventNo,eventTag,seqNo])
        sno = cursor.fetchall()[0]
    else: #update
        query = 'UPDATE eventDefinition SET eventNo=%s , eventTag=%s WHERE sno=%s'
        cursor = connections['dbDesigning'].cursor()
        cursor.execute(query,[eventNo,eventTag,sno])


    return JsonResponse({'sno':[sno]})
@csrf_exempt
def updateInterval(request):
    sno = request.POST.get('sno')
    pdID = request.POST.get('pdID')
    eventID = request.POST.get('eventID')
    eventNo = request.POST.get('eventNo')
    seqNo = request.POST.get('seqNo')
    if sno=='-1': #insert
        query = 'INSERT eventDefinition (pdID,eventID,eventNo,seqNo) OUTPUT INSERTED .sno VALUES (%s,%s,%s,%s)'
        cursor = connections['dbDesigning'].cursor()
        cursor.execute(query,[pdID,eventID,eventNo,seqNo])
        sno = cursor.fetchall()[0]
    else: #update
        query = 'UPDATE eventDefinition SET seqNo=%s WHERE sno=%s'
        cursor = connections['dbDesigning'].cursor()
        cursor.execute(query,[seqNo,sno])
    return JsonResponse({'sno':sno})

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
    Disease=[]
    EventGroup=[]
    EventTag=[]
    Interval = []
    for i in range(len(res)):
        Disease.append(res[i][0].replace('  ',''))
        EventGroup.append(res[i][1].replace('  ',''))
        EventTag.append(res[i][2].replace('  ',''))
        Interval.append(res[i][3])
    return JsonResponse({'IND':IND,'Disease':Disease,'EventGroup':EventGroup,'EventTag':EventTag,'Interval':Interval})

@csrf_exempt
def searchPhaseAndInterval(request):
    sno = request.POST.get('sno')
    query = '''
    select  eventNo,eventTag,seqNo from eventDefinition 
    where sno=%s
    '''
    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query,[sno])
    res = cursor.fetchall()
    eventNo = []
    eventTag = []
    seqNo = []
    if len(res)!=0:
        for row in res:
            eventNo.append(row[0])
            eventTag.append(row[1])
            seqNo.append(row[2])
    else:
        eventNo=[0]
        eventTag=[0]
        seqNo=[1]
    

    return JsonResponse({'eventNo':eventNo,'eventTag':eventTag,'seqNo':seqNo})

@csrf_exempt
def searchRecord(request):
    IND = request.POST.get('IND')
    eventID = request.POST.get('eventID')
    query = '''
    select A.sno from eventDefinition as A
        inner join PatientDisease as B on A.pdID=B.pdID 
        inner join diseaseGroup as C on B.diseaseNo=C.diseaseNo
        where eventID=%s
    '''
    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query,[eventID])
    res = cursor.fetchall()
    sno = []
    if len(res)==0:
        Record = 1
        sno = [-1]
    else:
        Record = len(res)
        for row in res:
            sno.append(row[0])

    return JsonResponse({'IND':IND,'Record':Record,'sno':sno})