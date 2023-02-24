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
import copy


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
        result = cursor.execute("select * from Vocabulary where tokenType != 'U' ")
        patient = cursor.fetchall()
        result = {}
        result['data'] = []
        for item in patient:
            record = {}
            record['token'] = item.token
            result['data'].append(record)
        
        conn.commit()
        conn.close()
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
            if request.GET['tokenType'] == 'U':
                query = 'select * from Vocabulary where tokenType=? and tokenID <= 152 order by tokenID DESC;'
            else:
                query = 'select * from Vocabulary where tokenType=?;'
            args = [request.GET['tokenType']]
            #print(args)
            cursor.execute(query, args)
            tokenID = cursor.fetchall()
            #print(tokenID[0])
            result['status'] = '0'            
            result['data'] = []
            for i in tokenID:
                record = {}
                record['token'] = i.token      
                #print("token: " + str(i.token))
                result['data'].append(record)
        except:
            result = {'status':'1'} #預設失敗
    
        conn.commit()
        conn.close()
    return JsonResponse(result)

    #新增至Vocabulary並回傳新增的tokenID
@csrf_exempt
def insertVocabulary(request):
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
        result['status'] = '0'
        record['tokenID'] = tokenID[0][0]            
        result['data'].append(record)
        print("data saved(Vocabulary)")
        conn.commit()
        conn.close()
            
    return JsonResponse(result)

    #新增至Vocabulary並回傳新增的tokenID
@csrf_exempt
def insertVocabulary_U(request):
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
        #result = cursor.execute("select * from Vocabulary")
        #取得post資料
        result['data'] = []
        # record = {}
        # record['token'] = request.POST.get('token')
        # record['nWord'] = request.POST.get('nWord')
        # record['tokenType'] = request.POST.get('tokenType')
        token = request.POST.getlist('token[]')
        nWord = request.POST.getlist('nWord[]')
        tokenType = request.POST.getlist('tokenType[]')
        print("token : ", len(token))
        print("nWord : ", len(nWord))
        print("tokenType : ", len(tokenType))
        tokenID = []
        for i in range(len(token)):
            Token = token[i]
            Token = Token.lower()
            print("Token : ", Token)
            #先查詢
            query = 'select * from Vocabulary where token = ?;'
            args = [Token]
            cursor.execute(query, args)
            old_tokenID = cursor.fetchone()
            # print("old_tokenID", old_tokenID)
            # print("i : ", i)
            # 不存在插入
            if old_tokenID == None:
                # print("i : ", i)
                query = 'INSERT into Vocabulary (token,nWord,tokenType) OUTPUT [INSERTED].tokenID VALUES (?, ?, ?);'
                args = [Token,nWord[i],tokenType[i]]
                # print("args : ", args)
                cursor.execute(query, args)
                newtoken = cursor.fetchone()
                # 沒找到存現在的tokenID
                tokenID.append(newtoken.tokenID)
            else:
                # 有找到存舊的tokenID
                tokenID.append(old_tokenID.tokenID)
        print("ID : ", tokenID)
        result['status'] = '0'
        # record['tokenID'] = tokenID[0][0]            
        result['data'].append(tokenID)
        # print("data saved(Vocabulary)")
        print(result)
        conn.commit()
        conn.close()            
    return JsonResponse(result)

    #插入U資料
