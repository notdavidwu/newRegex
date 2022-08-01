from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import pathlib
import pandas as pd

@csrf_exempt
def Search(request):
    au = request.session.get('au')
    return render(request, 'Search/Search.html',{'au':au})

@csrf_exempt
def PoolList(request):
    partystart=request.POST.get('partystart')
    partyend=request.POST.get('partyend')
    hospitalized=request.POST.get('hospitalized')
    bacterial=request.POST.get('bacterial')
    ward=request.POST.get('ward')
    DivName=request.POST.get('DivName')
    query = f'''
        select distinct a.ChartNo  from (
        select distinct a.ChartNo from I_Patient as a inner join I_AllExam_Test0419 as b on a.ChartNo=b.ChartNo
        where ExecDate between '{partystart}'/*起始日期*/ and '{partyend}'/*終止日期*/ and MedType between 2131 and 2135--時間
        ) as a 
        inner join (
        select distinct a.ChartNo from I_Patient as a inner join I_AllExam_Test0419 as b on a.ChartNo=b.ChartNo--Ward
        where locationnow like '{ward}' and ExecDate between '{partystart}'/*起始日期*/ and '{partyend}'/*終止日期*/
        ) as b on a.ChartNo=b.ChartNo
        inner join (
        select distinct a.ChartNo from I_Patient as a inner join I_AllExam_Test0419 as b on a.ChartNo=b.ChartNo--Ward
        where Division like '{DivName}'
        ) as c on b.ChartNo=c.ChartNo
        inner join (
        select distinct a.ChartNo from I_Patient as a inner join I_AllExam_Test0419 as b on a.ChartNo=b.ChartNo--Ward
        where locationnow is not null and ExecDate between '{partystart}'/*起始日期*/ and '{partyend}'/*終止日期*/--住院
        ) as d on c.ChartNo=d.ChartNo
        inner join (
        select distinct a.ChartNo from I_Patient as a inner join I_AllExam_Test0419 as b on a.ChartNo=b.ChartNo--Ward
        where Attibute={bacterial} and ExecDate between '{partystart}'/*起始日期*/ and '{partyend}'/*終止日期*/ ---有菌
        ) as e on d.ChartNo=e.ChartNo
        order by ChartNo asc
    '''
    print(query)
    cursor = connections['AIC_Infection'].cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    ChartNo=[]
    for row in result:
        ChartNo.append(row[0])
    return JsonResponse({'ChartNo': ChartNo})

