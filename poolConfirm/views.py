
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
    if len(statusfilter)>15:
        statusfilter=''
    return statusfilter
import re
@csrf_exempt
def confirmpat(request):
    filter = request.POST.get('filter')
    Disease = request.POST.get('Disease')
    statusfilterNames = request.POST.getlist('statusfilterNames[]')
    cursor = connections['practiceDB'].cursor()
    if filter=='0':
        query = '''
        select [PD],[chartNo],[pdConfirmed] 
        from(
            SELECT *
            ,ROW_NUMBER() Over (Partition By [chartNo] Order By [caSeqNo] Desc) As Sort
            FROM [PatientDisease] where [diseaseID]=%s '''
        for statusfilter in statusfilterNames:
            statusfilter = replaceCapitalAndLowCase(statusfilter)
            query +=f' and {statusfilter}=1 '
        query += ') as a where  a.Sort=1 and a.chartNo>0'
    elif filter=='1':
        query = '''
        select a.PD,a.chartNo from(
            select [PD],[chartNo] 
            from(
                SELECT *
                ,ROW_NUMBER() Over (Partition By [chartNo] Order By [caSeqNo] Desc) As Sort
                FROM [PatientDisease] where [diseaseID]=%s '''
        for statusfilter in statusfilterNames:
            statusfilter = replaceCapitalAndLowCase(statusfilter)
            query +=f' and {statusfilter}=1 '

        query +='''    ) as a where a.Sort=1 and a.chartNo>0
        ) as a
        left outer join allEvents as b on a.chartNo=b.chartNo
        where b.eventChecked is null
        group by a.PD,a.chartNo,b.eventChecked
        order by a.chartNo,b.eventChecked ASC
        '''
    elif filter=='2':
        query = '''
        select a.PD,a.chartNo from(
            select [PD],[chartNo] 
            from(
                SELECT *
                ,ROW_NUMBER() Over (Partition By [chartNo] Order By [caSeqNo] Desc) As Sort
                FROM [PatientDisease] where [diseaseID]=%s '''
        for statusfilter in statusfilterNames:
            statusfilter = replaceCapitalAndLowCase(statusfilter)
            query +=f' and {statusfilter}=1 '
        query +='''
            ) as a where a.Sort=1 and a.chartNo>0
        ) as a
        left outer join allEvents as b on a.chartNo=b.chartNo
        where b.eventChecked is not null
        group by a.PD,a.chartNo,b.eventChecked
        order by a.chartNo,b.eventChecked ASC
        '''
    cursor.execute(query,[Disease])
    

    examID=''
    #examID = list(cursor.fetchall())
    for row in cursor:
        examID += f'''
        <tr><td>
        <input type="radio" onclick="GetTime()" name="confirmPID" id={row[0]}>
        '''
        if filter=='0':
            if row[2] is True:
                examID += f'''<label for={row[0]}><p class="PatientListID exclude">{str(row[1])}</p><p class="ID">{row[0]}</p></label>'''
            else:
                examID += f'''<label for={row[0]}><p class="PatientListID ">{str(row[1])}</p><p class="ID">{row[0]}</p></label>'''
        else:    
            examID += f'''<label for={row[0]}><p class="PatientListID ">{str(row[1])}</p><p class="ID">{row[0]}</p></label>'''
        examID += f'''</td></tr>'''    

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
    select a.chartNo,a.orderNo,a.eventDate,a.medType,b.typeName,c.descriptionType,c.reportText,a.eventID 
	from allEvents as a
	inner join medTypeSet as b on a.medType=b.medType
	left join eventDetails as c on a.eventID=c.eventID
	where a.chartNo=%s and (c.descriptionType=3 or c.descriptionType=5 or  c.descriptionType is NULL) and eventID_F is null 
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
        <div class="medType">{con[i][3]}</div>
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
def getCancerRegistData(request):
    chartNo = request.POST.get('chartNo')
    query = ''' 
            select disease,caSeqNo,c.caregExecDate,d.procedureName
                from PatientDisease as a
                inner join diseasetList as b on a.diseaseId=b.diseaseId
                inner join eventDefinitions as c on a.PD=c.PDID
                inner join clinicalProcedures as d on c.procedureID=d.procedureID
                where chartNo=%s and c.caregExecDate is not NULL
            '''
    cursor = connections['coreDB'].cursor()
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
        <div class="medType">{row[3]}</div>
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
def updatePhase(request):
    EDID = 'NULL' if request.POST.get('EDID')=='-1' else request.POST.get('EDID')
    PDID = request.POST.get('PDID')
    eventID = request.POST.get('eventID')
    procedureID = request.POST.get('procedureID')
    chartNo = request.POST.get('chartNo')
    diseaseId = request.POST.get('diseaseId')
    originSeqNo = request.POST.get('originSeqNo')
    cursor = connections['coreDB'].cursor()

    if procedureID=='0':
        query = 'DELETE FROM eventDefinitions WHERE EDID=%s'
        cursor.execute(query,[EDID])
    else:
        
        if PDID == 'Infinity':
            query = 'SELECT top(1)PD,caSeqNo FROM PatientDisease WHERE chartNo = %s'
            cursor.execute(query,[chartNo])
            res=cursor.fetchall()
            PDID = res[0][0]
            originSeqNo = res[0][1]
            
            if len(res)==0:
                queryInsert = '''INSERT INTO PatientDisease (chartNo,diseaseId,caSeqNo) OUTPUT INSERTED .PD VALUES(%s,%s,%s)'''
                cursor.execute(queryInsert,[chartNo,diseaseId,1])
                PDID = cursor.fetchall()[0][0]
        if EDID == 'NULL': #insert
            query = 'INSERT eventDefinitions (eventID,PDID,procedureID) OUTPUT INSERTED .EDID VALUES (%s,%s,%s)'
            cursor.execute(query,[eventID,PDID,procedureID])
            EDID = cursor.fetchall()[0]
        else: #update
            query = 'UPDATE eventDefinitions SET procedureID=%s WHERE EDID=%s'
            cursor.execute(query,[procedureID,EDID])
    return JsonResponse({'sno':[EDID],'originSeqNo':[originSeqNo]})
