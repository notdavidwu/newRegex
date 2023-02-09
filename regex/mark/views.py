from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView
from django.template import loader
from django.http import HttpResponse
from django.views.generic import ListView,DeleteView

from mark.serializers import TextSerializer 
from mark.models import *
from mark.forms import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import re
import pyodbc


    # queryset = Text.objects.all()
    # serializer_class = TextSerializer
    # def get(self, request, *args, **krgs):
    #     Texts = self.get_queryset()
    #     serializer = self.serializer_class(Texts, many=True)
    #     data = serializer.data
    #     return JsonResponse(data, safe=False)
    # def post(self, request, *args, **krgs):
    #     data = request.data
    #     try:
    #         serializer = self.serializer_class(data=data)
    #         serializer.is_valid(raise_exception=True)
    #         with transaction.atomic():
    #             serializer.save()
    #         data = serializer.data
    #     except Exception as e:
    #         data = {'error': str(e)}
    #     return JsonResponse(data)
    
    #沒用到
def TextView(request):
    result = {'status':'1'}#預設失敗
    if request.method == 'GET':
        a = Text.objects.all()
        result = {'status':'0'}#成功
        result['text_input'] = []
        for item in a:
            record = {}
            record['id'] = item.id
            record['regexText'] = item.regexText
            record['inputText'] = item.inputText
            result['text_input'].append(record)
    # return JsonResponse(result)
    template = loader.get_template('index.html')
    # return HttpResponse(template.render()) #回傳template
    return render(request, 'index.html')

    #沒用到
@csrf_exempt
def TextFormView(request):
    if  request.method == 'POST':
        form = TextModelForm(request.POST) #拿到POST過來的資料並填入form
        result = {'status':'1'} #預設失敗
        print(request.POST)
        if form.is_valid(): #檢查forms.py中的格式
            print("form is valid")            
            data = form.cleaned_data #接form裡面丟出來的資料
            # print(data)
            FormRegexText = form.cleaned_data['regexText'] #依標籤解析出資料
            FormInputText = form.cleaned_data['inputText'] #依標籤解析出資料
            # print("User is :", request.user)
            # print("regexText is :",FormRegexText)
            # print("inputText is :",FormInputText)
            # if FormInputText != None and FormRegexText != None:
            #     text123 = Text.objects.create(author=request.user) #建立新表單
            #     text123.author = request.user
            #     text123.regexText = FormRegexText #將解析完的資料丟到物件內
            #     text123.inputText = FormInputText #將解析完的資料丟到物件內
            #     result = {'status':'0'}
            #     text123.save() #存檔
            # print(result)
        else:
            print("form is NOT valid.")
    
    
    
        
        
    return JsonResponse(result)

    #取得Vocabulary所有token並回傳
@csrf_exempt
def getVocabulary(request):
    if request.method == 'GET':
        #測試拉資料
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'newcomer' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        result = cursor.execute("select * from Vocabulary")
        patient = cursor.fetchall()
        result = {}
        result['data'] = []       
        for item in patient:
            record = {}
            record['token'] = item.token
            result['data'].append(record)
    return JsonResponse(result)

    #取得Vocabulary所有token用tokenType篩選並回傳