@csrf_exempt
def TimeShow(request):
    ChartNo = request.POST.get('ChartNo')
    careRecordCheck = request.POST.get('careRecordCheck')
    hospitalized = request.POST.get('hospitalized')
    tubeCheck = request.POST.get('tubeCheck')
    bodycheck = request.POST.get('bodycheck')
    partystart = request.POST.get('partystart')
    partyend = request.POST.get('partyend')
    print(bodycheck)
    if hospitalized =='true':
        hospitalized_string = '2131,2132,2133,2134,2135,30402,30401,30403'
    else:
        hospitalized_string = '2131,2132,2133,2134,2135'
    query=f'''
    select distinct ChartNo,h.VisitNo,OrderNo,ItemNo,ExecDate,h.MedType,Ward,Division,Attibute,locationnow,TypeName,medTypeSource,eventCategory,i.ReportID '''
    if bodycheck=='true':
        query +=f''',BT,BP,PULSE,SPO2 '''
    
    query +=f'''from(
    -----------------------------病床
    select a.*,b.TypeName,b.medTypeSource,b.eventCategory from I_AllExam_Test0419 as a 
    inner join medTypeSet as b on a.MedType=b.MedType
    where ChartNo={ChartNo}/**/ and a.MedType in({hospitalized_string})
    '''
    if careRecordCheck =='true':
        query +=f'''
        -----------------------------護理
        union all
        select a.*,b.TypeName,b.medTypeSource,b.eventCategory from threedayprogression({ChartNo}/**/)as a 
        inner join medTypeSet as b on a.MedType=b.MedType
    '''
    if tubeCheck=='true':
        query +=f'''
        -----------------------------導管
        union all
        select a.*,b.TypeName,b.medTypeSource,b.eventCategory from I_AllExam_Test0419 as a 
        inner join medTypeSet as b on a.MedType=b.MedType
        where ChartNo={ChartNo}/**/ and a.MedType in(30903)
        -----------------------------
    '''
    if bodycheck=='true':
        query +=f'''
        -----------------------------異常生理評值
        union all
        select a.*,b.TypeName,b.medTypeSource,b.eventCategory from I_AllExam_Test0419 as a 
        inner join medTypeSet as b on a.MedType=b.MedType
        where ChartNo={ChartNo}/**/ and a.MedType in(30501)
        -----------------------------
    '''
    query +=f'''
    )as h
    left join AnalyseText as i on h.OrderNo=i.ReportNo '''
    if bodycheck =='true':
        query +=f'''
        left join
		(
            select * from bodycheck({ChartNo})
		)as j on h.ExecDate=j.OccurDate
    '''
    if partystart != '':
        query +=f'''
        where ExecDate between DATEADD(DAY,-3 ,('{partystart}'))/*起始日期*/ and DATEADD(DAY,+3 ,('{partyend}'))/*終止日期*/ 
        '''
    query +=f'''order by ExecDate asc'''
    if bodycheck=='true':
        query +=f''',BT DESC,BP DESC,PULSE DESC ,SPO2 DESC'''
    print(query)
    cursor = connections['AIC_Infection'].cursor()
    ChartNo=[]
    VisitNo = []
    OrderNo = []
    ItemNo = []
    ExecDate = []
    ExecDateTime = []
    MedType = []
    Ward = []
    Division=[]
    Attribute = []
    locationnow = []
    TypeName = []
    cursor.execute(query)
    result = cursor.fetchall()
    BT=[]
    BP=[]
    PULSE=[]
    SPO2=[]
    bodychecker=[]
    for i in range(len(result)):
        ChartNo.append(result[i][0])
        VisitNo.append(result[i][1])
        OrderNo.append(result[i][2])
        ItemNo.append(result[i][3])
        ExecDate.append(result[i][4].date())
        ExecDateTime.append(result[i][4].replace(microsecond=0).time())
        MedType.append(result[i][5])
        Ward.append(result[i][6])
        Division.append(result[i][7])
        Attribute.append(result[i][8])
        locationnow.append(result[i][9])
        TypeName.append(result[i][10])
        if bodycheck =='true':
            bodychecker.append('1')
            if result[i][14]==None:
                BT.append(' ')
            else:
                BT.append(result[i][14])
            if result[i][15]==None:
                BP.append(' ')
            else:
                BP.append(result[i][15])
            if result[i][16]==None:
                PULSE.append(' ')
            else:
                PULSE.append(result[i][16])
            if result[i][17]==None:
                SPO2.append(' ')
            else:
                SPO2.append(result[i][17])
    print(bodychecker)
    if bodycheck =='true':
        return JsonResponse({'ChartNo': ChartNo,'VisitNo': VisitNo,'OrderNo': OrderNo,'ItemNo': ItemNo,
                         'ExecDate':ExecDate,'ExecDateTime':ExecDateTime,'MedType':MedType,'TypeName':TypeName,
                         'Attribute':Attribute,'Ward':Ward,'locationnow':locationnow,'BP':BP,'BT':BT,'PULSE':PULSE,'SPO2':SPO2,'bodychecker':bodychecker})
    else:
        return JsonResponse({'ChartNo': ChartNo,'VisitNo': VisitNo,'OrderNo': OrderNo,'ItemNo': ItemNo,
                         'ExecDate':ExecDate,'ExecDateTime':ExecDateTime,'MedType':MedType,'TypeName':TypeName,
                         'Attribute':Attribute,'Ward':Ward,'locationnow':locationnow})
    
    