@csrf_exempt
def updateInterval(request):
    EDID = 'NULL' if request.POST.get('EDID')=='-1' else request.POST.get('EDID')
    PDID = 'NULL' if request.POST.get('PDID')=='-1' else request.POST.get('PDID')
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
            if PDID != 'NULL':
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
            if PDID != 'NULL':
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

@csrf_exempt
def getNum(request):
    cursor = connections['practiceDB'].cursor()
    disease = request.POST.get('disease')
    statusfilterNames = request.POST.getlist('statusfilterNames[]')

    query = '''
    select COUNT(chartNo) as NUM 
    from(
        SELECT [PD],[chartNo],[diseaseID],[caSeqNo],[diagStatus],[treatStatus]
        ,ROW_NUMBER() Over (Partition By [chartNo] Order By [caSeqNo] Desc) As Sort
        FROM [PatientDisease] where [diseaseID]=%s'''
    for statusfilter in statusfilterNames:
        statusfilter = replaceCapitalAndLowCase(statusfilter)
        query +=f' and {statusfilter}=1 '
    query += '''    
    ) as a where  a.Sort=1 and a.chartNo>0
    UNION ALL

    select COUNT(chartNo) as NUM  from (
        select a.PD,a.chartNo from(
            select [PD],[chartNo] 
            from(
                SELECT [PD],[chartNo],[diseaseID],[caSeqNo],[diagStatus],[treatStatus]
                ,ROW_NUMBER() Over (Partition By [chartNo] Order By [caSeqNo] Desc) As Sort
                FROM [PatientDisease] where [diseaseID]=%s'''
    for statusfilter in statusfilterNames:
        statusfilter = replaceCapitalAndLowCase(statusfilter)
        query +=f' and {statusfilter}=1 '                
    query +='''
            ) as a where a.Sort=1 and a.chartNo>0
        ) as a
        left outer join allEvents as b on a.chartNo=b.chartNo
        where b.eventChecked is null
        group by a.PD,a.chartNo,b.eventChecked
    ) as result1
    UNION ALL

    select COUNT(chartNo) as NUM  from (
    select a.PD,a.chartNo from(
        select [PD],[chartNo] 
        from(
            SELECT [PD],[chartNo],[diseaseID],[caSeqNo],[diagStatus],[treatStatus]
            ,ROW_NUMBER() Over (Partition By [chartNo] Order By [caSeqNo] Desc) As Sort
            FROM [PatientDisease] where [diseaseID]=%s'''
    for statusfilter in statusfilterNames:
        statusfilter = replaceCapitalAndLowCase(statusfilter)
        query +=f' and {statusfilter}=1 '
    query +='''
        ) as a where a.Sort=1 and a.chartNo>0
    ) as a
    left outer join allEvents as b on a.chartNo=b.chartNo
    where b.eventChecked is not null
    group by a.PD,a.chartNo,b.eventChecked
    ) as result2

    '''
    cursor.execute(query,[disease,disease,disease])
    num=[]
    res = cursor.fetchall()
    for row in res:
        num.append(row[0])
    return JsonResponse({'num':num})


