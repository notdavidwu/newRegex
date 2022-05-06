from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import pathlib

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
        select distinct a.ChartNo from I_Patient as a inner join I_AllExam_Test as b on a.ChartNo=b.ChartNo
        where ExecDate between '{partystart}'/*起始日期*/ and '{partyend}'/*終止日期*/ and MedType between 2131 and 2135--時間
        ) as a 
        inner join (
        select distinct a.ChartNo from I_Patient as a inner join I_AllExam_Test as b on a.ChartNo=b.ChartNo--Ward
        where Ward like '{ward}'
        ) as b on a.ChartNo=b.ChartNo
        inner join (
        select distinct a.ChartNo from I_Patient as a inner join I_AllExam_Test as b on a.ChartNo=b.ChartNo--Ward
        where Division like '{DivName}'
        ) as c on b.ChartNo=c.ChartNo
        inner join (
        select distinct a.ChartNo from I_Patient as a inner join I_AllExam_Test as b on a.ChartNo=b.ChartNo--Ward
        where MedType in(30401,30402,30403) --住院
        ) as d on c.ChartNo=d.ChartNo
        inner join (
        select distinct a.ChartNo from I_Patient as a inner join I_AllExam_Test as b on a.ChartNo=b.ChartNo--Ward
        where Attribute={bacterial} ---有菌
        ) as e on d.ChartNo=e.ChartNo
        order by ChartNo asc
    '''
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
    partystart = request.POST.get('partystart')
    partyend = request.POST.get('partyend')
    if hospitalized =='true':
        hospitalized_string = '2131,3132,2133,2134,2135,30402,30401,30403'
    else:
        hospitalized_string = '2131,3132,2133,2134,2135'
    query=f'''
    select * from(
    -----------------------------病床
    select a.*,b.TypeName,b.medTypeSource,b.eventCategory from I_AllExam_Test as a 
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
        select a.*,b.TypeName,b.medTypeSource,b.eventCategory from I_AllExam_Test as a 
        inner join medTypeSet as b on a.MedType=b.MedType
        where ChartNo={ChartNo}/**/　and a.MedType in(30901,30902)
        -----------------------------
    '''
    query +=f'''
    )as h
    where ExecDate between DATEADD(DAY,-3 ,('{partystart}'))/*起始日期*/ and DATEADD(DAY,+3 ,('{partyend}'))/*終止日期*/ 
    order by ExecDate asc
    '''
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
    TypeName = []
    cursor.execute(query)
    result = cursor.fetchall()

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
        TypeName.append(result[i][9])

    return JsonResponse({'ChartNo': ChartNo,'VisitNo': VisitNo,'OrderNo': OrderNo,'ItemNo': ItemNo,
                         'ExecDate':ExecDate,'ExecDateTime':ExecDateTime,'MedType':MedType,'TypeName':TypeName,'Attribute':Attribute,'Ward':Ward})

@csrf_exempt
def PrimaryText(request):
    OrderNo = request.POST.get('OrderNo')
    MedType = request.POST.get('MedType')
    ChartNo = request.POST.get('ChartNo')
    ExecDate = request.POST.get('ExecDate')
    ItemNo = request.POST.get('ItemNo')
    print(MedType)
    if MedType == '30801':
        query = '''select CreateTime,Content from ProgessionNote where ChartNo=%s and CONVERT(varchar(100), CreateTime, 23)=%s'''
        cursor = connections['AIC_Infection'].cursor()
        cursor.execute(query,[ChartNo,ExecDate])
        result = cursor.fetchall()
        ReportText = []
        CreateTime = []
        for i in range(len(result)):

            CreateTime.append(result[i][0].strftime("%Y-%m-%d %H:%M:%S"))
            ReportText.append(result[i][1])

        return JsonResponse({'ReportText': ReportText,'CreateTime':CreateTime})
    elif MedType in ['30901','30902']:
        query = '''select TubeName,BodyPosition,BodyPart,TubeLength,TubeStatus,TubeInsertion,RemovalTime,RemovalReason,TubeRemark from TubeUsage where TubeUsageNo=%s'''
        cursor = connections['AIC_Infection'].cursor()
        
        cursor.execute(query,[ItemNo])
        result = cursor.fetchall()
        object = f'''
        <tr class="table-secondary"><th >導管名稱 </th><th>是否為中心導管</th></tr>
        <tr><td>{result[0][0]} </td><td></td></tr>
        <tr class="table-secondary"><th>導管位置 </th><th>導管長度</th></tr>
        <tr><td>{result[0][1]}{result[0][2]} </td><td>{result[0][3]}</td></tr>
        <tr class="table-secondary"><th colspan="2">導管狀態</th></tr>
        <tr><td colspan="2" class="noMarginAndPadding">{result[0][4]}<br><br>A:使用中 D:已刪除 R:已拔除</td></tr>
        <tr class="table-secondary"><th>置入時間 </th><th>停用/取出時間</th></tr>
        <tr><td>{result[0][5]} </td><td>{result[0][6]}</td></tr>
        <tr class="table-secondary"><th colspan="2">導管停用/取出原因 </th></tr>
        <tr><td colspan="2">{result[0][7]}</td></tr>
        <tr class="table-secondary"><th colspan="2">標註 </th></tr>
        <tr><td class="TubeRemark" colspan="2">{result[0][8]}</td></tr>
        '''
        return JsonResponse({'object': object})
    else:
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

    queryExamItem='''
        select * from ReportContent(%s,1278,1259)
        union all
        select * from ReportContent(%s,1259,109)
    '''
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
def getWard(request):
    cursor = connections['AIC_Infection'].cursor()
    query='''select Ward from Bed group by Ward order by Ward'''
    cursor.execute(query)
    fetchallWard = cursor.fetchall()
    ward = []
    for res in fetchallWard:
        ward.append(res[0])
    return JsonResponse({'ward': ward})

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