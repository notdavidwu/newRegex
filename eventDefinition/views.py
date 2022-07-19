
from cv2 import resize
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import numpy as np

@csrf_exempt
def confirm(request):
    au = request.session.get('au')
    de_identification = request.session.get('de_identification')
    eventDefinition_edit = request.session.get('eventDefinition_edit')
    if not request.user.is_authenticated : 
        return redirect('/')
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
    scrollTop = request.session.get('eventDefinition_scrollTop')
    filter = request.POST.get('filter')
    Disease = request.POST.get('Disease')

    diagChecked = request.POST.get('diagChecked')
    treatChecked = request.POST.get('treatChecked')
    fuChecked = request.POST.get('fuChecked')
    ambiguousChecked = request.POST.get('ambiguousChecked')
    pdConfirmed = request.POST.get('pdConfirmed')
    statusfilterValueSum = int(np.sum(np.array([diagChecked,treatChecked,fuChecked,ambiguousChecked,pdConfirmed]).astype(int)))

    cursor = connections['practiceDB'].cursor()

    query = 'EXEC EventDefinition_getPatient @filter=%s,@diseaseID=%s,@diagChecked=%s,@treatChecked=%s,@fuChecked=%s,@ambiguousChecked=%s,@pdConfirmed=%s,@statusfilterValueSum=%s'
    cursor.execute(query,[filter,Disease,diagChecked,treatChecked,fuChecked,ambiguousChecked,pdConfirmed,statusfilterValueSum])
 

    examID=''
    #examID = list(cursor.fetchall())
    for row in cursor:

        examID += f'''
        <tr><td>
        '''
        if filter=='0':
            examID += f'''
                <input type="radio" onclick="GetTime()" name="confirmPID" id={row[0]} data-isDone={int(row[4])}>
            '''
            if row[2] is True:
                examID += f'''<label for={row[0]}><p data-checked={row[3]} class="PatientListID exclude">{str(row[1])}</p><p class="ID">{row[0]}</p></label>'''
            else:
                examID += f'''<label for={row[0]}><p data-checked={row[3]} class="PatientListID ">{str(row[1])}</p><p class="ID">{row[0]}</p></label>'''
        else:    
            examID += f'''
                <input type="radio" onclick="GetTime()" name="confirmPID" id={row[0]} data-isDone=1>
            '''
            examID += f'''<label for={row[0]}><p class="PatientListID ">{str(row[1])}</p><p class="ID">{row[0]}</p></label>'''
        examID += f'''</td></tr>'''    
    return JsonResponse({'examID': examID,'scrollTop':scrollTop})

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
    request.session['eventDefinition_scrollTop']=scrollTop
    query = '''EXEC EventDefinition_getPatientEvent @chartNo = %s, @filter = %s'''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[PID,excludeFilter])
    objectArray=[]
    MedType=[]
    eventID=[]
    con = cursor.fetchall()
    for i in range(len(con)):
        MedType.append(con[i][3])
        eventID.append(con[i][6])
        eventChecked = con[i][7]
        note = con[i][8]
        if eventChecked is None:
            eventChecked=True
        if note is None:
            note=''
        
        object = f'''<tr><td>'''

        object += f'''<input type="radio" onclick="GetReport();getCurrentEventProcedure();" name="timePID" data-eventCheck={eventChecked} id=timePID{i}>
                    <label for=timePID{i}>'''
        object += f'''
        <div class="pdID">{i}</div>
        <div class="eventID">{con[i][6]}</div>
        <div class="ChartNo">{con[i][0]}</div>
        <div class="OrderNo">{con[i][1]}</div>
        <div class="edate">{con[i][2]}</div>
        <div class="medType">{con[i][3]}</div>
        <div class="type2">{con[i][4]}</div>
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

    return JsonResponse({'eventID':eventID,'MedType':MedType ,'objectArray':objectArray,'eventID_F':eventID_F})

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
    ind=request.POST.get('ind')
    eventID=request.POST.get('eventID')
    cursor = connections['practiceDB'].cursor()
    query= '''
	select a.chartNo,a.orderNo,a.eventDate,a.medType,b.typeName,c.descriptionType,c.reportText,a.eventID,a.note
	from allEvents as a
	inner join medTypeSet as b on a.medType=b.medType
	left join eventDetails as c on a.eventID=c.eventID
	where a.eventID_F=%s and (c.descriptionType=3 or c.descriptionType is null) order by a.eventDate 
    '''
    cursor.execute(query,[eventID])
    result = cursor.fetchall()
    object=''
    for i,row in enumerate(result):
        object += f'''<tr><td class="hiddenRow" onclick="showReport()">'''
        object += f'''
        <div  class="accordian-body collapse collapse{ind} " id="collapse{ind}" >'''

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

    return JsonResponse({'objectList':object})

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
    eventID = request.POST.get('eventID')
    username = request.POST.get('username')
    query = '''
        EXEC EventDefinition_searchRecord @chartNo = %s,@eventID=%s, @username = %s
    '''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[chartNo,eventID,username])
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
    return JsonResponse({})

@csrf_exempt
def updateInducedEvent(request):
    eventID_F = request.POST.get('eventID_F')
    eventID = request.POST.get('eventID')
    query = 'update allEvents set eventID_F=%s where eventID=%s'
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[eventID_F,eventID])
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
    medType = request.POST.get('medType')
    query = '''
        EXEC EventDefinition_getClinicalProcedures @medType = %s
    '''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[medType])
    result = cursor.fetchall()
    selection = '<option value=0>請確認階段</option>'
    for row in result:
        selection += f'<option value={row[0]}>{row[1]}</option>'
    return JsonResponse({'selection':selection})

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
            where medType=%s and diseaseID=%s and procedureID=%s 
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
    formObject=''
    dictionary={}
    if len(eventFactorCode)!=0:
        eventFactorID=eventFactorCode
        '''---------------查詢有無紀錄--------------'''
        searchRecord = '''SELECT * FROM [practiceDB].[dbo].[extractedFactors] where eventID=%s'''
        cursor.execute(searchRecord,[eventID])
        recordedOrNot = len(cursor.fetchall())
        '''---------------取得大標題--------------'''
        if recordedOrNot !=0:
            mainSubjectQuery='''
            select eventFactorID,factorName,itemType,labeled,dense_rank() OVER ( ORDER BY serialNo)-1 as dr
            from eventFactor as a
            where a.F_eventFactorID=0 and eventFactorCode=%s
            group by eventFactorID,factorName,itemType,labeled,serialNo
            '''
            cursor.execute(mainSubjectQuery,[eventFactorID])
        else:
            mainSubjectQuery='''
            select eventFactorID,factorName,itemType,labeled,dense_rank() OVER ( ORDER BY serialNo)-1 as dr
            from eventFactor as a
            where a.F_eventFactorID=0 and eventFactorCode=%s
            group by eventFactorID,factorName,itemType,labeled,serialNo
            '''
            cursor.execute(mainSubjectQuery,[eventFactorID])
        step = 1
        
        mainSubjectSet = cursor.fetchall()
        formObject = '<div class="formStructure">'
        num=0
        for ind1,mainSubject in enumerate(mainSubjectSet):
            step = 2
            formObject += f'<div data-prepareAdd=0 onmousedown="record()" class="mainBlock mainBlock{mainSubject[4]}" >'
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
            
            
            for ind2,structure in enumerate(structureSet):
                formObject += '<ul>'
                num += 1
                type = structure[4].replace(' ','')
                stop = structure[7]
                if type=='text':
                    formObject += f'''
                    <li>
                        <label for="item_{num}">{structure[3]}：
                        <input type={type} name="formStructure_[1]_[{ind1}][{structure[6]}]" data-recorded=0 data-eventFactorID={structure[0]} id="item_{num}"></label>
                    </li>
                    '''
                elif type=='date':
                    formObject += f'''<li><input onclick="myFunction()" data-recorded=0 data-checked=0 type={type} data-eventFactorID={structure[0]} name="formStructure_[1]_[{ind1}][{structure[6]}]" id="item_{num}" value="{structure[3]}"></li>'''  
                elif type=='NE':
                    formObject += f'''<li class="H_{stop}"><label for="item_{num}">{structure[3]}</label></li>'''
                else:
                    formObject += f'''<li><input onclick="myFunction()" data-recorded=0 data-checked=0 type={type} data-eventFactorID={structure[0]} name="formStructure_[1]_[{ind1}][{structure[6]}]" id="item_{num}"><label for="item_{num}">{structure[3]}</label></li>'''

                factorID=structure[0]
                if stop != True:
                    step = 3
                    formObject,num = subForm(dictionary,3,ind1,num,factorID,formObject,cursor)
                    
                formObject += '</ul>'
            formObject += '</div>'

        formObject += '</div>'
    return JsonResponse({'formObject':formObject})

def subForm(dictionary,depth,ind1,num,factorID,formObject,cursor):
    
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
            formObject += f'''<li class="H_{stop}"><label for="item_{num}">{structure[3]}：</label><input onclick="myFunction()" data-recorded=0 data-checked=0 type={type} data-eventFactorID={structure[0]} name=formStructure_[1]_[{ind1}][{structure[6]}] id="item_{num}"></li>'''
        elif type=='NE':
            formObject += f'''<li class="H_{stop}"><label for="item_{num}">{structure[3]}</label></li>'''
        else:
            formObject += f'''<li class="H_{stop}"><input onclick="myFunction()" data-recorded=0 data-checked=0 type={type} name=formStructure_[1]_[{ind1}][{structure[6]}] data-eventFactorID={structure[0]} id="item_{num}"><label for="item_{num}">{structure[3]}</label></li>'''
        factorID=structure[0]
        if stop != True:
            formObject,num = subForm(dictionary,depth+1,ind1,num,factorID,formObject,cursor)
    formObject += '</ul>'
    
    return formObject,num

@csrf_exempt
def insertExtractedFactors(request):
    cursor = connections['practiceDB'].cursor()
    eventID = request.POST.get('eventID')
    eventFactorCode = request.POST.get('version')
    insertSeq = request.POST.get('insertSeq')
    insertIDArray = request.POST.getlist('insertIDArray[]')
    insertValArray = request.POST.getlist('insertValArray[]')
    insertRecordedArray = request.POST.getlist('insertRecordedArray[]')

    queryDelete='''DELETE 
    FROM [practiceDB].[dbo].[extractedFactors] where factorID in 
    (select eventFactorID from eventFactor where eventFactorCode=%s)
    and eventID=%s and seq=%s'''
    cursor.execute(queryDelete,[eventFactorCode,eventID,insertSeq])
    print(eventFactorCode,eventID,insertSeq)
    query = '''select * from extractedFactors where eventID=%s and factorID=%s and seq=%s'''
    for factorID,factorValue,Recorded in zip(insertIDArray,insertValArray,insertRecordedArray):
        cursor.execute(query,[eventID,factorID,insertSeq])
        if len(cursor.fetchall())==0: # =0, insert this data
            queryInsert='''insert into extractedFactors (eventID,factorID,factorValue,seq) VALUES(%s,%s,%s,%s)'''
            cursor.execute(queryInsert,[eventID,factorID,factorValue,insertSeq])
            print(eventID,factorID,factorValue,insertSeq)
    return JsonResponse({})

@csrf_exempt
def searchExtractedFactorsRecord(request):
    cursor = connections['practiceDB'].cursor()
    eventID = request.POST.get('eventID')
    diseaseId = request.POST.get('diseaseId')
    seq = request.POST.get('seq')
    idArray = request.POST.getlist('idArray[]')
    classArray = request.POST.getlist('classArray[]')
    query='''select factorValue from extractedFactors where eventID=%s and factorID=%s and seq=%s'''
    factorIdRecorded = []
    factorValueRecorded = []
    seqRecorded = []
    classRecorded = []

    for factorId,className in zip(idArray,classArray):
        cursor.execute(query,[eventID,factorId,seq])
        result = cursor.fetchall()

        if len(result)!=0:
            seqRecorded.append(seq)
            classRecorded.append(className)
            factorIdRecorded.append(factorId)
            factorValueRecorded.append(result[0][0])

    return JsonResponse({'seqRecorded':seqRecorded,'classRecorded':classRecorded,'factorIdRecorded':factorIdRecorded,'factorValueRecorded':factorValueRecorded})

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

    deleteQuery = 'delete from eventFactor where eventFactorCode=%s'
    cursor.execute(deleteQuery,[eventFactorCode])
    
    for eventFactorID,serialNo,factorName,itemType,labeled,F_eventFactorID,isLeaf in zip(eventFactorIDSet,serialNoSet,factorNameSet,itemTypeSet,labeledSet,F_eventFactorIDSet,isLeafSet):
        insertQuery='insert into eventFactor values(%s,%s,%s,%s,%s,%s,%s,%s)'
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
    SELECT distinct groupNo
    FROM [practiceDB].[dbo].[eventFactorCode] as a
    inner join clinicalProcedures as b on a.procedureID=b.procedureID
    inner join diseasetList as c on a.diseaseID=c.diseaseID

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
    eventFactorCode,groupNo,diseaseID,disease,procedureID,procedureName,version = [],[],[],[],[],[],[]
    for row in result_EventFactorCode:
        eventFactorCode.append(row[0])
    result_GroupNo = cursor.execute(queryGroupNo)
    for row in result_GroupNo:
        groupNo.append(row[0])
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

    return JsonResponse({'eventFactorCode':eventFactorCode,'groupNo':groupNo,'diseaseID':diseaseID,'disease':disease,'procedureID':procedureID,'procedureName':procedureName,'version':version})

@csrf_exempt
def getNewEventFactorID(request):
    cursor = connections['practiceDB'].cursor()
    query = 'SELECT  MAX([eventFactorID])+1 FROM [practiceDB].[dbo].[eventFactor]'
    cursor.execute(query,[])
    newEventFactorID = cursor.fetchall()[0][0]
    return JsonResponse({'newEventFactorID':newEventFactorID})

@csrf_exempt
def getSeqNoOption(request):
    chartNo=request.POST.get('chartNo')
    query = '''
        select caSeqNo from PatientDisease where chartNo=%s order by caSeqNo
    '''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[chartNo])
    result = cursor.fetchall()
    seqNo=''
    for row in result:
        seqNo += f'<option value={row[0]}>{row[0]}</option>'
    return JsonResponse({'seqNo':seqNo})

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
                inner join correlationPatientDisease as b on a.topicNo=b.diseaseNo
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
        SELECT topicNo,topicName,COUNT(chartNo) FROM(
        SELECT distinct topicNo,topicName,c.chartNo FROM [practiceDB].[dbo].[researchTopic] as a
        inner join correlationPatientDisease as b on a.topicNo=b.diseaseNo 
        inner join PatientDisease as c on b.chartNo=c.chartNo and a.diseaseID=c.diseaseID
        where a.diseaseID=%s
        ) as num
        GROUP BY topicNo,topicName
        order by topicNo
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
    insert into correlationPatientDisease(chartNo,diseaseNo)
    select a.chartNo,%s as diseaseNo from (select %s as 'chartNo') as a
    left outer join (
        select * from correlationPatientDisease where diseaseNo=%s
    ) as b on a.chartNo=b.chartNo
    where b.chartNo is null
    '''
    cursor.execute(query_insertAnnotation,[topicNo,chartNo,topicNo])

def deleteAnnotation(cursor,topicNo,chartNo):
    query = 'delete from annotation where topicNo=%s and chartNo=%s'
    cursor.execute(query,[topicNo,chartNo])

def deleteCorrelationPatientDisease(cursor,topicNo,chartNo):
    query = 'delete from correlationPatientDisease where diseaseNo = %s and chartNo=%s'
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