@csrf_exempt
def updatePatientStatus(request):
    PDSet = request.POST.getlist('PD[]')
    diagCheckedSet = request.POST.getlist('diagChecked[]')
    treatCheckedSet = request.POST.getlist('treatChecked[]')
    fuCheckedSet = request.POST.getlist('fuChecked[]')
    pdConfirmedSet = request.POST.getlist('pdConfirmed[]')
    adjTreatCheckedSet = request.POST.getlist('adjTreatChecked[]')
    neoTreatCheckedSet = request.POST.getlist('neoTreatChecked[]')
    query = '''UPDATE PatientDisease SET diagChecked = %s,treatChecked=%s,fuChecked=%s,pdConfirmed=%s,adjTreatChecked=%s,neoTreatChecked=%s where PD = %s'''
    cursor = connections['practiceDB'].cursor()
    for diagChecked,treatChecked,fuChecked,pdConfirmed,adjTreatChecked,neoTreatChecked,PD in zip(diagCheckedSet,treatCheckedSet,fuCheckedSet,pdConfirmedSet,adjTreatCheckedSet,neoTreatCheckedSet,PDSet):
        cursor.execute(query,[diagChecked,treatChecked,fuChecked,pdConfirmed,adjTreatChecked,neoTreatChecked,PD])
    return JsonResponse({})

@csrf_exempt
def getPatientStatus(request):
    cursor = connections['practiceDB'].cursor()
    chartNo = request.POST.get('chartNo')
    disease = request.POST.get('diseaseId')
    query='''
    select PD, b.disease, caSeqNo, diagChecked, treatChecked, fuChecked, pdConfirmed, neoTreatChecked, adjTreatChecked
    from PatientDisease as a 
    inner join diseasetList as b on a.diseaseID=b.diseaseID
    where a.chartNo=%s and a.diseaseID=%s 
    '''
    cursor.execute(query,[chartNo,disease])
    PD,disease,caSeqNo,diagChecked,treatChecked,fuChecked,pdConfirmed,neoTreatChecked,adjTreatChecked=[],[],[],[],[],[],[],[],[]
    res = cursor.fetchall()
    for row in res:
        PD.append(row[0])
        disease.append(row[1])
        caSeqNo.append(row[2])
        diagChecked.append(False if row[3] is None else row[3])
        treatChecked.append(False if row[4] is None else row[4])
        fuChecked.append(False if row[5] is None else row[5])
        pdConfirmed.append(False if row[6] is None else row[6])
        neoTreatChecked.append(False if row[7] is None else row[7])
        adjTreatChecked.append(False if row[8] is None else row[8])

    return JsonResponse({'PD':PD,'disease':disease,'caSeqNo':caSeqNo,'diagChecked':diagChecked,'treatChecked':treatChecked,'fuChecked':fuChecked,'pdConfirmed':pdConfirmed,'neoTreatChecked':neoTreatChecked,'adjTreatChecked':adjTreatChecked})

