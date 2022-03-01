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
    query = '''
    select distinct a.ChartNo--,b.Ward 
    from (
        select distinct ChartNo--a.*,b.*,c.* 
        from AnalyseText as a inner join ExecTime as b on a.ReportNo=b.OrderNo 
        left join BedRecord as c on b.VisitNo=c.VisitNo
        left join(
            select distinct ReportNo from AnalyseText as a inner join TextToken as b on a.ReportID=b.ReportID
            inner join ontologyTrans as c on b.TokenID=c.TokenID
            where  PosStart>0 and b.TokenID=2507
        )as d on b.OrderNo=d.ReportNo
        where ExecTime >= %s and ExecTime < %s
    '''
    
    if hospitalized=='true':
        query +=''' and ExecTime<c.EndTime and ExecTime>StartTime'''
    if bacterial=='true':
        query +=''' and d.ReportNo is not null'''

    query += ') as a inner join I_AllExam as b on a.ChartNo=b.ChartNo'

    if ward != '不限':
        query +=" where b.Ward = '"+ward+"'"
        if DivName != '不限':
            query +=" and b.Division = '"+DivName+"'"
    else :
        if DivName != '不限':
            query +=" where b.Division = '"+DivName+"'"

    query +=''' and a.ChartNo<99999990  order by a.ChartNo'''

    cursor = connections['AIC_Infection'].cursor()

    ChartNo=[]
    cursor.execute(query,[partystart,partyend])
    result = cursor.fetchall()

    for i in range(len(result)):
        ChartNo.append(result[i][0])

    return JsonResponse({'ChartNo': ChartNo})

@csrf_exempt
def TimeShow(request):
    ChartNo = request.POST.get('ChartNo')
    careRecordCheck = request.POST.get('careRecordCheck')
    query = '''select a.*,b.TypeName from I_AllExam as a inner join medTypeSet as b on a.MedType=b.MedType where a.MedType in(2134,2133'''
    print(careRecordCheck)
    if careRecordCheck =='true':
        query +=''',30801'''
    
    query +=''') and a.ChartNo='''+ChartNo+''' order by a.ChartNo,a.ExecDate asc '''
    print(query)
    cursor = connections['AIC_Infection'].cursor()
    ChartNo=[]
    VisitNo = []
    OrderNo = []
    ItemNo = []
    ExecDate = []
    MedType = []
    TypeName = []
    cursor.execute(query)
    result = cursor.fetchall()

    for i in range(len(result)):
        print((result[i]))
        ChartNo.append(result[i][0])
        VisitNo.append(result[i][1])
        OrderNo.append(result[i][2])
        ItemNo.append(result[i][3])
        ExecDate.append(result[i][4])
        MedType.append(result[i][5])
        TypeName.append(result[i][8])

    return JsonResponse({'ChartNo': ChartNo,'VisitNo': VisitNo,'OrderNo': OrderNo,'ItemNo': ItemNo,
                         'ExecDate':ExecDate,'MedType':MedType,'TypeName':TypeName})

@csrf_exempt
def PrimaryText(request):
    OrderNo = request.POST.get('OrderNo')
    MedType = request.POST.get('MedType')
    ChartNo = request.POST.get('ChartNo')
    ExecDate = request.POST.get('ExecDate')
    print(MedType !='30801')
    if MedType !='30801':
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
    else:
        query = '''select * from ProgessionNote where ChartNo=%s and CONVERT(varchar(100), CreateTime, 23)=%s'''
        cursor = connections['AIC_Infection'].cursor()
        cursor.execute(query,[ChartNo,ExecDate])
        result = cursor.fetchall()
        ReportText=[]
        
        for i in range(len(result)):
            ReportText.append(result[i][4])
        print(ReportText)
        return JsonResponse({'ReportText': ReportText})

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
    print(len(check))
    print(len(check) != 0)
    queryExamItem='''
        select * from ReportContent(%s,1278,1259)
        union all
        select * from ReportContent(%s,1259,109)
    '''
    cursor.execute(queryExamItem,[ReportID,ReportID])
    resExamItem = cursor.fetchall()
    print(len(resExamItem))
    ExamItem = resExamItem[0][3].replace('EndLine','')
    ExamItemText =  resExamItem[0][5]
    print(ExamItemText)
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
            print(res[0])
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
    query='''select Ward from Bed group by Ward'''
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