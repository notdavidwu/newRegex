from asyncio.windows_events import NULL
from cv2 import resize
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect


@csrf_exempt
def confirm(request):
    au = request.session.get('au')
    de_identification = request.session.get('de_identification')
    return render(request, 'poolConfirm/confirm.html',{'au':au,'de_identification':de_identification})


@csrf_exempt
def confirmpat(request):
    Disease = request.POST.get('Disease')
    query = '''
    select [PD],[chartNo] from(
    SELECT [PD],[chartNo],[diseaseId],[caSeqNo],[diagStatus],[treatStatus],[confirmed]
    ,ROW_NUMBER() Over (Partition By [chartNo] Order By [caSeqNo] Desc) As Sort
    FROM [coreDB].[dbo].[PatientDisease] where diseaseId=%s
    ) as a where  a.Sort=1
    '''
    cursor = connections['coreDB'].cursor()
    cursor.execute(query,[Disease])
    examID=''
    #examID = list(cursor.fetchall())
    for row in cursor:
        examID += f'''
        <tr><td>
        <input type="radio" onclick="GetTime()" name="confirmPID" id={row[0]}>
        <label for={row[0]}><p class="PatientListID">{str(row[1])}</p><p class="ID">{row[0]}</p></label>
        </td></tr>
        '''
        
    return JsonResponse({'examID': examID})

@csrf_exempt
def Disease(request):
    query = '''select * from diseasetList'''
    cursor = connections['coreDB'].cursor()
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

    # query = '''
    # select b.chartNo,f.orderNo,f.eventDate,f.medType,e.typeName,g.descriptionType,g.reportText,f.eventID,b.PD
    # from diseasetList as a inner join PatientDisease as b on a.diseaseId=b.diseaseId
    #     left outer join allEvents as f on b.chartNo=f.chartNo 
    #     inner join medTypeSet as e on e.medType=f.medType
    #     left outer join eventDetails as g on f.eventID=g.eventID
    # where b.chartNo=%s and g.descriptionType=3
    # order by f.eventDate DESC
    # '''

    query = '''
    select a.chartNo,a.orderNo,a.eventDate,a.medType,b.typeName,c.descriptionType,c.reportText,a.eventID from allEvents as a
	inner join medTypeSet as b on a.medType=b.medType
	inner join eventDetails as c on a.eventID=c.eventID
	where a.chartNo=%s and c.descriptionType=3 and eventID_F is null 
    '''
    cursor = connections['coreDB'].cursor()
    cursor.execute(query,[PID])
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
        <div class="pdID">{i}</div>
        <div class="eventID">{con[i][7]}</div>
        <div class="ChartNo">{con[i][0]}</div>
        <div class="OrderNo">{con[i][1]}</div>
        <div class="edate">{con[i][2]}</div>
        <div class="type2">{con[i][4].replace(' ','')}</div>
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
        object += f'''</label></tr></td>'''
        objectArray.append(object)

    query= '''
	select distinct eventID_F
	from allEvents as a
	inner join medTypeSet as b on a.medType=b.medType
	inner join eventDetails as c on a.eventID=c.eventID
	where a.chartNo=%s and c.descriptionType=3 and eventID_F is not null
    '''
    cursor.execute(query,[PID])
    eventID_F=[]
    res = cursor.fetchall()
    for i in range(len(res)):
        eventID_F.append(res[i][0])

    return JsonResponse({'eventID':eventID,'MedType':MedType ,'objectArray':objectArray,'eventID_F':eventID_F})