@csrf_exempt
def getTextToken(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'newcomer' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        query = 'select * from [buildVocabulary ].[dbo].textToken as A inner join [buildVocabulary ].[dbo].textToken as B on A.reportID = B.reportID and B.posStart - A.posEnd = 1 and A.posStart > 0 and B.posStart > 0 order by A.reportID, A.posStart;'
        cursor.execute(query)
        textTokenData = cursor.fetchall()
        # print("textTokenData : ", textTokenData)
        result['data'] = []
        # print(textTokenData[0][0])
        record = {}
        for i in textTokenData:
            # print(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])          
            result['status'] = '0'
            record['reportID1'] = i[0]
            record['posStart1'] = i[1]
            record['posEnd1'] = i[2]
            record['tokenID1'] = i[3]
            record['reportID2'] = i[4]
            record['posStart2'] = i[5]
            record['posEnd2'] = i[6]
            record['tokenID2'] = i[7]
            # print(record)
            result['data'].append(copy.deepcopy(record))

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
        tokenID = request.POST.getlist('tokenID[]')[0]
        tokenID = tokenID.split(",")
        # print(len(reportID), len(posStart), len(posEnd), len(tokenID))
        # print(  type(reportID), type(posStart), type(posEnd), type(tokenID))
        # print("tokenID : ", tokenID.split(","))
        for i in range(len(reportID)):
            result['status'] = '0'
            
            print( reportID[i], posStart[i], posEnd[i], tokenID[i])
            #插入資料表
            query = 'INSERT into textToken (reportID, posStart, posEnd, tokenID) OUTPUT [INSERTED].reportID, [INSERTED].posStart VALUES (?, ?, ?, ?);'
            args = [int(reportID[i]), posStart[i], posEnd[i], int(tokenID[i])]
            # print("args : ", args)
            cursor.execute(query, args)

        conn.commit()
        conn.close()
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
            result['status'] = '0'
            record['tokenREID'] = tokenREID[0][0]            
            result['data'].append(record)
            print("data saved(tokenRE)")
        except:
            result = {'status':'1'} #預設失敗
            print("insert into tokenRE error occurred")
    
        conn.commit()
        conn.close()     

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
            result['status'] = '0'
            record['tokenREItemID'] = tokenREItemID[0][0]
            result['data'].append(record)
            print("data saved(tokenREItem)")
        except:
            result = {'status':'1'} #預設失敗
            print("insert into tokenREItem error occurred")
        conn.commit()
        conn.close()


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
        Token = request.GET.getlist('Name[]')
        tokenID = []
        tokenType = []

        for i in range(len(Token)):
            query = 'SELECT * FROM Vocabulary WHERE token = ?;'
            args = [Token[i]]
            cursor.execute(query, args)
            token = cursor.fetchone()
            if token:
                tokenID.append(token.tokenID)
                tokenType.append(token.tokenType)
        # print(tokenID)
        # print(tokenType)
# 
        # 有找到
        if token:
            result['status'] = '0'
            result['tokenID'] = tokenID
            result['tokenType'] = tokenType
        
        conn.commit()
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
        TokenID = request.GET.getlist('tokenID[]')
        RE = []
        TokenREID = []

        for i in range(len(TokenID)):
            query = 'SELECT * FROM tokenRE WHERE tokenID = ?;'
            args = [TokenID[i]]
            # print(args)
            #print(query)
            cursor.execute(query, args)
            tokenREID = cursor.fetchone()
            if tokenREID:
                RE.append(tokenREID.RE)
                TokenREID.append(tokenREID.tokenREID)
        print("RE : ", RE)
        print("TokenREID : ", TokenREID)

        #有找到
        if tokenREID != None:
            result['status'] = '0'
            result['RE'] = RE
            result['tokenREID'] = TokenREID
        
        conn.commit()
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
        conn.commit()
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
        # query = 'SELECT * FROM analyseText where reportID = 120362328 or reportID = 126933368 or reportID = 126989974 or reportID = 127185348;'
        # query = 'SELECT * FROM analyseText;'
        query = 'SELECT * FROM analyseText where reportID >= 130000000 and reportID <= 130060000;'
        
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
        
        conn.commit()
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
            # result['reportText'].append(reportID.reportText)
            if reportID.analysed == 'N':
                result['reportText'].append(reportID.reportText)
            else:
                result['reportText'].append(reportID.residualText)

        
        conn.commit()
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
        query = 'update analyseText  set analysed = ?, residualText = ? output INSERTED.reportID,INSERTED.reportText,INSERTED.residualText where reportID = ?;'
        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        # print('data : ' + data.getlist['residualText'])
        print( body['reportID'])
        
        args = ["Y", body['residualText'], body['reportID']]
        
        cursor.execute(query, args)
        reportID = cursor.fetchone()

        #有找到
        if reportID != None:
            #print(reportID.reportText)
            result['status'] = '0'
            result['reportText'] = reportID[0]        
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
            
            result['status'] = '0'
            if id.tokenType == 'U':
                result = {'status':'U'}
            #插入資料表
            query = 'INSERT into textToken (reportID, posStart, posEnd, tokenID) OUTPUT [INSERTED].reportID, [INSERTED].posStart VALUES (?, ?, ?, ?);'
            args = [reportID[i], posStart[i], posEnd[i], id.tokenID]
            # print("args : ", args)
            cursor.execute(query, args)

        conn.commit()
        conn.close()
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
            # print("data : ", data)
            # content = body[0]
            # print('Data: "%s"' % content['year'])
        tokenIDArray = []
        tokentypeArray = []
        tokenREIDArray = []
        tokenREItemIDArray = []
                                        
        temp = []
        
        for i in range(len(data)):
            temp.clear()
            # print("data[i] : ", data[i])
            if data[i]['tokenID']:
                #查詢tokenType
                query = 'SELECT * FROM Vocabulary where tokenID = ?;'
                args = [data[i]['tokenID']]
                cursor.execute(query, args)
                tokenType = cursor.fetchone()
                # print("tokenType ", tokenID.tokenType)
                if tokenType:
                    tokenIDArray.append(tokenType.tokenID)
                    tokentypeArray.append(tokenType.tokenType)

                if tokenType.tokenType == 'E':
                    #查詢tokenREID
                    query = 'SELECT * FROM tokenRE where tokenID = ?;'
                    args = [data[i]['tokenID']]
                    cursor.execute(query, args)
                    tokenREID = cursor.fetchone()
                    if tokenREID:
                        tokenREIDArray.append(tokenREID.tokenREID)
                    print("data[i].keys()", data[i].keys())
                    for j in range(len(list(data[i].keys()))):
                        if tokenType.tokenType == 'E':
                            # print(j)
                            #查詢tokenREItemID
                            query = 'SELECT * FROM tokenREItem where tokenREID = ? and itemName = ?;'
                            args = [tokenREID.tokenREID, list(data[i].keys())[j]]
                            cursor.execute(query, args)
                            tokenREItemID = cursor.fetchone()
                        if tokenREItemID:
                            temp.append(tokenREItemID.tokenREItemID)
                            print("temp : ", temp)
                        print("j : ", j)
                        print("len : ", len(list(data[i].keys()))-1)
                        if len(list(data[i].keys()))-1 == j:
                            tokenREItemIDArray.append(copy.deepcopy(temp))
                            print("tokenREItemIDArray : ", tokenREItemIDArray)

        record = {}
        result['data'] = []
        record['tokenID'] = tokenIDArray
        record['tokenREID'] = tokenREIDArray
        record['tokenType'] = tokentypeArray
        record['tokenREItemID'] = tokenREItemIDArray
        result['data'].append(record)
        # print(result)
        conn.commit()
        conn.close()
        result['status'] = '0'
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
        # print("reportID: ", request.POST.getlist('reportID[]'))
        # print("posStart: ", request.POST.getlist('posStart[]'))
        # print("tokenREItemID: ", request.POST.getlist('tokenREItemID[]'))
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
        # print("Value: ", len(Value))
        # print("Value: ", Value)
        
        # print("tokenREItemID: ", len(tokenREItemID))
        tokenREItemIDIndex = 0
        #插入資料表()
        for i in range(len(reportID)):
            # print("i : ", i)
            if tokenType[i] == 'E':
                for j in range(len(tokenREItemID[tokenREItemIDIndex])):
                    # print("j : ", j)
                    # print(tokenType[i])
                    # print(reportID[i], posStart[i], tokenREItemID[i][j], Value[i][j])
                    query = 'INSERT into extractedValueFromToken (reportID, posStart, tokenREItemID, extractedValue) OUTPUT [INSERTED].reportID, [INSERTED].posStart VALUES (?, ?, ?, ?);'
                    Value[tokenREItemIDIndex][j] = Value[tokenREItemIDIndex][j].replace("|", ",")
                    args = [reportID[i], posStart[i], tokenREItemID[tokenREItemIDIndex][j], Value[tokenREItemIDIndex][j]]
                    cursor.execute(query, args)
                tokenREItemIDIndex += 1

        conn.commit()
        conn.close()
        result['status'] = '0'
        # print(result)
    return JsonResponse(result)


@csrf_exempt
def getToken(request):
    if request.method == 'GET':
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

        #取得資料
        tokenID1 = request.GET.getlist('tokenID1[]')
        tokenID2 = request.GET.getlist('tokenID2[]')
        # print(tokenID1)        
        # print(tokenID2)
        token1 = []
        token2 = []
        for i in tokenID1:
            # print(i)
            query = 'select * from Vocabulary where tokenID = ?;'
            args = [i]
            cursor.execute(query, args)
            token = cursor.fetchone()
            # print(token.token)
            token1.append(token.token)

        for i in tokenID2:
            # print(i)
            query = 'select * from Vocabulary where tokenID = ?;'
            args = [i]
            cursor.execute(query, args)
            token = cursor.fetchone()
            # print(token.token)
            token2.append(token.token)

        # print(token1)
        # print(token2)
        result['data'] = []
        record = {}
        record['token1'] = token1
        record['token2'] = token2
        result['data'].append(record)
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

class Merge(ListView):
    model = Text
    template_name = 'merge.html'


    