@csrf_exempt
def PrimaryText(request):
    OrderNo = request.POST.get('OrderNo')
    MedType = request.POST.get('MedType')
    ChartNo = request.POST.get('ChartNo')
    ExecDate = request.POST.get('ExecDate')
    ItemNo = request.POST.get('ItemNo')
    print(MedType)
    if MedType == '30801': #點擊護理紀錄
        query = '''select top 20 CreateTime,Content from ProgessionNote where ChartNo=%s and CONVERT(varchar(100), CreateTime, 23)=%s
        '''#order by CreateTime
        cursor = connections['AIC_Infection'].cursor()
        cursor.execute(query,[ChartNo,ExecDate])
        result = cursor.fetchall()
        ReportText = []
        CreateTime = []
        for i in range(len(result)):

            CreateTime.append(result[i][0].strftime("%Y-%m-%d %H:%M:%S"))
            ReportText.append(result[i][1])

        return JsonResponse({'ReportText': ReportText,'CreateTime':CreateTime})
    elif MedType in ['99999']:#點擊管路細節
        query = '''select TubeName,BodyPosition,BodyPart,TubeLength,TubeStatus,TubeInsertion,RemovalTime,RemovalReason,TubeRemark,TubeUsageNo,IsCenter,TubeUnit from TubeUsage where TubeUsageNo=%s'''
        cursor = connections['AIC_Infection'].cursor()
        
        cursor.execute(query,[OrderNo])
        result = cursor.fetchall()
        object = f'''
        <tr class="table-info" ><th colspan="2">導管名稱 </th><th  colspan="2">中心導管(1/0)</th></tr>
        <tr class="table-light"><td  colspan="2">{result[0][0].replace(' ','')}<br>({result[0][9]}) </td><td  colspan="2">{result[0][10]}</td></tr>
        <tr class="table-info"><th  colspan="2">導管位置 </th><th  colspan="2">導管長度</th></tr>
        <tr class="table-light"><td  colspan="2">{result[0][1]}{result[0][2]} </td><td  colspan="2">{result[0][3]}{result[0][11]}</td></tr>
        <tr class="table-info"><th colspan="4">導管狀態</th></tr>
        <tr class="table-light"><td colspan="4" class="noMarginAndPadding">{result[0][4]}<br><br>A:使用中 D:已刪除 R:已拔除</td></tr>
        <tr class="table-info"><th  colspan="2">置入時間 </th><th  colspan="2">停用/取出時間</th></tr>
        <tr class="table-light"><td  colspan="2">{result[0][5]} </td><td  colspan="2">{result[0][6]}</td></tr>
        <tr class="table-info"><th colspan="4">導管停用/取出原因 </th></tr>
        <tr class="table-light"><td colspan="4">{result[0][7]}</td></tr>
        <tr class="table-info"><th colspan="4">標註 </th></tr>
        <tr class="table-light"><td class="TubeRemark" colspan="4">{result[0][8]}</td></tr>
        '''
        return JsonResponse({'object': object})
    elif MedType in ['30903']:#點擊管路
        print(MedType)
        query = '''select *,30901 as 'MedType' from TubeUsage as a inner join medTypeSet as b on b.MedType=30901
        where ChartNo=%s/**/ and convert(date,TubeInsertion)=convert(date,%s)
        UNION ALL
        select *,30902 as 'MedType' from TubeUsage as a inner join medTypeSet as b on b.MedType=30902
        where ChartNo=%s/**/ and  convert(date,RemovalTime)=convert(date,%s)
        order by b.MedType,TubeInsertion asc
        '''
        cursor = connections['AIC_Infection'].cursor()
        TubeUsageNo = []
        TubeInsertion = []
        TubeInsertionTime = []
        RemovalTime = []
        RemovalTimeTime = []
        TubeName = []
        IsCenter = []
        MedType = []
        cursor.execute(query,[ChartNo,ExecDate,ChartNo,ExecDate])
        result = cursor.fetchall()
        for i in range(len(result)):
            TubeUsageNo.append(result[i][5])
            TubeInsertion.append(result[i][6].date())
            TubeInsertionTime.append(result[i][6].replace(microsecond=0).time())
            RemovalTime.append(result[i][7].date())
            RemovalTimeTime.append(result[i][7].replace(microsecond=0).time())
            TubeName.append(result[i][9])
            IsCenter.append(result[i][18])
            MedType.append(result[i][19])
        
        return JsonResponse({'TubeUsageNo': TubeUsageNo,'TubeInsertion': TubeInsertion,'RemovalTime': RemovalTime,'IsCenter': IsCenter,
                            'MedType':MedType,'TubeInsertionTime':TubeInsertionTime,'RemovalTimeTime':RemovalTimeTime,'TubeName':TubeName})
    elif MedType in ['30501']:#點擊異常生理評值
        print(MedType)
        query = '''
        select *
        from (
            select a.VisitNo,OccurDate,Value,concat(Value1,' ',Unit1) as 'BT'
            from HIS.HealthCare.dbo.NursingEventData as a inner join HIS.HealthCare.dbo.VisitRecord as b on a.VisitNo=b.VisitNo
            where  EventType like '%BT%'and ChartNo='''+ ChartNo +''' and VisitZone='A'
            and Value1>38.00
        )as a 
        left join (
            select a.VisitNo,OccurDate,Value,concat(Value1,' / ',Value2,' ',Unit2) as 'BP'
            from HIS.HealthCare.dbo.NursingEventData as a inner join HIS.HealthCare.dbo.VisitRecord as b on a.VisitNo=b.VisitNo
            where  EventType like '%BP%'and ChartNo='''+ ChartNo +''' and VisitZone='A'
        )as b on a.VisitNo=b.VisitNo and DATEDIFF(hh,a.OccurDate,b.OccurDate)between -1 and 1
        left join (
            select a.VisitNo,OccurDate,Value,concat(Value1,' ',Unit1) as 'PULSE'
            from HIS.HealthCare.dbo.NursingEventData as a inner join HIS.HealthCare.dbo.VisitRecord as b on a.VisitNo=b.VisitNo
            where  EventType like '%PULSE%'and ChartNo='''+ ChartNo +''' and VisitZone='A'
        )as c on a.VisitNo=c.VisitNo and DATEDIFF(hh,a.OccurDate,c.OccurDate)between -1 and 1
        left join (
            select a.VisitNo,OccurDate,Value,concat(Value1,' ',Unit1) as 'SPO2'
            from HIS.HealthCare.dbo.NursingEventData as a inner join HIS.HealthCare.dbo.VisitRecord as b on a.VisitNo=b.VisitNo
            where  EventType like '%SPO2%'and ChartNo='''+ ChartNo +''' and VisitZone='A'
        )as d on a.VisitNo=c.VisitNo and DATEDIFF(hh,a.OccurDate,d.OccurDate)between -1 and 1
        where a.OccurDate=\''''+ ExecDate +'''\'
        order by a.OccurDate,b.OccurDate,c.OccurDate,d.OccurDate asc
        '''
        print(query)
        cursor = connections['AIC_Infection'].cursor()
        VisitNo = []
        OccurDate = []
        BT = []
        BP = []
        PULSE = []
        SPO2 = []
        cursor.execute(query)
        result = cursor.fetchall()
        for i in range(len(result)):
            VisitNo.append(result[i][0])
            OccurDate.append(result[i][1])
            BT.append(result[i][3])
            BP.append(result[i][7])
            PULSE.append(result[i][11])
            SPO2.append(result[i][15])
        
        return JsonResponse({'VisitNo': VisitNo,'OccurDate': OccurDate,'BT': BT,'BP': BP,
                            'PULSE':PULSE,'SPO2':SPO2})
    
    else:#點擊檢驗報告
        query = '''select * from AnalyseText where ReportNo ='''+OrderNo
        cursor = connections['AIC_Infection'].cursor()
        ReportID=[]
        CategoryNo = []
        ReportNo = []
        MedType = []
        ReportText = []
        Analysed = []
        cursor.execute(query)
        result = cursor.fetchall()
        for i in range(len(result)):
            ReportID.append(result[i][0])
            CategoryNo.append(result[i][1])
            ReportNo.append(result[i][2])
            MedType.append(result[i][3])
            ReportText.append(result[i][4])
            Analysed.append(result[i][5])
        
        return JsonResponse({'ReportID': ReportID,'CategoryNo': CategoryNo,'ReportNo': ReportNo,'MedType': MedType,
                            'ReportText':ReportText,'Analysed':Analysed})      
        

