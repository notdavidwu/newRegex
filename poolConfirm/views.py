from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from itertools import chain

@csrf_exempt
def confirm(request):
    au = request.session.get('au')
    return render(request, 'poolConfirm/confirm.html',{'au':au})


@csrf_exempt
def confirmpat(request):
    Disease = request.POST.get('Disease')
    print(Disease)
    query = '''select distinct chartNo from PatientDisease where diseaseNo = %s order by chartNo asc'''
    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query,[Disease])
    examID=''
    #examID = list(cursor.fetchall())
    for i,row in enumerate(cursor):
        examID += '<tr><td><input type="radio" onclick="GetTime()" name="confirmPID" id='+str(i)+'><label for='+str(i)+'>'+str(row[0])+'</label></td></tr>'
        
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
        where a.chartNo=%s and c.eventTag like %s
        order by a.eventDate desc
    '''
    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query,[PID,'3%'])
    ChartNo=[]
    OrderNo=[]
    ExecDate=[]
    MedType=[]
    TypeName=[]
    ReportText=[]
    eventID=[]
    pdID=[]
    con = cursor.fetchall()
    for i in range(len(con)):
        ChartNo.append(con[i][0])
        OrderNo.append(con[i][1])
        ExecDate.append(con[i][2])
        MedType.append(con[i][3])
        TypeName.append(con[i][4].replace(' ',''))
        if con[i][3] in [30001,30002]:
            ReportText.append(con[i][5])
        else:
            ReportText.append(con[i][6])
        eventID.append(con[i][7])
        pdID.append(con[i][8])
    return JsonResponse({'pdID':pdID,'eventID':eventID,'ChartNo': ChartNo,'OrderNo': OrderNo, 'ExecDate': ExecDate,'MedType':MedType , 'TypeName': TypeName,
                         'ReportText': ReportText})
@csrf_exempt
def Phase(request):

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
    seqNo = request.POST.get('seqNo')
    if eventNo!=str(0):
        if sno=='-1': #insert
            query = 'INSERT eventDefinition (pdID,eventID,eventNo,seqNo) OUTPUT INSERTED .sno VALUES (%s,%s,%s,%s)'
            cursor = connections['dbDesigning'].cursor()
            cursor.execute(query,[pdID,eventID,eventNo,seqNo])
            sno = cursor.fetchall()[0]
        else: #update
            query = 'UPDATE eventDefinition SET eventNo=%s WHERE sno=%s'
            cursor = connections['dbDesigning'].cursor()
            cursor.execute(query,[eventNo,sno])
    else:#請選擇階段，就刪除資料
        query = 'DELETE FROM eventDefinition WHERE sno=%s'
        cursor = connections['dbDesigning'].cursor()
        cursor.execute(query,[sno])

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
    IND = request.POST.get('IND')
    eventID = request.POST.get('eventID')
    query = '''
      select D.disease,C.event,A.seqNo from eventDefinition as A
	inner join(
		select * from PatientDisease where chartNo=(
		select distinct b.chartNo from eventDefinition as a
			inner join PatientDisease as b on a.pdID=b.pdID
			)
	) as B on A.pdID=B.pdID
	inner join eventGroup as C on A.eventNo=C.eventNo
	inner join diseaseGroup as D on B.diseaseNo=D.diseaseNo
    where eventID=%s Order by B.diseaseNo ASC'''

    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query,[eventID])
    res = cursor.fetchall()
    Disease=[]
    Event=[]
    Interval = []
    for i in range(len(res)):
        Disease.append(res[i][0].replace('  ',''))
        Event.append(res[i][1].replace('  ',''))
        Interval.append(res[i][2])
    return JsonResponse({'IND':IND,'Disease':Disease,'Event':Event,'Interval':Interval})

@csrf_exempt
def searchPhaseAndInterval(request):
    sno = request.POST.get('sno')
    query = '''
    select  eventNo,seqNo from eventDefinition 
    where sno=%s
    '''
    cursor = connections['dbDesigning'].cursor()
    cursor.execute(query,[sno])
    res = cursor.fetchall()
    eventNo = []
    seqNo = []
    if len(res)!=0:
        for row in res:
            eventNo.append(row[0])
            seqNo.append(row[1])
    else:
        eventNo=[0]
        seqNo=[1]
    

    return JsonResponse({'eventNo':eventNo,'seqNo':seqNo})

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
    print(sno)

    return JsonResponse({'IND':IND,'Record':Record,'sno':sno})