@csrf_exempt
def formGenerator(request):
    cursor = connections['practiceDB'].cursor()
    medType = request.POST.get('medType')
    diseaseId = request.POST.get('diseaseId')
    eventID = request.POST.get('eventID')
    print(eventID)

    '''---------------取得與medtype相對應的form格式id--------------'''
    getEventFactorID='''
    SELECT top(1) eventFactorCode
    FROM [practiceDB].[dbo].[eventFactorCode] as a
    inner join medTypeSet as b on a.groupNo=b.groupNo
    where medType=%s and diseaseID=%s
    '''
    cursor.execute(getEventFactorID,[medType,diseaseId])
    eventFactorID = cursor.fetchall()[0][0]

    '''---------------查詢有無紀錄--------------'''
    searchRecord = '''SELECT * FROM [practiceDB].[dbo].[extractedFactors] where eventID=%s'''
    cursor.execute(searchRecord,[eventID])
    recordedOrNot = len(cursor.fetchall())
    '''---------------取得大標題--------------'''
    if recordedOrNot !=0:
        mainSubjectQuery='''
        select eventFactorID,factorName,itemType,labeled,b.seq,dense_rank() OVER ( ORDER BY eventFactorID)-1 as dr
        from eventFactor as a
        left outer join  (select * from [extractedFactors] where eventID=%s) as b on a.eventFactorID=b.rootID
        where a.F_eventFactorID=0 and eventFactorCode=%s
        group by eventFactorID,factorName,itemType,labeled,b.seq
        '''
        cursor.execute(mainSubjectQuery,[eventID,eventFactorID])
    else:
        mainSubjectQuery='''
        select eventFactorID,factorName,itemType,labeled,b.seq,dense_rank() OVER ( ORDER BY eventFactorID)-1 as dr
        from eventFactor as a
        left outer join [extractedFactors] as b on a.eventFactorID=b.rootID
        where a.F_eventFactorID=0 and eventFactorCode=%s
        group by eventFactorID,factorName,itemType,labeled,b.seq
        '''
        cursor.execute(mainSubjectQuery,[eventFactorID])
    step = 1
    
    mainSubjectSet = cursor.fetchall()
    formObject = '<div class="formStructure">'
    num=0
    for ind1,mainSubject in enumerate(mainSubjectSet):

        step = 2

        if mainSubject[4] is None:
            seq = 1
        else:
            seq = mainSubject[4]
        
        formObject += f'<div data-prepareAdd=0 onmousedown="record()" class="mainBlock mainBlock{mainSubject[5]}" data-Seq={seq}>'
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
        
        formObject += '<ul>'
        for ind2,structure in enumerate(structureSet):
            num += 1


            type = structure[4].replace(' ','')
            stop = structure[7]
            if type=='text':
                formObject += f'''
                <li>
                    <input type=radio name="formStructure_[1]_[{ind1}][{structure[6]}]"  data-usage="text" id="item_{num}">
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
            print(type)
            factorID=structure[0]

            if stop != True:
                step = 3
                query =f'''
                select a{step}.*
                from eventFactor as a1 
                left outer join eventFactor as a2 on a1.F_eventFactorID=0 and a1.eventFactorID=a2.F_eventFactorID
                '''
                for i in range(step,step+1):
                    query +=f'''
                        left outer join eventFactor as a{i} on a{i-1}.F_eventFactorID<>0 and a{i-1}.eventFactorID=a{i}.F_eventFactorID
                    '''
                query +=f'where a2.eventFactorID is not null and a{i-1}.'
                query +='eventFactorID=%s'
                
                cursor.execute(query,[factorID])
                structureSet3 = cursor.fetchall()
                formObject += '<ul>'
                for structure3 in structureSet3:
                    stop = structure3[7]
                    num += 1
                    type = structure3[4].replace(' ','')
                    if type=='text':
                        formObject += f'''<li class="H_{stop}"><label for="item_{num}">{structure3[3]}：</label><input onclick="myFunction()" data-recorded=0 data-checked=0 type={type} data-eventFactorID={structure3[0]} name=formStructure_[1]_[{ind1}][{structure3[6]}] id="item_{num}"></li>'''
                    elif type=='NE':
                        formObject += f'''<li class="H_{stop}"><label for="item_{num}">{structure3[3]}</label></li>'''
                    elif type=='date':
                        formObject += f'''<li class="H_{stop}"><input onclick="myFunction()" data-recorded=0 data-checked=0 type={type} name=formStructure_[1]_[{ind1}][{structure3[6]}] data-eventFactorID={structure3[0]} id="item_{num}" value="{structure3[3]}"></li>'''
                    else:
                        formObject += f'''<li class="H_{stop}"><input onclick="myFunction()" data-recorded=0 data-checked=0 type={type} name=formStructure_[1]_[{ind1}][{structure3[6]}] data-eventFactorID={structure3[0]} id="item_{num}"><label for="item_{num}">{structure3[3]}</label></li>'''
                    
                    factorID=structure3[0]
                    if stop != True:
                        step = 4
                        query =f'''
                        select a{step}.*
                        from eventFactor as a1 
                        left outer join eventFactor as a2 on a1.F_eventFactorID=0 and a1.eventFactorID=a2.F_eventFactorID
                        '''
                        for i in range(step-1,step+1):
                            query +=f'''
                                left outer join eventFactor as a{i} on a{i-1}.F_eventFactorID<>0 and a{i-1}.eventFactorID=a{i}.F_eventFactorID
                            '''
                        query +=f'where a2.eventFactorID is not null and a{i-1}.'
                        query +='eventFactorID=%s'
                        cursor.execute(query,[factorID])
                        structureSet4 = cursor.fetchall()
                        formObject += '<ul>'
                        for structure4 in structureSet4:
                            stop = structure4[7]
                            num += 1
                            type = structure4[4].replace(' ','')
                            if type=='text':
                                formObject += f'''<li class="H_{stop}"><label for="item_{num}">{structure4[3]}：</label><input onclick="myFunction()" data-recorded=0 data-eventFactorID={structure4[0]} data-checked=0 type={type} name=formStructure_[1]_[{ind1}][{structure4[6]}] id="item_{num}"></li>'''
                            elif type=='NE':
                                formObject += f'''<li class="H_{stop}"><label for="item_{num}">{structure4[3]}</label></li>'''
                            else:
                                formObject += f'''<li class="H_{stop}"><input onclick="myFunction()" data-recorded=0 data-checked=0 type={type} data-eventFactorID={structure4[0]} name=formStructure_[1]_[{ind1}][{structure4[6]}] id="item_{num}"><label for="item_{num}">{structure4[3]}</label></li>'''
                            factorID=structure4[0]
                            if stop != True:
                                step = 5
                                query =f'''
                                select a{step}.*
                                from eventFactor as a1 
                                left outer join eventFactor as a2 on a1.F_eventFactorID=0 and a1.eventFactorID=a2.F_eventFactorID
                                '''
                                for i in range(step-2,step+1):
                                    query +=f'''
                                        left outer join eventFactor as a{i} on a{i-1}.F_eventFactorID<>0 and a{i-1}.eventFactorID=a{i}.F_eventFactorID
                                    '''
                                query +=f'where a2.eventFactorID is not null and a{i-1}.'
                                query +='eventFactorID=%s'
                                cursor.execute(query,[factorID])
                                structureSet5 = cursor.fetchall()
                                formObject += '<ul>'
                                for structure5 in structureSet5:
                                    stop = structure5[7]
                                    num += 1
                                    type = structure5[4].replace(' ','')
                                    if type=='text':
                                        formObject += f'''<li class="H_{stop}"><label for="item_{num}">{structure5[3]}：</label><input onclick="myFunction()" data-recorded=0 data-checked=0 type={type} data-eventFactorID={structure5[0]} name=formStructure_[1]_[{ind1}][{structure5[6]}] id="item_{num}"></li>'''
                                    elif type=='NE':
                                        formObject += f'''<li class="H_{stop}"><label for="item_{num}">{structure5[3]}</label></li>'''
                                    else:
                                        formObject += f'''<li class="H_{stop}"><input onclick="myFunction()" data-recorded=0 data-checked=0 type={type} name=formStructure_[1]_[{ind1}][{structure5[6]}] data-eventFactorID={structure5[0]} id="item_{num}"><label for="item_{num}">{structure5[3]}</label></li>'''
                                formObject += '</ul>'
                        formObject += '</ul>'
                
                formObject += '</ul>'
        formObject += '</ul>'
        formObject += '</div>'

    formObject += '</div>'
    return JsonResponse({'formObject':formObject})

@csrf_exempt
def insertExtractedFactors(request):
    cursor = connections['practiceDB'].cursor()
    eventID = request.POST.get('eventID')
    diseaseId = request.POST.get('diseaseId')
    insertSeqArray = request.POST.getlist('insertSeqArray[]')
    insertIDArray = request.POST.getlist('insertIDArray[]')
    insertValArray = request.POST.getlist('insertValArray[]')
    insertRootArray = request.POST.getlist('insertRootArray[]')
    insertRecordedArray = request.POST.getlist('insertRecordedArray[]')

    queryDelete='''delete from extractedFactors where eventID=%s'''
    cursor.execute(queryDelete,[eventID])
    
    query = '''select * from extractedFactors where eventID=%s and factorID=%s and seq=%s'''
    for factorID,factorValue,seq,root,Recorded in zip(insertIDArray,insertValArray,insertSeqArray,insertRootArray,insertRecordedArray):
        cursor.execute(query,[eventID,factorID,seq])
        if len(cursor.fetchall())==0: # =0, insert this data
            queryInsert='''insert into extractedFactors (eventID,factorID,factorValue,seq,rootID) VALUES(%s,%s,%s,%s,%s)'''
            cursor.execute(queryInsert,[eventID,factorID,factorValue,seq,root])
    return JsonResponse({})

@csrf_exempt
def searchExtractedFactorsRecord(request):
    cursor = connections['practiceDB'].cursor()
    eventID = request.POST.get('eventID')
    diseaseId = request.POST.get('diseaseId')
    seqArray = request.POST.getlist('seqArray[]')
    idArray = request.POST.getlist('idArray[]')
    classArray = request.POST.getlist('classArray[]')
    query='''select factorValue from extractedFactors where eventID=%s and factorID=%s and seq=%s'''
    factorIdRecorded = []
    factorValueRecorded = []
    seqRecorded = []
    classRecorded = []

    for factorId,seq,className in zip(idArray,seqArray,classArray):
        cursor.execute(query,[eventID,factorId,seq])
        result = cursor.fetchall()
        if len(result)!=0:
            seqRecorded.append(seq)
            classRecorded.append(className)
            factorIdRecorded.append(factorId)
            factorValueRecorded.append(result[0][0])

    return JsonResponse({'seqRecorded':seqRecorded,'classRecorded':classRecorded,'factorIdRecorded':factorIdRecorded,'factorValueRecorded':factorValueRecorded})