@csrf_exempt
def structureData(request):
    ReportID = str(request.POST.get('ReportID')).replace(' ','')

    cursor = connections['AIC_Infection'].cursor()

    queryCheck='''
        select top 1 a.ReportID--,Block,Resistance1w,Resistance1n,Resistance2w,Resistance2n,Resistance3w,Resistance3n,drug 
        from 
        DrugResistance_AnalyseText as a inner join AnalyseText as b on a.ReportID=b.ReportID where a.ReportID=%s
    '''
    cursor.execute(queryCheck,[ReportID])
    check = cursor.fetchall()

    queryExamItem='''select * from ReportContentTable where ReportID=%s and State=1 order by PosStart'''
    cursor.execute(queryExamItem,[ReportID,ReportID])
    resExamItem = cursor.fetchall()

    ExamItem = resExamItem[0][3].replace('EndLine','')
    ExamItemText =  resExamItem[0][5]

    ExamSource = resExamItem[1][3]
    ExamSourceText = resExamItem[1][5]



    if len(check) != 0 :
        queryBacteria='''
            select ReportID,Block,Item,Token2 from Bacteria(%s)
        '''
        cursor.execute(queryBacteria,[ReportID])
        resBacteria = cursor.fetchall()
        Bacteria=[]
        for res in resBacteria:
            Bacteria.append(res[3].replace('[space]',' '))
        queryResistance='''
            select a.ReportID,Block,Resistance1w,Resistance1n,Resistance2w,Resistance2n,Resistance3w,Resistance3n,drug from 
	        DrugResistance_AnalyseText as a inner join AnalyseText as b on a.ReportID=b.ReportID where a.ReportID=%s order by Block ASC
        '''
        cursor.execute(queryResistance,[ReportID])
        resResistance = cursor.fetchall()
        Resistance1w=[]
        Resistance1n=[]
        Resistance2w=[]
        Resistance2n=[]
        Resistance3w=[]
        Resistance3n=[]
        drag=[]
        for res in resResistance:
            Resistance1w.append(res[2].replace(' ',''))
            Resistance1n.append(res[3].replace(' ',''))
            Resistance2w.append(res[4].replace(' ',''))
            Resistance2n.append(res[5].replace(' ',''))
            Resistance3w.append(res[6].replace(' ',''))
            Resistance3n.append(res[7].replace(' ',''))
            drag.append(res[8].replace(' ',''))

            #Resistance.append(res[3].replace('[space]',' '))
        
        return JsonResponse({
            'check':len(check),
            'ReportID':ReportID,
            'ExamItem':ExamItem,
            'ExamItemText':ExamItemText,
            'ExamSource':ExamSource,
            'ExamSourceText':ExamSourceText,
            'Bacteria':Bacteria,
            'Resistance1w':Resistance1w,
            'Resistance1n':Resistance1n,
            'Resistance2w':Resistance2w,
            'Resistance2n':Resistance2n,
            'Resistance3w':Resistance3w,
            'Resistance3n':Resistance3n,
            'drag':drag
        })
    else:
        queryReportContentBack = '''select ReportContentBack from ReportContentBack(%s)'''
        cursor.execute(queryReportContentBack,[ReportID])
        resBacteria = cursor.fetchall()
        Bacteria=[]
        for res in resBacteria:
            Bacteria.append(res[0])
        return JsonResponse({
            'check':len(check),
            'ReportID':ReportID,
            'ExamItem':ExamItem,
            'ExamItemText':ExamItemText,
            'ExamSource':ExamSource,
            'ExamSourceText':ExamSourceText,
            'Bacteria':Bacteria,
        })
