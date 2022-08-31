from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from itertools import chain

@csrf_exempt
def confirm(request):
    au = request.session.get('au')
    return render(request, 'confirm/confirm.html',{'au':au})


@csrf_exempt
def confirmpat(request):
    Disease = request.POST.get('Disease')
    print(Disease)
    query = '''select distinct chartNo from correlationPatientDisease where topicNo = %s order by chartNo asc'''
    cursor = connections['default'].cursor()
    cursor.execute(query,[Disease])
    examID=''
    #examID = list(cursor.fetchall())
    for i,row in enumerate(cursor):
        examID += '<tr><td><input type="radio" onclick="GetTime()" name="confirmPID" id='+str(i)+'><label for='+str(i)+'>'+str(row[0])+'</label></td></tr>'
        
    return JsonResponse({'examID': examID})

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
def confirmpat2(request):
    PID=request.POST.get('ID')

    query = '''
        select a.chartNo,a.orderNo,a.eventDate, a.medType,b.TypeName,a.eventSummary,a.reportText,a.eventID
        from allEvents as a 
        inner join medTypeSet as b on a.medType=b.MedType
        where a.chartNo=%s
        order by a.eventDate desc
    '''
    cursor = connections['default'].cursor()
    cursor.execute(query,[PID])
    ChartNo=[]
    OrderNo=[]
    ExecDate=[]
    MedType=[]
    TypeName=[]
    ReportText=[]
    eventID=[]
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

    return JsonResponse({'eventID':eventID,'ChartNo': ChartNo,'OrderNo': OrderNo, 'ExecDate': ExecDate,'MedType':MedType , 'TypeName': TypeName,
                         'ReportText': ReportText})
@csrf_exempt
def Phase(request):

    query = '''select * from ClinicalEvents order by EventID asc '''
    cursor = connections['default'].cursor()
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
    cursor = connections['default'].cursor()
    cursor.execute(query,[eventID,diseaseNo])
    res = cursor.fetchall()
    if len(res)==0:
        Ignore = 1
        query = '''insert into Ignore (eventID,Ignore,diseaseNo) values(%s,%s,%s)'''
        cursor = connections['default'].cursor()
        cursor.execute(query,[eventID,Ignore,diseaseNo])
    else:
        Ignore = res[0][0]
        if Ignore == 0:
            Ignore = 1
            query = '''UPDATE Ignore SET Ignore=1 WHERE eventID=%s  AND diseaseNo=%s'''
            cursor = connections['default'].cursor()
            cursor.execute(query,[eventID,diseaseNo])
        elif Ignore == 1:
            Ignore = 0
            query = '''UPDATE Ignore SET Ignore=0 WHERE eventID=%s  AND diseaseNo=%s'''
            cursor = connections['default'].cursor()
            cursor.execute(query,[eventID,diseaseNo])
    return JsonResponse({'Ignore':Ignore})
@csrf_exempt
def updatePhase(request):
    Disease = request.POST.get('Disease')
    EventID = request.POST.get('Event')
    eventID = request.POST.get('eventID')
    IntervalNo = request.POST.get('IntervalNo')

    if EventID!=str(0):
        query = '''SELECT * FROM EventDefinition WHERE eventID=%s AND DiseaseNo=%s'''
        cursor = connections['default'].cursor()
        cursor.execute(query,[eventID,Disease])
        res = cursor.fetchall()
        if len(res)==0: #insert
            query = 'INSERT EventDefinition (eventID,DiseaseNo,EventID,IntervalNo) VALUES (%s,%s,%s,%s)'
            cursor = connections['default'].cursor()
            cursor.execute(query,[eventID,Disease,EventID,IntervalNo])
        elif len(res)==1: #update
            query = 'UPDATE EventDefinition SET EventID=%s WHERE DiseaseNo=%s AND eventID=%s'
            cursor = connections['default'].cursor()
            cursor.execute(query,[EventID,Disease,eventID])
    else:#請選擇階段，就刪除資料
        query = 'DELETE FROM EventDefinition WHERE DiseaseNo=%s AND eventID=%s'
        cursor = connections['default'].cursor()
        cursor.execute(query,[Disease,eventID])
    return JsonResponse({})
@csrf_exempt
def updateInterval(request):
    Disease = request.POST.get('Disease')
    eventID = request.POST.get('eventID')
    IntervalNo = request.POST.get('IntervalNo')
    query = '''SELECT * FROM EventDefinition WHERE eventID=%s AND DiseaseNo=%s'''
    cursor = connections['default'].cursor()
    cursor.execute(query,[eventID,Disease])
    res = cursor.fetchall()
    if len(res)==0: #insert
        query = 'insert EventDefinition(eventID,DiseaseNo,EventID,IntervalNo) values(%s,%s,%s,%s,%s)'
        cursor = connections['default'].cursor()
        cursor.execute(query,[eventID,Disease,str(-9999),IntervalNo])
    elif len(res)==1: #update
        query = 'UPDATE EventDefinition SET IntervalNo=%s WHERE DiseaseNo=%s AND eventID=%s'
        cursor = connections['default'].cursor()
        cursor.execute(query,[IntervalNo,Disease,eventID])
    return JsonResponse({})

@csrf_exempt
def searchNote(request):
    IND = request.POST.get('IND')
    eventID = request.POST.get('eventID')
    query = '''
      select  B.Disease,C.Enent,A.IntervalNo from EventDefinition as A 
      inner join diseaseGroup as B on A.DiseaseNo = B.DiseaseNo 
      inner join ClinicalEvents as C on A.EventID=C.EventID 
      where eventID=''' + eventID+''' Order by A.DiseaseNo ASC'''

    cursor = connections['default'].cursor()
    cursor.execute(query)
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
    IND = request.POST.get('IND')
    DiseaseNo = request.POST.get('DiseaseNo')
    eventID = request.POST.get('eventID')
    query = '''
    select  EventID,IntervalNo from EventDefinition 
    where eventID=''' + str(eventID)+''' AND DiseaseNo=''' + str(DiseaseNo)+'''
    '''
    cursor = connections['default'].cursor()
    cursor.execute(query)
    res = cursor.fetchall()

    if len(res)!=0:
        EventID=res[0][0]
        IntervalID=res[0][1]
    else:
        EventID=0
        IntervalID=1

    return JsonResponse({'IND':IND,'EventID':EventID,'IntervalID':IntervalID})