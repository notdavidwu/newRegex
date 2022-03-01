from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect

def tube2(request):
    au = request.session.get('au')
    return render(request, 'tube2/tube2.html',{'au':au})

@csrf_exempt
def TextReport(request):
    PID=request.POST.get('PID')
    query = '''select ExecTime,ReportText  from ExamList where ChartNo='''+str(PID)
    cursor = connections['AICH'].cursor()
    cursor.execute(query)
    examDate=[]
    examReport=[]
    exam = cursor.fetchall()
    for i in range(len(exam)):
        examDate.append(str(exam[i][0]).split(' ')[0])
        examReport.append(exam[i][1])

    return JsonResponse({'examDate': examDate, 'examReport': examReport})

@csrf_exempt
def sql12(request):
    query = 'SELECT * FROM t1169$ where Times>1 ORDER BY 1 ASC'
    cursor = connections['TUBE'].cursor()
    cursor.execute(query)
    exam = cursor.fetchall()
    No=[]
    TubeName=[]
    Times=[]

    query2 = "select a.TubeNo,b.TubeNo as 'bTubeNo',b.TubeName,c.No from TUBE as a inner join　TUBE as b on a.F_TubeNo=b.TubeNo inner join t52$ as c on b.TubeNo=c.TubeNo where a.Category=3 and b.Category=1 order by 1 asc"
    cursor = connections['TUBE'].cursor()
    cursor.execute(query2)
    exam2 = cursor.fetchall()
    TubeNo=[]
    bTubeNo=[]
    TubeNamecheck=[]
    CNocheck=[]

    query3 = "select * from t52$ where No<>0 order by 1 asc"
    cursor = connections['TUBE'].cursor()
    cursor.execute(query3)
    exam3 = cursor.fetchall()
    No52=[]
    TubeNo52=[]
    TubeName52=[]
    for i in range(len(exam)):
        No.append(exam[i][0])
        TubeName.append(str(exam[i][1]))
        Times.append(exam[i][2])

    for i in range(len(exam2)):
        TubeNo.append(exam2[i][0])
        bTubeNo.append(exam2[i][1])
        TubeNamecheck.append(str(exam2[i][2]))
        CNocheck.append(exam2[i][3])

    for i in range(len(exam3)):
        No52.append(exam3[i][0])
        TubeNo52.append(exam3[i][1])
        TubeName52.append(str(exam3[i][2]))

    return JsonResponse({'No1169': No, 'TubeName1169': TubeName, 'Times1169': Times, 'TubeNocheck12': TubeNo, 'bTubeNocheck12': bTubeNo, 'TubeNamecheck12': TubeNamecheck, 'CNocheck': CNocheck, 'No52': No52, 'TubeNo52': TubeNo52, 'TubeName52': TubeName52})

@csrf_exempt
def sqlupdate(request):
    TubeNo=request.POST.get('TubeNo')
    F_TubeNo = request.POST.get('F_TubeNo')
    query = 'UPDATE TUBE SET F_TubeNo='+F_TubeNo+ 'WHERE Category=3 and TubeNo='+TubeNo
    cursor = connections['TUBE'].cursor()
    cursor.execute(query)

    return JsonResponse({})