@csrf_exempt
def structureDatatest(request):
   
    ReportID = str(request.POST.get('ReportID')).replace(' ','')
    
    cursor = connections['AIC_Infection'].cursor()
    queryExamItem='''select * from ReportContentTable where ReportID=%s and State=1 order by PosStart'''
    #print(ReportID)
        
    ExamItem = []
    ExamItemText = []
    Category = []
    cursor.execute(queryExamItem,[ReportID])
    
    result = cursor.fetchall()
    
    for i in range(len(result)):
        ExamItem.append(result[i][3].replace('EndLine',''))
        ExamItemText.append(result[i][5])
        Category.append(result[i][8])
    queryBacteria='''
        select *,null as 'Token1',null as 'Token2',1 as 'State'  from DrugResistance_AnalyseText_test0408 where ReportID = %s/**/
        union 
        select qq,ReportID,Block,PosStart1,null,null,null,null,null,null,null,Token1,Token2,State from BacteriaTable where ReportID = %s /*47424*/ and State = 1
        order by PosStart,Ordery asc
    '''
    cursor.execute(queryBacteria,[ReportID,ReportID])
    resBacteria = cursor.fetchall()

    Resistance1w=[]
    Resistance1n=[]
    Resistance2w=[]
    Resistance2n=[]
    Resistance3w=[]
    Resistance3n=[]
    drug=[]
    Bacteria=[]
    state=[]
    for i in range(len(resBacteria)):
        Resistance1w.append(resBacteria[i][4])
        Resistance1n.append(resBacteria[i][5])
        Resistance2w.append(resBacteria[i][6])
        Resistance2n.append(resBacteria[i][7])
        Resistance3w.append(resBacteria[i][8])
        Resistance3n.append(resBacteria[i][9])
        drug.append(resBacteria[i][10])
        Bacteria.append(resBacteria[i][12])
        state.append(resBacteria[i][13])
    
    return JsonResponse({
        'ReportID':ReportID,
        'ExamItem':ExamItem,
        'ExamItemText':ExamItemText,
        'Category':Category,

        'Resistance1w':Resistance1w,
        'Resistance1n':Resistance1n,
        'Resistance2w':Resistance2w,
        'Resistance2n':Resistance2n,
        'Resistance3w':Resistance3w,
        'Resistance3n':Resistance3n,
        'drug':drug,
        'Bacteria':Bacteria,
        'state':state
    })


