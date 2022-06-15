import django.forms
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse

def auth_control(request):
    au = request.session.get('au')
    if not request.user.is_authenticated : 
        return redirect('/')
    elif not request.user.is_superuser:
        return redirect('/')
    return render(request, 'administrator/auth_control.html',{'au':au})

@csrf_exempt
def Auth(username):
    query = '''select Authority_app from auth_user where username=%s'''
    cursor = connections['default'].cursor()
    cursor.execute(query, [username])
    res = cursor.fetchall()
    au = []
    for i in range(len(res)):
        au.append(res[i][0])
    return au

@csrf_exempt
def get_users(request):
    query = '''select username from auth_user where is_superuser=0'''
    cursor = connections['default'].cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    username = []
    for i in range(len(res)):
        username.append(res[i][0])
    return JsonResponse({'username': username})

@csrf_exempt
def get_auth_app(request):
    un=request.POST.get('username')
    query = '''select Authority_app from auth_app where username=%s'''
    cursor = connections['default'].cursor()
    cursor.execute(query,[un])
    res = cursor.fetchall()
    auth_app = []
    for i in range(len(res)):
        auth_app.append(res[i][0].replace(' ',''))
    return JsonResponse({'auth_app': auth_app})

@csrf_exempt
def upadte_auth_app(request):
    username=request.POST.get('username')
    authapp = request.POST.get('authapp')
    query = '''select Authority_app from auth_app where username=%s and Authority_app=%s'''
    cursor = connections['default'].cursor()
    cursor.execute(query,[username,authapp])
    res = cursor.fetchall()
    if(len(res)==1):#刪除資料
        query = '''delete from auth_app where username=%s and Authority_app=%s'''
        cursor = connections['default'].cursor()
        cursor.execute(query, [username, authapp])
    else:
        query = '''insert into auth_app (username,Authority_app) values (%s,%s)'''
        cursor = connections['default'].cursor()
        cursor.execute(query, [username, authapp])
    return JsonResponse({})

@csrf_exempt
def get_disease(request):
    query = '''select * from researchTopic'''
    cursor = connections['practiceDB'].cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    disease = []
    diseaseNo = []
    for i in range(len(res)):
        diseaseNo.append(str(res[i][0]))
        disease.append(res[i][1])
    return JsonResponse({'disease': disease,'diseaseNo':diseaseNo})


@csrf_exempt
def get_auth_disease(request):
    username=request.POST.get('username')
    query = '''select a.disease,b.topicName from auth_disease as a
                    inner join [practiceDB].[dbo].[researchTopic] as b on a.disease=b.topicNo
                    where username=%s order by a.disease
            '''
    cursor = connections['default'].cursor()
    cursor.execute(query,[username])
    res = cursor.fetchall()
    auth_disease = []
    auth_diseaseName = []
    for i in range(len(res)):
        auth_disease.append(res[i][0].replace(' ',''))
        auth_diseaseName.append(res[i][1])
    print(auth_disease)
    return JsonResponse({'auth_disease': auth_disease,'auth_diseaseName':auth_diseaseName})

@csrf_exempt
def upadte_auth_disease(request):
    username=request.POST.get('username')
    authdisease = request.POST.get('authdisease')
    query = '''select disease from auth_disease where username=%s and disease=%s'''
    cursor = connections['default'].cursor()
    cursor.execute(query,[username,authdisease])
    res = cursor.fetchall()
    if(len(res)==1):#刪除資料
        query = '''delete from auth_disease where username=%s and disease=%s'''
        cursor = connections['default'].cursor()
        cursor.execute(query, [username, authdisease])
    else:
        query = '''insert into auth_disease (username,disease) values (%s,%s)'''
        cursor = connections['default'].cursor()
        cursor.execute(query, [username, authdisease])
    return JsonResponse({})

@csrf_exempt
def get_user_setting(request):
    un=request.POST.get('username')
    query = '''select is_active,de_identification,all_annotations from auth_user where username=%s'''
    cursor = connections['default'].cursor()
    cursor.execute(query,[un])
    res = cursor.fetchall()
    active = res[0][0]
    de_identification = res[0][1]
    all_annotations = res[0][2]
    print(active)
    return JsonResponse({'active': active,'de_identification':de_identification,'all_annotations':all_annotations})