@csrf_exempt
def getVocabularyByType(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        try:
            #建立連線
            server = '172.31.6.22' 
            database = 'buildVocabulary' 
            username = 'newcomer' 
            password = 'test81218' 
            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
            cursor = conn.cursor()
            #插入資料表
            query = 'select * from Vocabulary where tokenType=?;'
            args = [request.GET['tokenType']]
            #print(args)
            cursor.execute(query, args)
            tokenID = cursor.fetchall()
            #print(tokenID[0])
            conn.commit()
            conn.close()
            result['status'] = '0'            
            result['data'] = []
            for i in tokenID:
                record = {}
                record['token'] = i.token      
                #print("token: " + str(i.token))
                result['data'].append(record)
        except:
            result = {'status':'1'} #預設失敗
    return JsonResponse(result)

    #新增至Vocabulary並回傳新增的tokenID
@csrf_exempt
def insertVocabulary(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        try:
            #建立連線
            server = '172.31.6.22' 
            database = 'buildVocabulary' 
            username = 'newcomer' 
            password = 'test81218' 
            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
            cursor = conn.cursor()
            #result = cursor.execute("select * from Vocabulary")
            #取得post資料
            result['data'] = []
            record = {}
            record['token'] = request.POST.get('token')
            record['nWord'] = request.POST.get('nWord')
            record['tokenType'] = request.POST.get('tokenType')
            #插入資料表
            query = 'INSERT into Vocabulary (token,nWord,tokenType) OUTPUT [INSERTED].tokenID VALUES (?, ?, ?);'
            args = [request.POST.get('token'),int(request.POST.get('nWord')),request.POST.get('tokenType')]
            print(args)
            cursor.execute(query, args)
            tokenID = cursor.fetchall()
            print(tokenID[0])
            conn.commit()
            conn.close()
            result['status'] = '0'
            record['tokenID'] = tokenID[0][0]            
            result['data'].append(record)
            print("data saved(Vocabulary)")
        except:
            result = {'status':'1'} #預設失敗
            print("insert into Vocabulary error occurred")
        
    return JsonResponse(result)

    #新增至tokenRE並回傳tokenID.RE.tokenREID
@csrf_exempt
def inserttokenRE(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        try:
            #建立連線
            server = '172.31.6.22' 
            database = 'buildVocabulary' 
            username = 'newcomer' 
            password = 'test81218' 
            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
            cursor = conn.cursor()
            #result = cursor.execute("select * from Vocabulary")
            #取得post資料
            result['data'] = []
            record = {}
            record['tokenID'] = request.POST.get('tokenID')
            record['RE'] = request.POST.get('RE')
            #插入資料表
            query = 'INSERT into tokenRE (tokenID, RE) OUTPUT [INSERTED].tokenREID VALUES (?, ?);'
            args = [int(request.POST.get('tokenID')), request.POST.get('RE') ]
            print(args)
            cursor.execute(query, args)
            tokenREID = cursor.fetchall()
            print(tokenREID[0])
            conn.commit()
            conn.close()            
            result['status'] = '0'
            record['tokenREID'] = tokenREID[0][0]            
            result['data'].append(record)
            print("data saved(tokenRE)")
        except:
            result = {'status':'1'} #預設失敗
            print("insert into tokenRE error occurred")

    return JsonResponse(result)

    #新增至tokenREItem並回傳tokenREID.serialNo.itemName.tokenREItemID
@csrf_exempt
def inserttokenREItem(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        try:
            #建立連線
            server = '172.31.6.22' 
            database = 'buildVocabulary' 
            username = 'newcomer' 
            password = 'test81218' 
            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
            cursor = conn.cursor()
            #result = cursor.execute("select * from Vocabulary")
            #取得post資料
            result['data'] = []
            record = {}
            record['tokenREID'] = request.POST.get('tokenREID')
            record['serialNo'] = request.POST.get('serialNo')
            record['itemName'] = request.POST.get('itemName')
            #插入資料表
            query = 'INSERT into tokenREItem (tokenREID, serialNo, itemName) OUTPUT [INSERTED].tokenREID VALUES (?, ?, ?);'
            args = [int(request.POST.get('tokenREID')), request.POST.get('serialNo'), request.POST.get('itemName') ]
            print(args)
            cursor.execute(query, args)
            tokenREItemID = cursor.fetchall()
            print(tokenREItemID[0])
            conn.commit()
            conn.close()
            result['status'] = '0'
            record['tokenREItemID'] = tokenREItemID[0][0]
            result['data'].append(record)
            print("data saved(tokenREItem)")
        except:
            result = {'status':'1'} #預設失敗
            print("insert into tokenREItem error occurred")

    return JsonResponse(result)

    #檢查傳入的token存不存在Vocabulary
@csrf_exempt
def checkName(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'newcomer'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        query = 'SELECT * FROM Vocabulary WHERE token=? ;'
        args = [request.GET['Name']]
        print(args)
        #print(query)
        cursor.execute(query, args)
        token = cursor.fetchone()
        print(token)

        #有找到
        if token != None:
            result['status'] = '0'
            result['tokenID'] = token.tokenID
            result['tokenType'] = token.tokenType
        #     print(token[0])
        conn.close()
    return JsonResponse(result)

#找RE
@csrf_exempt
def checkRE(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'newcomer'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        query = 'SELECT * FROM tokenRE WHERE tokenID=? ;'
        args = [request.GET['tokenID']]
        print(args)
        #print(query)
        cursor.execute(query, args)
        tokenID = cursor.fetchone()
        print(tokenID)

        #有找到
        if tokenID != None:
            result['status'] = '0'
            result['RE'] = tokenID.RE
            result['tokenREID'] = tokenID.tokenREID
        #     print(token[0])
        conn.close()            
    return JsonResponse(result)

#找REItem
@csrf_exempt
def checkREItem(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'newcomer'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        query = 'SELECT * FROM tokenREItem WHERE tokenREID=? ;'
        args = [request.GET['tokenREID']]
        print(args)
        #print(query)
        cursor.execute(query, args)
        tokenREID = cursor.fetchall()
        print(tokenREID)

        #有找到
        if tokenREID != None:
            result['status'] = '0'
            result['data'] = []
            for item in tokenREID:
                record = {}
                record['itemName'] = item.itemName
                result['data'].append(record)
        #     print(token[0])
        conn.close()            
    return JsonResponse(result)

    #取得點選ID的reportText
@csrf_exempt
def getAnalyseText(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'newcomer'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        query = 'SELECT * FROM analyseText;'
        cursor.execute(query)
        reportText = cursor.fetchall()

        #有找到
        if reportText != None:
            result['status'] = '0'
            result['data'] = []
            for item in reportText:
                record = {}
                record['reportText'] = item.reportText
                result['data'].append(record)
        #     print(token[0])
        conn.close()
        
    return JsonResponse(result)

    #讀取所有reportID
@csrf_exempt
def getReportID(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'newcomer'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        query = 'SELECT * FROM analyseText;'
        cursor.execute(query)
        reportID = cursor.fetchall()

        #有找到
        if reportID != None:
            result['status'] = '0'
            result['data'] = []
            for item in reportID:
                record = {}
                record['reportID'] = item.reportID
                result['data'].append(record)
        #     print(token[0])
        conn.close()
    return JsonResponse(result)

    #用reportID讀取reportText
@csrf_exempt
def getReportText(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'newcomer'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        query = 'SELECT * FROM analyseText where reportID = ?;'        
        args = [request.GET['reportID']]
        cursor.execute(query, args)
        reportID = cursor.fetchone()

        #有找到
        if reportID != None:
            #print(reportID.reportText)
            result['status'] = '0'
            result['reportText'] = []
            result['reportText'].append(reportID.reportText)
        conn.close()
        
    return JsonResponse(result)


class Home(ListView):
    model = Text
    template_name = 'base.html'

class Page2(ListView):
    model = Text
    template_name = 'Page2.html'


    