@csrf_exempt        
def getWard(request):
    cursor = connections['AIC_Infection'].cursor()
    query='''select Ward from Bed group by Ward order by Ward'''
    cursor.execute(query)
    fetchallWard = cursor.fetchall()
    ward = []
    for res in fetchallWard:
        ward.append(res[0])
    return JsonResponse({'ward': ward})
    print(11111)

@csrf_exempt        
def getDivName(request):
    cursor = connections['AIC_Infection'].cursor()
    query='''select DivName from  Division group by DivName'''
    cursor.execute(query)
    fetchallDivName = cursor.fetchall()
    DivName = []
    for res in fetchallDivName:
        DivName.append(res[0])
    return JsonResponse({'DivName': DivName})

@csrf_exempt        
def getCategory(request):
    cursor = connections['AIC_Infection'].cursor()
    query='''select Category from  Infection_Conversion_Category order by Category'''
    cursor.execute(query)
    fetchallDivName = cursor.fetchall()
    Category = []
    for res in fetchallDivName:
        Category.append(res[0])
    return JsonResponse({'Category': Category})

@csrf_exempt        
def deletebacteria(request):
    bacName = str(request.POST.get('bacName')).strip()#request.POST.get('bacName')
    print(bacName)
    query='''update BacteriaTable set State=0 where 
    LTRIM(RTRIM(REPLACE(REPLACE(REPLACE(Token2, CHAR(10), CHAR(32)),CHAR(13), CHAR(32)),CHAR(9), CHAR(32))))=%s'''
    cursor = connections['AIC_Infection'].cursor()
    cursor.execute(query,[bacName])  
    print(query) 
    return JsonResponse({})    
    