@csrf_exempt
def addInducedEvent(request):
    ind=request.POST.get('ind')
    eventID=request.POST.get('eventID')
    cursor = connections['coreDB'].cursor()
    query= '''
	select a.chartNo,a.orderNo,a.eventDate,a.medType,b.typeName,c.descriptionType,c.reportText,a.eventID 
	from allEvents as a
	inner join medTypeSet as b on a.medType=b.medType
	inner join eventDetails as c on a.eventID=c.eventID
	where a.eventID_F=%s and c.descriptionType=3 
    '''
    cursor.execute(query,[eventID])
    result = cursor.fetchall()
    object=''
    for i,row in enumerate(result):
        object += f'''<tr><td onclick="showReport()">'''
        object += f'''
        <div  class="accordion-collapse collapse sow collapseItem collapse{ind} " id="collapse{ind}" >'''

        object += f'''
        <div class="pdID">?</div>
        <div class="eventID">{row[7]}</div>
        <div class="ChartNo">{row[0]}</div>
        <div class="OrderNo">{row[1]}</div>
        <div class="edate">{row[2]}</div>
        <div class="type2">{row[4].replace(' ','')}</div>
        ''' 
        if row[3] == 30001 or row[3]==30002:
            object += f'''<p class="report2">{row[5]}</p>'''
        else:
            object += f'''
                <div class="note"></div>
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
    cursor = connections['coreDB'].cursor()
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
    EDID = NULL if request.POST.get('EDID')=='-1' else request.POST.get('EDID')
    PDID = request.POST.get('PDID')
    eventID = request.POST.get('eventID')
    procedureID = request.POST.get('procedureID')
    cursor = connections['coreDB'].cursor()
    print(int(procedureID)==0)
    print(procedureID)
    print(len(procedureID))
    if procedureID=='0':
        query = 'DELETE FROM eventDefinitions WHERE EDID=%s'
        cursor.execute(query,[EDID])
    else:
        if EDID is NULL: #insert
            query = f'INSERT eventDefinitions (eventID,PDID,procedureID) OUTPUT INSERTED .EDID VALUES ({eventID},{PDID},{procedureID})'
            cursor.execute(query)
            EDID = cursor.fetchall()[0]
        else: #update
            query = 'UPDATE eventDefinitions SET procedureID=%s WHERE EDID=%s'
            cursor.execute(query,[procedureID,EDID])


    return JsonResponse({'sno':[EDID]})
@csrf_exempt
def updateInterval(request):
    EDID = NULL if request.POST.get('EDID')=='-1' else request.POST.get('EDID')
    PDID = NULL if request.POST.get('PDID')=='-1' else request.POST.get('PDID')
    eventID = request.POST.get('eventID')
    chartNo = request.POST.get('chartNo')
    procedureID=request.POST.get('procedureID')

    newSeqNo = request.POST.get('newSeqNo')
    originSeqNo = int(request.POST.get('originSeqNo'))
    diseaseId = request.POST.get('diseaseId')
    cursor = connections['coreDB'].cursor()
    '''先搜尋該seqNo有沒有預設在PatientDease'''
    query_presearch='''select PD,diagStatus,treatStatus from PatientDisease where chartNo=%s and caSeqNo=%s and diseaseId=%s'''
    cursor.execute(query_presearch,[chartNo,newSeqNo,diseaseId])
    searchResult = cursor.fetchall()
    
    if int(newSeqNo)==0:
        query_presearch='''select PD,diagStatus,treatStatus from PatientDisease where chartNo=%s and caSeqNo=%s and diseaseId=%s'''
        cursor.execute(query_presearch,[chartNo,originSeqNo,diseaseId])
        searchResult3 = cursor.fetchall()
        print(searchResult3)
        diagStatus = searchResult3[0][1]
        treatStatus = searchResult3[0][2]
        if diagStatus is None and treatStatus is None:
            queryDelete='''DELETE FROM PatientDisease WHERE PD=%s'''
            cursor.execute(queryDelete,[PDID])
        query = 'DELETE FROM eventDefinitions WHERE EDID=%s'
        cursor.execute(query,[EDID])
        returnPDID=-1
        EDID=-1
    else:
        if len(searchResult)==0:
            '''insert new caSeqNo into PatientDease'''
            queryInsert = '''INSERT INTO PatientDisease (chartNo,diseaseId,caSeqNo) OUTPUT INSERTED .PD VALUES(%s,%s,%s)'''
            cursor.execute(queryInsert,[chartNo,diseaseId,newSeqNo])
            newPDID = cursor.fetchall()[0][0]
            if PDID is not NULL:
                '''修改 eventDefinitions PDID'''
                queryModify = '''UPDATE eventDefinitions SET PDID=%s where PDID=%s and eventID=%s'''
                cursor.execute(queryModify,[newPDID,PDID,eventID])
            else:
                queryInsert = 'INSERT eventDefinitions (eventID,PDID,procedureID) OUTPUT INSERTED .EDID VALUES (%s,%s,%s)'
                cursor.execute(queryInsert,[eventID,newPDID,procedureID])
                EDID = cursor.fetchall()[0]
            returnPDID=newPDID
        else:
            '''先找舊的PDID'''
            querySearch='''select PD,diagStatus,treatStatus from PatientDisease where chartNo=%s and caSeqNo=%s and diseaseId=%s'''
            if int(originSeqNo)!=0:
                cursor.execute(querySearch,[chartNo,originSeqNo,diseaseId])
            else:
                cursor.execute(querySearch,[chartNo,newSeqNo,diseaseId])
            searchResult2 = cursor.fetchall()
            oldPDID = searchResult2[0][0]
            diagStatus = searchResult2[0][1]
            treatStatus = searchResult2[0][2]

            returnPDID=searchResult[0][0]

            '''如果 diagStatus or treatStatus 不是null 代表是癌登資料，不刪除'''
            if diagStatus is None and treatStatus is None:
                queryDelete='''DELETE FROM PatientDisease WHERE PD=%s'''
                cursor.execute(queryDelete,[oldPDID])
            if PDID is not NULL:
                '''修改 eventDefinitions PDID'''
                queryModify = '''UPDATE eventDefinitions SET PDID=%s where PDID=%s and eventID=%s'''
                cursor.execute(queryModify,[returnPDID,oldPDID,eventID])
            else:
                queryInsert = 'INSERT eventDefinitions (eventID,PDID,procedureID) OUTPUT INSERTED .EDID VALUES (%s,%s,%s)'
                cursor.execute(queryInsert,[eventID,oldPDID,procedureID])
                EDID = cursor.fetchall()[0]

        
    return JsonResponse({'EDID':EDID,'returnPDID':returnPDID})

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
    from diseasetList as a inner join PatientDisease as b on a.diseaseId=b.diseaseId
        inner join eventDefinitions as c on b.PD=c.PDID
        inner join ProcedureEvent as d on c.procedureID=d.procedureID
        inner join medTypeSet as e on d.groupNo=e.groupNo
        left outer join allEvents as f on b.chartNo=f.chartNo and e.medType=f.medType
        left outer join eventDetails as g on f.eventID=g.eventID
    where b.chartNo=%s and f.eventDate is not null  and descriptionType=3 and DATEDIFF(DAY, c.caregExecDate, f.eventDate) between -5 and 5
    ) as res where res.eventID=%s
    '''
    cursor = connections['coreDB'].cursor()
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
    print(eventID)
    print(chartNo)
    query = '''
        select * from (
        select b.caSeqNo,c.EDID,c.eventID,c.procedureID,f.eventID as 'eventID_F',b.PD,c.caregExecDate,f.eventDate
        from diseasetList as a inner join PatientDisease as b on a.diseaseId=b.diseaseId
            inner join eventDefinitions as c on b.PD=c.PDID
            inner join ProcedureEvent as d on c.procedureID=d.procedureID
            inner join medTypeSet as e on d.groupNo=e.groupNo
            left outer join allEvents as f on b.chartNo=f.chartNo and e.medType=f.medType
            left outer join eventDetails as g on f.eventID=g.eventID
        where b.chartNo=%s and f.eventDate is not null  and descriptionType=3 
        and  (DATEDIFF(DAY, c.caregExecDate, f.eventDate) between -5 and 5 or  c.caregExecDate is null)  
        and ((c.eventID is null and f.eventID is not null) or (c.eventID is not null and c.eventID=f.eventID))
        ) as res  where res.eventID_F=%s
    '''
    cursor = connections['coreDB'].cursor()
    cursor.execute(query,[chartNo,eventID])
    res = cursor.fetchall()

    caSeqNo = []
    EDID = []
    PDID = []
    procedureID = []
    eventID = []
    eventID_F = []
    print(len(res))
    if len(res)!=0:
        Record = len(res)
        for row in res:
            caSeqNo.append(row[0])
            EDID.append(row[1])
            eventID.append(row[2])
            procedureID.append(row[3])
            eventID_F.append(row[4])
            PDID.append(row[5])
    else:
        Record = 1
        EDID=[-1]
        eventID=[0]
        caSeqNo=[0]
        procedureID=[0]
        eventID_F=[0]
        PDID = ['-1']
    print(procedureID)
    return JsonResponse({'IND':IND,'Record':Record,'caSeqNo':caSeqNo,'EDID':EDID,'eventID':eventID,'procedureID':procedureID,'eventID_F':eventID_F,'PDID':PDID})

