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
import json


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
            # if reportID.analysed == 'N':
            #     result['reportText'].append(reportID.reportText)
            # else:
            #     result['reportText'].append(reportID.residualText)

        conn.close()

    if request.method == 'PATCH':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'newcomer'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        # print("patch in")
        #更新資料表
        query = 'update analyseText  set analysed = ?, residualText = ? output INSERTED.reportID where reportID = ?;'
        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        # print('data : ' + data.getlist['residualText'])
        print( body['reportID'])
        
        args = ["Y", body['residualText'], body['reportID']]
        
        cursor.execute(query, args)
        reportID = cursor.fetchone()
        print(reportID[0])

        #有找到
        if reportID != None:
            #print(reportID.reportText)
            result['status'] = '0'
            result['reportID'] = reportID[0]        
        conn.commit()
        conn.close()

    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'newcomer' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        # print(request.POST)
        reportID = request.POST.getlist('reportID[]')
        posStart = request.POST.getlist('posStart[]')
        posEnd = request.POST.getlist('posEnd[]')
        tokenID = request.POST.getlist('tokenID[]')
        # print(len(reportID), len(posStart), len(posEnd), len(tokenID))
        # print(reportID, posStart, posEnd, tokenID)
        for i in range(len(reportID)):
            # print(reportID[i], posStart[i], posEnd[i], tokenID[i])
            query = "select * from Vocabulary where token = ?"
            args = [tokenID[i]]
            cursor.execute(query, args)
            id = cursor.fetchone()

            #插入資料表
            query = 'INSERT into textToken (reportID, posStart, posEnd, tokenID) OUTPUT [INSERTED].reportID, [INSERTED].posStart VALUES (?, ?, ?, ?);'
            args = [reportID[i], posStart[i], posEnd[i], id.tokenID]
            cursor.execute(query, args)

        conn.commit()
        conn.close()
        result['status'] = '0'
    return JsonResponse(result)

@csrf_exempt
def getTokenREItemID(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'newcomer'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        data = []
        #取締一個取成功
        if request.is_ajax():
            # print('Raw Data: "%s"' % request.body)
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            for i in body:
                data.append(i)
            # print(data)
            # content = body[0]
            # print('Data: "%s"' % content['year'])
        tokenIDArray = []
        tokentype = []
        tokenREIDArray = []
        tokenREItemIDArray = []
        for i in data:
            #查詢tokenType
            query = 'SELECT * FROM Vocabulary where tokenID = ?;'
            args = [i['tokenID']]
            cursor.execute(query, args)
            tokenType = cursor.fetchone()
            # print("tokenType ", tokenID.tokenType)
            if tokenType:
                tokenIDArray.append(tokenType.tokenID)
                tokentype.append(tokenType.tokenType)


            #查詢tokenREID
            query = 'SELECT * FROM tokenRE where tokenID = ?;'
            args = [i['tokenID']]
            cursor.execute(query, args)
            tokenREID = cursor.fetchone()
            if tokenREID:
                tokenREIDArray.append(tokenREID.tokenREID)
                                
            temp = []
            for key in list(i.keys()):
                if tokenType.tokenType == 'E':
                    # print(j)
                    #查詢tokenREItemID
                    query = 'SELECT * FROM tokenREItem where tokenREID = ? and itemName = ?;'
                    args = [tokenREID.tokenREID, key]
                    cursor.execute(query, args)
                    tokenREItemID = cursor.fetchone()
                if tokenREItemID:
                    temp.append(tokenREItemID.tokenREItemID)
            tokenREItemIDArray.append(temp)
                    
                        # print("tokenREItemID ", tokenREItemID.tokenREItemID)
        print(tokenIDArray)
        print(tokentype)
        print(tokenREIDArray)
        print(tokenREItemIDArray)




        #有找到
        if (tokenType != None) and (tokenREID != None) :
            result['status'] = '0'
            # result['tokenID'] = tokenIDArray
            # result['tokenREID'] = tokentype
            # result['tokenType'] = tokenREIDArray
            # # if (tokenType.tokenType == 'E') and (tokenREItemID != None):
            # result['tokenREItemID'] = tokenREItemIDArray

            record = {}
            result['data'] = []
            record['tokenID'] = tokenIDArray
            record['tokenREID'] = tokenREIDArray
            record['tokenType'] = tokentype
            record['tokenREItemID'] = tokenREItemIDArray
            result['data'].append(record)
        # print(result)
        conn.close()
    return JsonResponse(result)

@csrf_exempt
def insertExtractedValueFromToken(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'newcomer' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        # print("request: ", request.POST.getlist('tokenID[]'))

        #取得post資料
        reportID = request.POST.getlist('reportID[]')
        posStart = request.POST.getlist('posStart[]')
        tokenREItemID = request.POST.getlist('tokenREItemID[]')
        tokenType = request.POST.getlist('tokenType[]')        
        Value = request.POST.getlist('Value[]')
        # print("tokenID: ", request.POST.getlist('tokenID[]'))
        # print("posStart: ", request.POST.getlist('posStart[]'))
        # print("tokenREItemID: ", request.POST.getlist('tokenREItemID[]')[0].split(','))
        # print("tokenType: ", request.POST.getlist('tokenType[]'))
        # print("Value: ", request.POST.getlist('Value[]'))

        # 處理tokenREItemID二維陣列(用逗號分開轉int)
        for i in range(len(tokenREItemID)):
            tokenREItemID[i] = tokenREItemID[i].split(',')
            for j in range(len(tokenREItemID[i])):
                tokenREItemID[i][j] = int(tokenREItemID[i][j])
        # print("tokenREItemID: ", tokenREItemID)

        # 處理Value二維陣列(用逗號分開)
        for i in range(len(Value)):
            Value[i] = Value[i].split(',')
        print("Value: ", Value)

        # record = {}
        # result['data'] = []
        # record['reportID'] = request.POST.get('reportID')
        # record['posStart'] = request.POST.get('posStart')
        # record['tokenREItemID'] = request.POST.get('tokenREItemID')
        # record['extractedValue'] = request.POST.get('extractedValue')
        # result['data'].append(record)

        #插入資料表()
        for i in range(len(reportID)):
            for j in range(len(tokenREItemID[i])):
                # print(tokenType[i])
                if tokenType[i] == 'E':
                    # print(reportID[i], posStart[i], tokenREItemID[i][j], Value[i][j])
                    query = 'INSERT into extractedValueFromToken (reportID, posStart, tokenREItemID, extractedValue) OUTPUT [INSERTED].reportID, [INSERTED].posStart VALUES (?, ?, ?, ?);'
                    args = [reportID[i], posStart[i], tokenREItemID[i][j], Value[i][j]]
                    cursor.execute(query, args)

        conn.commit()
        conn.close()
        result['status'] = '0'
        # print(result)
    return JsonResponse(result)



class Home(ListView):
    model = Text
    template_name = 'base.html'

class Page2(ListView):
    model = Text
    template_name = 'Page2.html'


    
