from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import pathlib

def pool(request):
    au = request.session.get('au')
    return render(request, 'pool/pool.html',{'au':au})

@csrf_exempt
def SubjectPatientList(request):
    Disease=request.POST.get('Disease')
    query = '''
          	select distinct a.chartNo
            from correlationPatientDisease as a 
                inner join diseaseGroup as e on a.diseaseNo=e.DiseaseNo
                inner join allEvents as f on a.chartNo=f.chartNo
                inner join ExamStudySeries_6 as g on f.eventID=g.eventID
                where a.diseaseNo=%s
    '''
    cursor = connections['default'].cursor()
    cursor.execute(query,[Disease])
    PatientListID=[]
    res = cursor.fetchall()
    for i in range(len(res)):
        PatientListID.append(res[i][0])
    return JsonResponse({'PatientListID': PatientListID})
@csrf_exempt
def PatientList(request):
    condition = request.POST.get('PID')
    Disease = request.POST.get('Disease')

    query =  '''
  select b.chartNo,b.eventDate,d.TypeName,f.Enent,b.eventID,e.category from allEvents as b 
		left join EventDefinition as c on b.eventID=c.eventID
		inner join medTypeSet as d on  b.medType=d.MedType
        inner join ExamStudySeries_6 as e on b.eventID=e.eventID
		left join ClinicalEvents as f on c.EventID=f.EventID
        where b.chartNo=%s
        group by b.chartNo,b.eventDate,d.TypeName,f.Enent,b.eventID,e.category
		order by b.eventDate DESC
    '''

    query2 = '''
        select studyID from ExamStudySeries_6 where sliceNo in
                (select MAX(sliceNo) from (
                select eventID,studyID,category,seriesID,seriesDes,sliceNo
                from ExamStudySeries_6) as a left outer join allEvents as b on a.eventID=b.eventID 
                where b.eventID=%s ) and eventID=%s group by studyID
        '''

    cursor = connections['default'].cursor()
    cursor.execute(query,[condition])
    PID = []
    MedExecTime = []
    Item = []
    phase = []
    Check = []
    Study = []
    StudyDes=[]
    res = cursor.fetchall()
    for j in range(len(res)):
        cursor2 = connections['default'].cursor()
        cursor2.execute(query2, [res[j][4],res[j][4]])
        StudyID = cursor2.fetchall()
        if StudyID != []:
            StudyID = (StudyID[0][0])
            Study.append(StudyID)
        else:
            Study.append(0)
        fileDir = "D:\\image\\" + str(res[j][0]) + '\\' + str(res[j][1]) + '\\' + str(StudyID)
        fileDir = fileDir.replace('-', '')
        fileDir = fileDir.replace(' ', '')

        fileExt = r"**\*.h5"
        print(fileDir)
        if len(list(pathlib.Path(fileDir).glob(fileExt))) == 0:
            Check.append('N')
        else:
            Check.append('Y')

    for i in range(len(res)):
        PID.append(res[i][0])
        MedExecTime.append(res[i][1])
        Item.append(res[i][2])
        phase.append(res[i][3])
        StudyDes.append(res[i][5])

    return JsonResponse({'PID': PID, 'MedExecTime': MedExecTime,'StudyID':Study ,'Item': Item,'StudyDes':StudyDes, 'phase': phase, 'Check': Check},
                        status=200)


@csrf_exempt
def Session(request):
    PID = request.POST.get('PID')
    MedExecTime = request.POST.get('MedExecTime')
    Item = request.POST.get('Item')
    StudyID = request.POST.get('StudyID')
    Disease = request.POST.get('Disease')
    request.session['PID'] = PID
    request.session['MedExecTime'] = MedExecTime
    request.session['Item'] = Item
    request.session['StudyID'] = StudyID
    request.session['Disease'] = Disease
    return JsonResponse({})
    #print(PID)
    #return render(request, 'DICOM/DICOM.html', {'PID':PID,'MedExecTime':MedExecTime,'Item':Item})