@csrf_exempt
def updateCancerRegist(request):
    EDID = request.POST.get('EDID')
    eventID = request.POST.get('eventID')
    query = 'UPDATE eventDefinitions SET eventID=%s WHERE EDID=%s'
    cursor = connections['coreDB'].cursor()
    cursor.execute(query,[eventID,EDID])
    return JsonResponse({})

@csrf_exempt
def updateInducedEvent(request):
    eventID_F = request.POST.get('eventID_F')
    eventID = request.POST.get('eventID')
    query = 'update allEvents set eventID_F=%s where eventID=%s'
    cursor = connections['coreDB'].cursor()
    cursor.execute(query,[eventID_F,eventID])
    return JsonResponse({})

@csrf_exempt
def deleteEvent_F(request):
    eventID = request.POST.get('eventID')
    query = 'update allEvents set eventID_F=NULL where eventID=%s'
    cursor = connections['coreDB'].cursor()
    cursor.execute(query,[eventID])
    return JsonResponse({})

@csrf_exempt
def getClinicalProcedures(request):
    medType = request.POST.get('medType')
    query = '''
        select c.procedureID,c.procedureName from medTypeSet as a
        inner join ProcedureEvent as b on a.groupNo=b.groupNo
        inner join clinicalProcedures as c on b.[procedureID]=c.[procedureID]
        where medType=%s
        order by c.procedureID
    '''
    cursor = connections['coreDB'].cursor()
    cursor.execute(query,[medType])
    result = cursor.fetchall()
    selection = '<option value=0>請確認階段</option>'
    for row in result:
        selection += f'<option value={row[0]}>{row[1]}</option>'
    return JsonResponse({'selection':selection})