@csrf_exempt        
def recoverybacteria(request):
    bacName = str(request.POST.get('bacName')).strip()#request.POST.get('bacName')
    print(bacName)
    query='''update BacteriaTable set State=1 where 
    LTRIM(RTRIM(REPLACE(REPLACE(REPLACE(Token2, CHAR(10), CHAR(32)),CHAR(13), CHAR(32)),CHAR(9), CHAR(32))))=%s'''
    cursor = connections['AIC_Infection'].cursor()
    cursor.execute(query,[bacName])  
    print(query) 
    return JsonResponse({})    
    
@csrf_exempt        
def bodyevaluate(request):
    ChartNo ='18892'
    print(ChartNo)
    query='''
    select *
    from (
        select a.VisitNo,OccurDate,Value,concat(Value1,' ',Unit1) as 'BT'
        from HIS.HealthCare.dbo.NursingEventData as a inner join HIS.HealthCare.dbo.VisitRecord as b on a.VisitNo=b.VisitNo
        where  EventType like '%BT%'and ChartNo='''+ ChartNo +'''and VisitZone='A'
        and Value1>38.00
    )as a 
    left join (
        select a.VisitNo,OccurDate,Value,concat(Value1,' / ',Value2,' ',Unit2) as 'BP'
        from HIS.HealthCare.dbo.NursingEventData as a inner join HIS.HealthCare.dbo.VisitRecord as b on a.VisitNo=b.VisitNo
        where  EventType like '%BP%'and ChartNo='''+ ChartNo +''' and VisitZone='A'
    )as b on a.VisitNo=b.VisitNo and DATEDIFF(hh,a.OccurDate,b.OccurDate)between -1 and 1
    left join (
        select a.VisitNo,OccurDate,Value,concat(Value1,' ',Unit1) as 'PULSE'
        from HIS.HealthCare.dbo.NursingEventData as a inner join HIS.HealthCare.dbo.VisitRecord as b on a.VisitNo=b.VisitNo
        where  EventType like '%PULSE%'and ChartNo='''+ ChartNo +''' and VisitZone='A'
    )as c on a.VisitNo=c.VisitNo and DATEDIFF(hh,a.OccurDate,c.OccurDate)between -1 and 1
    left join (
        select a.VisitNo,OccurDate,Value,concat(Value1,' ',Unit1) as 'SPO2'
        from HIS.HealthCare.dbo.NursingEventData as a inner join HIS.HealthCare.dbo.VisitRecord as b on a.VisitNo=b.VisitNo
        where  EventType like '%SPO2%'and ChartNo='''+ ChartNo +''' and VisitZone='A'
    )as d on a.VisitNo=c.VisitNo and DATEDIFF(hh,a.OccurDate,d.OccurDate)between -1 and 1
    order by a.OccurDate asc
    '''
    cursor = connections['AIC_Infection'].cursor()
    cursor.execute(query)  
    fetchallbody = cursor.fetchall()
    temperature = []
    print(query)
    for res in range(len(fetchallbody)):
        temperature.append(fetchallbody[res][2])
    return JsonResponse({'temperature': temperature})  
    
@csrf_exempt        
def commensals(request):
    Bacteria = str(request.POST.get('Bacteria'))
    print(Bacteria)
    query='''select * from Commensals where Commensals like '%'''+Bacteria+'''%'
    '''
    cursor = connections['AIC_Infection'].cursor()
    cursor.execute(query)  
    fetchallcommensals = cursor.fetchall()
    iscommensals = []
    print(query)
    for res in range(len(fetchallcommensals)):
        iscommensals.append(fetchallcommensals[res][0])
    return JsonResponse({'iscommensals': iscommensals})  


@csrf_exempt        
def test(request):
    def load_csv_data(file):
        return pd.read_csv(file)
    births=load_csv_data('https://archive.ics.uci.edu/ml/'
                        'machine-learning-databases/adult/adult.data')
    print(births)
