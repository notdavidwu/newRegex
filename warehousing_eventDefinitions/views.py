
from cv2 import resize
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import numpy as np
import re
@csrf_exempt
def eventDefinitions(request):
    au = request.session.get('au')
    
    if not request.user.is_authenticated : 
        return redirect('/')
    return render(request,'warehousing/eventDefinitions.html',{'au':au})


@csrf_exempt
def confirmpat(request):
    
    chartNoArray = np.array(request.session.get('warehousing_chartNo'))
    eventIDArray = np.array(request.session.get('warehousing_eventID'))
    eventIDStringArray = []
    num=[]
    examID=''
    uncheckPatient=''
    scrollTop=0
    print(chartNoArray)
    if len(chartNoArray)!=0:

        uniqueChartNoArray = np.unique(chartNoArray)
        for chartNo in uniqueChartNoArray:
            eventGroup = eventIDArray[np.where(chartNoArray==chartNo)]
            num.append(len(eventGroup))
            eventIDString = ",".join(np.unique(eventGroup))
            eventIDStringArray.append(eventIDString)

        uniqueChartNoArray = np.array(list(map(lambda chartNo:int(chartNo),uniqueChartNoArray)))

        # renewAllEvent_query = '''EXEC renewAllEvent @chartNo=%s'''
        # cursor = connections['practiceDB'].cursor()
        
        eventIDStringArray = np.array(eventIDStringArray)
        sortIndex = np.argsort(uniqueChartNoArray)
        num = np.array(num)
        uniqueChartNoArray = uniqueChartNoArray[sortIndex]
        eventIDStringArray = eventIDStringArray[sortIndex]
        num=num[sortIndex]
        chartNoString = '('
        chartNoString += "),(".join(map(str, uniqueChartNoArray.tolist()))
        chartNoString += ')'
        eventUnChecked_query = f'''                            --所有事件
                            select a.chartNo ,a.count1-isNULL(b.count2,0) as result from(
                            SELECT a.chartNo,count(b.chartNo) count1
                                                        FROM (
                                                        VALUES {chartNoString}
                                                        ) AS a(chartNo)
                                                        left join allEvents as b on a.chartNo=b.chartNo
                                                        group by a.chartNo 
                            )as a
                            left join(
                            SELECT a.chartNo,count(b.chartNo) as count2
                                                        FROM (
                                                        VALUES {chartNoString}
                                                        ) AS a(chartNo)
                                                        left join allEvents as b on a.chartNo=b.chartNo
                                                        where eventChecked is not null
                                                        group by a.chartNo 
                            ) as b on a.chartNo=b.chartNo order by a.chartNo'''
        cursor = connections['practiceDB'].cursor()
        print(eventUnChecked_query)
        cursor.execute(eventUnChecked_query,[])
        eventUnChecked_num = []
        res = cursor.fetchall()
        for row in res:
            eventUnChecked_num.append(row[1])

        query = '''select count(chartNo) from PatientDisease where chartNo=%s'''
        cursor = connections['practiceDB'].cursor()

        #examID = list(cursor.fetchall())
        i=0
        print(len(uniqueChartNoArray),len(eventUnChecked_num))
        for chartNo,eventID in zip(uniqueChartNoArray,eventIDStringArray):
            cursor.execute(query,[int(chartNo)])
            result = cursor.fetchall()[0][0]

            
            if result > 0:
                examID += f'''<tr><td>'''
                examID += f'''<input type="radio" data-chartNo="{chartNo}" onclick="getMedtype();GetTime()" name="confirmPID" id={i} data-eventID="{eventID}">'''
                examID += f'''<label for={i}><p class="PatientListID exclude">{chartNo}</p><p class="ID">{chartNo}</p><span class="newImageNum">({num[i]})</span><span class="eventUnCheckedNum">({eventUnChecked_num[i]})</span></label>'''
                examID += f'''</td></tr>'''   
            else:
                uncheckPatient += f'''<tr><td>'''
                uncheckPatient += f'''<input type="radio" data-chartNo="{chartNo}" onclick="getMedtype();GetTime()" name="confirmPID" id={i} data-eventID="{eventID}">'''
                uncheckPatient += f'''<label for={i}><p class="PatientListID exclude">{chartNo}</p><p class="ID">{chartNo}</p><span class="newImageNum">({num[i]})</span><span class="eventUnCheckedNum">({eventUnChecked_num[i]})</span></label>'''
                uncheckPatient += f'''</td></tr>'''  
            i += 1
    return JsonResponse({'examID': examID,'uncheckPatient':uncheckPatient,'scrollTop':scrollTop})

@csrf_exempt
def confirmpat2(request):
    PID=request.POST.get('ID')
    eventIDArray=request.POST.get('eventIDArray')
    print(PID)
    excludeFilter = request.POST.get('excludeFilter')
    scrollTop = request.POST.get('scrollTop')
    request.session['eventDefinition_scrollTop']=scrollTop
    query = '''EXEC EventDefinition_getPatientEvent @chartNo = %s, @filter = %s'''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query,[PID,0])
    objectArray=[]
    MedType=[]
    eventID=[]
    eventCheckedArray=[]
    con = cursor.fetchall()
    for i in range(len(con)):
        MedType.append(con[i][3])
        eventID.append(con[i][6])
        eventChecked = con[i][7]
        eventCheckedArray.append(eventChecked)
        note = con[i][8]
        if eventChecked is None:
            eventChecked=True
        if note is None:
            note=''
        
        object = f'''<tr><td>'''

        object += f'''<input type="radio" onclick="GetReport()" name="timePID" data-extractFactor=0 data-eventCheck={eventChecked} id=timePID{i}>
                    <label for=timePID{i}>'''
        object += f'''
        <div class="pdID">{i}</div>
        <div class="eventID">{con[i][6]}</div>
        <div class="ChartNo">{con[i][0]}</div>
        <div class="OrderNo">{con[i][1]}</div>
        <div class="edate">{con[i][2]}</div>
        <div class="medType">{con[i][3]}</div>
        <div class="type2">{con[i][4]}</div>
        <div class="eventChecked">🔔</div>
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

    return JsonResponse({'eventID':eventID,'MedType':MedType ,'objectArray':objectArray,'eventID_F':eventID_F,'eventCheckedArray':eventCheckedArray})




@csrf_exempt
def confirmDone(request):
    eventIDArray = request.POST.getlist('eventIDArray[]')
    query = 'update allevents set eventChecked=1 where eventID=%s'
    cursor = connections['practiceDB'].cursor()
    for eventID in eventIDArray:
        cursor.execute(query,[eventID])
    return JsonResponse({})