@csrf_exempt
def update_user_setting(request):
    username=request.POST.get('username')
    query = '''select is_active from auth_user where username=%s'''
    cursor = connections['default'].cursor()
    cursor.execute(query,[username])
    res = cursor.fetchall()
    active = res[0][0]
    print(active)
    if active:#True 更新為False
        query = '''update auth_user SET is_active=0 where username=%s'''
        cursor = connections['default'].cursor()
        cursor.execute(query, [username])
    else:#更新為True
        query = '''update auth_user SET is_active=1 where username=%s'''
        cursor = connections['default'].cursor()
        cursor.execute(query, [username])
    return JsonResponse({})

@csrf_exempt
def update_de_identificationSetting(request):
    username=request.POST.get('username')
    query = '''select de_identification from auth_user where username=%s'''
    cursor = connections['default'].cursor()
    cursor.execute(query,[username])
    res = cursor.fetchall()
    active = res[0][0]
    print(active)
    if active:#True 更新為False
        query = '''update auth_user SET de_identification=0 where username=%s'''
        cursor = connections['default'].cursor()
        cursor.execute(query, [username])
    else:#更新為True
        query = '''update auth_user SET de_identification=1 where username=%s'''
        cursor = connections['default'].cursor()
        cursor.execute(query, [username])
    return JsonResponse({})

@csrf_exempt
def update_all_annotations(request):
    username=request.POST.get('username')
    query = '''select all_annotations from auth_user where username=%s'''
    cursor = connections['default'].cursor()
    cursor.execute(query,[username])
    res = cursor.fetchall()
    active = res[0][0]
    print(active)
    if active:#True 更新為False
        query = '''update auth_user SET all_annotations=0 where username=%s'''
        cursor = connections['default'].cursor()
        cursor.execute(query, [username])
    else:#更新為True
        query = '''update auth_user SET all_annotations=1 where username=%s'''
        cursor = connections['default'].cursor()
        cursor.execute(query, [username])
    return JsonResponse({})

@csrf_exempt
def getAuthDiseaseLabeledUser(request):
    Disease=request.POST.get('disease')
    username=request.POST.get('username')
    query = '''select distinct username from annotation where Disease=%s and username<>%s'''
    cursor = connections['AIC'].cursor()
    cursor.execute(query,[Disease,username])
    res = cursor.fetchall()
    LabeledUser = []
    for i in range(len(res)):
        LabeledUser.append(str(res[i][0]))
    return JsonResponse({'LabeledUser':LabeledUser})

@csrf_exempt
def insertAuthDiseaseLabeledUser(request):
    disease=request.POST.get('disease')
    export_user=request.POST.get('export_user')
    import_user=request.POST.get('import_user')
    query = '''
        insert into annotation(PID,SD,Item,date,username,SUV,x,y,z,LabelGroup,LabelName,LabelRecord,Click_X,Click_Y,Click_Z,Disease,StudyID,fromWhere,seriesID)
        SELECT a.* 
        from(
            SELECT PID,SD,Item,date,%s as username,SUV,x,y,z,LabelGroup,LabelName,LabelRecord,Click_X,Click_Y,Click_Z,Disease,StudyID,%s as fromWhere,seriesID FROM annotation 
            WHERE Disease=%s and username=%s
        ) as a left outer join annotation as b on a.PID=b.PID and a.SD=b.SD and a.Item=b.Item and a.date=b.date and a.username=b.username and a.SUV=b.SUV and a.x=b.x and a.y=b.y and a.z=b.z and a.StudyID=b.StudyID and a.seriesID=b.seriesID
        where b.PID is null
    '''
    cursor = connections['AIC'].cursor()
    cursor.execute(query,[import_user,export_user,disease,export_user])
    return JsonResponse({})

@csrf_exempt
def removeAuthDiseaseLabeledUser(request):
    disease=request.POST.get('disease')
    export_user=request.POST.get('export_user')
    import_user=request.POST.get('import_user')
    print(disease)
    query = '''
        delete from  annotation  where username=%s and fromWhere=%s and Disease=%s
    '''
    cursor = connections['AIC'].cursor()
    cursor.execute(query,[import_user,export_user,disease])
    return JsonResponse({})