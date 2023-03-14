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
        # print(request.POST)
        if form.is_valid(): #檢查forms.py中的格式
            # print("form is valid")            
            data = form.cleaned_data #接form裡面丟出來的資料
            # # print(data)
            FormRegexText = form.cleaned_data['regexText'] #依標籤解析出資料
            FormInputText = form.cleaned_data['inputText'] #依標籤解析出資料
            # # print("User is :", request.user)
            # # print("regexText is :",FormRegexText)
            # # print("inputText is :",FormInputText)
            # if FormInputText != None and FormRegexText != None:
            #     text123 = Text.objects.create(author=request.user) #建立新表單
            #     text123.author = request.user
            #     text123.regexText = FormRegexText #將解析完的資料丟到物件內
            #     text123.inputText = FormInputText #將解析完的資料丟到物件內
            #     result = {'status':'0'}
            #     text123.save() #存檔
            # # print(result)
        else:
            pass
            # print("form is NOT valid.")
    
    
    
        
        
    return JsonResponse(result)

    #取得Vocabulary所有token並回傳
@csrf_exempt
def getVocabulary(request):
    if request.method == 'GET':
        #測試拉資料
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        result = cursor.execute("select * from [buildVocabulary ].[dbo].[Vocabulary] where tokenType != 'U' ")
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
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        if request.GET['tokenType'] == 'U':
            query = 'select * from [buildVocabulary ].[dbo].[Vocabulary] where (tokenType = ? and tokenID <= 152 and tokenID != 151) order by tokenID DESC;'
        elif request.GET['tokenType'] == 'P':
            query = 'select * from [buildVocabulary ].[dbo].[Vocabulary] where tokenType = ? or tokenType != \'U\';'
        else:
            query = 'select * from [buildVocabulary ].[dbo].[Vocabulary] where tokenType = ? ;'
        args = [request.GET['tokenType']]
        # print(args)
        cursor.execute(query, args)
        tokenID = cursor.fetchall()
        ## print(tokenID[0])
        result['status'] = '0'            
        result['data'] = []
        for i in tokenID:
            record = {}
            record['token'] = i.token 
            record['tokenType'] = i.tokenType     
            ## print("token: " + str(i.token))
            result['data'].append(record)
    
        conn.commit()
        conn.close()
    return JsonResponse(result)
@csrf_exempt
def getVocabularyByType_Ptable(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        query = '''    SELECT * FROM(
                SELECT a.*, b.token, b.tokenType, ROW_NUMBER() OVER (PARTITION BY a.tokenID ORDER BY posStart, reportID) AS rowID2
                --a.reportID, a.tokenID, b.token, a.posStart, a.posEnd
                FROM (
                 SELECT *, ROW_NUMBER() OVER (PARTITION BY reportID, tokenID ORDER BY posStart, reportID) AS rowID
                 FROM textToken
                ) AS a
                 inner join Vocabulary AS b ON (a.tokenID = b.tokenID) and ( b.tokenType != 'U') and b.token != '[NUM]'
                ) AS res
                WHERE res.rowID=1 and res.rowID2=1
                ORDER BY  tokenID, posStart,reportID
                '''
        # print(args)
        cursor.execute(query)
        tokenID = cursor.fetchall()
        result['data'] = []
            
        for ind,i in enumerate(tokenID):
            # print("i[0] : ",i[0])
            print("i : ", i)
            if i[1]>0 and i[2]>0:
                result['data'].append({
                    'No': ind+1,
                    'ProperNoun': i[5],
                    'tokenType': i[6],
                    'NewRE': '<button onclick="changeSrc()" class="btn btn-secondary">NewRE</button>',
                    'UnMerge':'<button onclick="" class="btn btn-danger">UnMerge</button>',
                })
            else:
                result['data'].append({
                    'No': ind+1,
                    'ProperNoun': i[5],
                    'tokenType': i[6],
                    'NewRE': '',
                    'UnMerge':'',
                })
    
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
        username = 'N824' 
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


        query = 'select * from [buildVocabulary ].[dbo].[Vocabulary] where token = ? and nWord = ?;'
        args = [request.POST.get('token'),int(request.POST.get('nWord'))]
        cursor.execute(query, args)
        tokenID_original = cursor.fetchone()
        print("tokenID_original : ", tokenID_original)

        
        if tokenID_original == None and request.POST.get('tokenType'):

        #插入資料表
            query = 'INSERT into [buildVocabulary ].[dbo].[Vocabulary] (token,nWord,tokenType) OUTPUT [INSERTED].tokenID,[INSERTED].token,[INSERTED].tokenType VALUES (?, ?, ?);'
            args = [request.POST.get('token'),int(request.POST.get('nWord')),request.POST.get('tokenType')]
            # print(args)
            cursor.execute(query, args)
            tokenID = cursor.fetchall()
            print(tokenID[0][0], tokenID[0][1], tokenID[0][2])
            if tokenID != []:
                result['status'] = '0'
                record['tokenID'] = tokenID[0][0]
                record['token'] = tokenID[0][1]
                record['tokenType'] = tokenID[0][2]
                result['data'].append(record)

        elif tokenID_original != None:
            # print("tokenID_original : ", tokenID_original)
            result['status'] = 'already_exist'
            record['tokenID'] = tokenID_original[2]
            record['token'] = tokenID_original[0]
            record['tokenType'] = tokenID_original[3]
            result['data'].append(record)

        # # print("data saved(Vocabulary)")
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
        username = 'N824' 
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
        # print("token : ", len(token))
        # print("nWord : ", len(nWord))
        # print("tokenType : ", len(tokenType))
        tokenID = []
        for i in range(len(token)):
            Token = token[i]
            # print("Token : ", Token)
            #先查詢
            query = 'select * from [buildVocabulary ].[dbo].[Vocabulary] where token = ?;'
            args = [Token]
            cursor.execute(query, args)
            old_tokenID = cursor.fetchone()
            # # print("old_tokenID", old_tokenID)
            # # print("i : ", i)
            # 不存在插入
            if old_tokenID == None:
                # # print("i : ", i)
                query = 'INSERT into Vocabulary (token,nWord,tokenType) OUTPUT [INSERTED].tokenID VALUES (?, ?, ?);'
                args = [Token,nWord[i],tokenType[i]]
                # # print("args : ", args)
                cursor.execute(query, args)
                newtoken = cursor.fetchone()
                # 沒找到存現在的tokenID
                tokenID.append(newtoken.tokenID)
            else:
                # 有找到存舊的tokenID
                tokenID.append(old_tokenID.tokenID)
        # print("ID : ", tokenID)
        result['status'] = '0'
        # record['tokenID'] = tokenID[0][0]            
        result['data'].append(tokenID)
        # # print("data saved(Vocabulary)")
        # print(result)
        conn.commit()
        conn.close()            
    return JsonResponse(result)

    
@csrf_exempt
def getTextToken(request):
    #取得
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        query = '''
                EXEC two_word;
                '''
        cursor.execute(query)
        textTokenData = cursor.fetchall()
        # # print("textTokenData : ", textTokenData)
        result['data'] = []
        # # print(textTokenData[0][0])
        record = {}
        RE = re.compile(r'([^\u4e00-\u9fa50-9a-zA-Z \n\u00A0\u200B\u2014\r]{1})') 
        RE1 = re.compile(r'([^\u4e00-\u9fa50-9a-zA-Z\(\)\:\[\]\{\}\-\/]{1})')
        number = 1
        for ind,i in enumerate(textTokenData):
            # print("textTokenData : ", i)

            if request.GET['NoSign'] == 'NS':
                first = RE.findall(i[0])
                second = RE.findall(i[1])
                # print("first : ", first)
                # print("second : ", first)
                if first == [] and second == [] :
                    result['data'].append({
                        'No': number,
                        'First': i[0],
                        'Second': i[1],
                        'Times': i[2],
                        'Mergecheck':'<button onclick="merge()" class="btn btn-info">Merge</button>',
                    })
                    number += 1 
                    
            else:                   
                first = RE1.findall(i[0])
                second = RE1.findall(i[1])
                # print("first : ", first)
                # print("second : ", first)
                if first == [] and second == [] :
                    result['data'].append({
                            'No': number,
                            'First': i[0],
                            'Second': i[1],
                            'Times': i[2],
                            'Mergecheck':'<button onclick="merge()" class="btn btn-info">Merge</button>',
                        })
                    number += 1 

        conn.commit()
        conn.close()

    #插入U資料
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        # # print(request.POST)
        reportID = request.POST.getlist('reportID[]')
        posStart = request.POST.getlist('posStart[]')
        posEnd = request.POST.getlist('posEnd[]')
        tokenID = request.POST.getlist('tokenID[]')[0]
        tokenID = tokenID.split(",")
        # # print(len(reportID), len(posStart), len(posEnd), len(tokenID))
        # # print(  type(reportID), type(posStart), type(posEnd), type(tokenID))
        # # print("tokenID : ", tokenID.split(","))
        for i in range(len(reportID)):
            result['status'] = '0'
            
            # print( reportID[i], posStart[i], posEnd[i], tokenID[i])
            #插入資料表
            query = 'INSERT into [buildVocabulary ].[dbo].[textToken] (reportID, posStart, posEnd, tokenID) OUTPUT [INSERTED].reportID, [INSERTED].posStart VALUES (?, ?, ?, ?);'
            args = [int(reportID[i]), posStart[i], posEnd[i], int(tokenID[i])]
            # # print("args : ", args)
            cursor.execute(query, args)

        conn.commit()
        conn.close()

    #把posStart posEnd *(-1)
    if request.method == 'PATCH':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        # print(body)
        # # print( body['reportID1'])

        tokenID1 = body['tokenID1']
        tokenID2 = body['tokenID2']

        
        # print(tokenID1, tokenID2)


        query = '''
                UPDATE A 
                SET A.posStart = -1 * A.posStart, A.posEnd = -1 * A.posEnd        
                OUTPUT [INSERTED].reportID, [INSERTED].posStart, [INSERTED].posEnd, [INSERTED].tokenID
                FROM 
                [buildVocabulary].[dbo].[textToken] AS A 
                INNER JOIN 
                [buildVocabulary].[dbo].[textToken] AS B 
                on A.reportID = B.reportID and B.posStart - A.posEnd = 1 and A.posStart > 0 and B.posStart > 0
                WHERE A.tokenID = ? AND B.tokenID = ?;

                '''
        args = [tokenID1, tokenID2]
        cursor.execute(query, args)
        changed_texttoken1 = cursor.fetchall()
        # # print("changed_texttoken first : ", changed_texttoken1)

        


        query = '''
                UPDATE B
                SET B.posStart = -1 * B.posStart, B.posEnd = -1 * B.posEnd
                OUTPUT [INSERTED].reportID, [INSERTED].posStart, [INSERTED].posEnd, [INSERTED].tokenID
                FROM 
                [buildVocabulary].[dbo].[textToken] AS A 
                INNER JOIN 
                [buildVocabulary].[dbo].[textToken] AS B 
                on A.reportID = B.reportID and B.posStart - A.posEnd*-1 = 1 and A.posStart*-1 > 0 and B.posStart > 0
                WHERE A.tokenID = ? AND B.tokenID = ?;
                '''
        args = [tokenID1, tokenID2]
        cursor.execute(query, args)
        changed_texttoken2 = cursor.fetchall()
        # # print("changed_texttoken second: ", changed_texttoken2)



        
        result = {'status':'0'} #成功
        result['data'] = []
        record = {}

        for i in changed_texttoken1:
            # print(i)
            record['reportID'] = i[0]
            record['posStart'] = i[1]
            record['posEnd'] = i[2]
            record['tokenID'] = i[3]
            result['data'].append(copy.deepcopy(record))

        for i in changed_texttoken2:
            # print(i)
            record['reportID'] = i[0]
            record['posStart'] = i[1]
            record['posEnd'] = i[2]
            record['tokenID'] = i[3]
            result['data'].append(copy.deepcopy(record))

        

        conn.commit()
        conn.close()
    return JsonResponse(result)

@csrf_exempt
def getTextToken_3(request):
    #取得
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        query = '''
                EXEC three_word;
                ''' 
        cursor.execute(query)
        textTokenData = cursor.fetchall()
        # # print("textTokenData : ", textTokenData)
        result['data'] = []
        # # print(textTokenData[0][0])
        record = {}

        RE = re.compile(r'([^\u4e00-\u9fa50-9a-zA-Z \n]{1})') 
        RE1 = re.compile(r'([^\u4e00-\u9fa50-9a-zA-Z\(\)\:\[\]\{\}\-\/]{1})')
        number = 1
        for ind,i in enumerate(textTokenData):
            # print(i)

            if request.GET['NoSign'] == 'NS':
                first = RE.findall(i[0])
                second = RE.findall(i[1])
                third = RE.findall(i[2])
                if first == [] and second == [] and third == [] :
                    result['data'].append({
                        'No': number,
                        'First': i[0],
                        'Second': i[1],
                        'Third': i[2],
                        'Times': i[3],
                        'Mergecheck':'<button onclick="merge_3()" class="btn btn-info">Merge</button>',
                    })
                    number += 1
                    
            else:
                first = RE1.findall(i[0])
                second = RE1.findall(i[1])
                third = RE.findall(i[2])
                # print("first : ", first)
                # print("second : ", first)
                if first == [] and second == [] and third == [] :
                    result['data'].append({
                            'No': number,
                            'First': i[0],
                            'Second': i[1],
                            'Third': i[2],
                            'Times': i[3],
                            'Mergecheck':'<button onclick="merge_3()" class="btn btn-info">Merge</button>',
                        })
                    number += 1

        conn.commit()
        conn.close()


    #把posStart posEnd *(-1)
    if request.method == 'PATCH':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        # print(body)
        # # print( body['reportID1'])

        tokenID1 = body['tokenID1']
        tokenID2 = body['tokenID2']
        tokenID3 = body['tokenID3']

        
        # print(tokenID1, tokenID2, tokenID3)


        query = '''
                UPDATE A 
                SET A.posStart = -1 * A.posStart, A.posEnd = -1 * A.posEnd        
                OUTPUT [INSERTED].reportID, [INSERTED].posStart, [INSERTED].posEnd, [INSERTED].tokenID
                FROM 
                [buildVocabulary].[dbo].[textToken] AS A 
                INNER JOIN 
                [buildVocabulary].[dbo].[textToken] AS B 
                on A.reportID = B.reportID and B.posStart - A.posEnd = 1 and A.posStart > 0 and B.posStart > 0
                INNER JOIN 
                [buildVocabulary].[dbo].[textToken] AS C 
                on B.reportID = C.reportID and C.posStart - B.posEnd = 1 and B.posStart > 0 and C.posStart > 0
                WHERE A.tokenID = ? AND B.tokenID = ? AND C.tokenID = ?;

                '''
        args = [tokenID1, tokenID2, tokenID3]
        cursor.execute(query, args)
        changed_texttoken1 = cursor.fetchall()
        # print("changed_texttoken first : ", changed_texttoken1)

        


        query = '''
                UPDATE B
                SET B.posStart = -1 * B.posStart, B.posEnd = -1 * B.posEnd        
                OUTPUT [INSERTED].reportID, [INSERTED].posStart, [INSERTED].posEnd, [INSERTED].tokenID
                FROM 
                [buildVocabulary].[dbo].[textToken] AS A 
                INNER JOIN 
                [buildVocabulary].[dbo].[textToken] AS B 
                on A.reportID = B.reportID and B.posStart - A.posEnd*(-1) = 1 and A.posStart*(-1) > 0 and B.posStart > 0
                INNER JOIN 
                [buildVocabulary].[dbo].[textToken] AS C 
                on B.reportID = C.reportID and C.posStart - B.posEnd = 1 and B.posStart > 0 and C.posStart > 0
                WHERE A.tokenID = ? AND B.tokenID = ? AND C.tokenID = ?;
                '''
        args = [tokenID1, tokenID2, tokenID3]
        cursor.execute(query, args)
        changed_texttoken2 = cursor.fetchall()
        # print("changed_texttoken second: ", changed_texttoken2)



        query = '''
                UPDATE C
                SET C.posStart = -1 * C.posStart, C.posEnd = -1 * C.posEnd        
                OUTPUT [INSERTED].reportID, [INSERTED].posStart, [INSERTED].posEnd, [INSERTED].tokenID
                FROM 
                [buildVocabulary].[dbo].[textToken] AS A 
                INNER JOIN 
                [buildVocabulary].[dbo].[textToken] AS B 
                on A.reportID = B.reportID and B.posStart*(-1) - A.posEnd*(-1) = 1 and A.posStart*(-1) > 0 and B.posStart*(-1) > 0
                INNER JOIN 
                [buildVocabulary].[dbo].[textToken] AS C 
                on B.reportID = C.reportID and C.posStart - B.posEnd*(-1) = 1 and B.posStart*(-1) > 0 and C.posStart > 0
                WHERE A.tokenID = ? AND B.tokenID = ? AND C.tokenID = ?;
                '''
        args = [tokenID1, tokenID2, tokenID3]
        cursor.execute(query, args)
        changed_texttoken3 = cursor.fetchall()
        # print("changed_texttoken Third: ", changed_texttoken3)

        # print("length of all data : ",  len(changed_texttoken1) + len(changed_texttoken2) + len(changed_texttoken3))



        
        result = {'status':'0'} #成功
        result['data'] = []
        record = {}

        for i in changed_texttoken1:
            # print(i)
            record['reportID'] = i[0]
            record['posStart'] = i[1]
            record['posEnd'] = i[2]
            record['tokenID'] = i[3]
            result['data'].append(copy.deepcopy(record))

        for i in changed_texttoken2:
            # print(i)
            record['reportID'] = i[0]
            record['posStart'] = i[1]
            record['posEnd'] = i[2]
            record['tokenID'] = i[3]
            result['data'].append(copy.deepcopy(record))

        for i in changed_texttoken3:
            # print(i)
            record['reportID'] = i[0]
            record['posStart'] = i[1]
            record['posEnd'] = i[2]
            record['tokenID'] = i[3]
            result['data'].append(copy.deepcopy(record))

        

        conn.commit()
        conn.close()
    return JsonResponse(result)
    


@csrf_exempt
def insertTexttoken(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()        

        tokenID1 = request.GET['tokenID1']
        tokenID2 = request.GET['tokenID2']

        query = '''
                select * from [buildVocabulary ].[dbo].textToken as A
                inner join
                [buildVocabulary ].[dbo].textToken as B 
                on A.reportID = B.reportID and B.posStart - A.posEnd = 1 and A.posStart > 0 and B.posStart > 0
                where A.tokenID = ? and B.tokenID = ?
                order by A.reportID, A.posStart
                '''
        args = [tokenID1, tokenID2]
        cursor.execute(query, args)
        position = cursor.fetchall()
        result['data'] = []
        record = {}
        for i in position:
            # print( "reportID = ", i[0], "position from ", i[1], " to ", i[6])
            record['reportID'] = i[0]
            record['posStart'] = i[1]
            record['posEnd'] = i[6]
            result['data'].append(copy.deepcopy(record))
        # print(result)

        result['status'] = '0'
        conn.commit()
        conn.close()



    #插入新的textToken資料([1,1] + [2,2] = [1,2])
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        data = json.loads(request.body)
        # print("positionArray : ", data.get('positionArray[]'))
        # print("newTokenID : ", data.get('newTokenID'))

        positionArray = data.get('positionArray[]')
        newTokenID = data.get('newTokenID')

        for i in positionArray:
            # # print(i)
            # # print( "data = ",i['reportID'] ,"position from ", i['posStart'], " to ", i['posEnd'], "ID = ", newTokenID)
            query = '''
                insert into [buildVocabulary ].[dbo].textToken
                (reportID, posStart, posEnd, tokenID)
                output [INSERTED].reportID, [INSERTED].posStart, [INSERTED].posEnd, [INSERTED].tokenID
                values(?, ?, ?, ?)
                '''
            args = [i['reportID'], i['posStart'], i['posEnd'], newTokenID]            
            cursor.execute(query, args)
            insertedResult = cursor.fetchone()
            # print("insertedResult : ", insertedResult)


        result['status'] = '0'

        conn.commit()
        conn.close()
    return JsonResponse(result)

@csrf_exempt
def insertTexttoken_3(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()        

        tokenID1 = request.GET['tokenID1']
        tokenID2 = request.GET['tokenID2']
        tokenID3 = request.GET['tokenID3']

        query = '''
                select * from [buildVocabulary ].[dbo].textToken as A
                inner join
                [buildVocabulary ].[dbo].textToken as B 
                on A.reportID = B.reportID and B.posStart - A.posEnd = 1 and A.posStart > 0 and B.posStart > 0
                inner join
                [buildVocabulary ].[dbo].textToken as C 
                on B.reportID = C.reportID and C.posStart - B.posEnd = 1 and C.posStart > 0 and B.posStart > 0
                where A.tokenID = ? and B.tokenID = ? and C.tokenID = ?
                order by A.reportID, A.posStart
                '''
        args = [tokenID1, tokenID2, tokenID3]
        cursor.execute(query, args)
        position = cursor.fetchall()
        result['data'] = []
        record = {}
        for i in position:
            # print( "reportID = ", i[0], "position from ", i[1], " to ", i[10])
            record['reportID'] = i[0]
            record['posStart'] = i[1]
            record['posEnd'] = i[10]
            result['data'].append(copy.deepcopy(record))
        # print(result)

        result['status'] = '0'
        conn.commit()
        conn.close()



    #插入新的textToken資料([1,1] + [2,2] = [1,2])
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        data = json.loads(request.body)
        # print("positionArray : ", data.get('positionArray[]'))
        # print("newTokenID : ", data.get('newTokenID'))

        positionArray = data.get('positionArray[]')
        newTokenID = data.get('newTokenID')

        for i in positionArray:
            # # print(i)
            # # print( "data = ",i['reportID'] ,"position from ", i['posStart'], " to ", i['posEnd'], "ID = ", newTokenID)
            query = '''
                insert into [buildVocabulary ].[dbo].textToken
                (reportID, posStart, posEnd, tokenID)
                output [INSERTED].reportID, [INSERTED].posStart, [INSERTED].posEnd, [INSERTED].tokenID
                values(?, ?, ?, ?)
                '''
            args = [i['reportID'], i['posStart'], i['posEnd'], newTokenID]            
            cursor.execute(query, args)
            insertedResult = cursor.fetchone()
            # print("insertedResult : ", insertedResult)


        result['status'] = '0'

        conn.commit()
        conn.close()
    return JsonResponse(result)



    #新增至tokenRE並回傳tokenID.RE.tokenREID
@csrf_exempt
def inserttokenRE(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #result = cursor.execute("select * from [buildVocabulary ].[dbo].[Vocabulary]")
        #取得post資料
        result['data'] = []
        record = {}
        record['tokenID'] = request.POST.get('tokenID')
        record['RE'] = request.POST.get('RE')


        query = 'select * from [buildVocabulary ].[dbo].[tokenRE] where tokenID = ? and RE = ?;'
        args = [int(request.POST.get('tokenID')), request.POST.get('RE') ]
        cursor.execute(query, args)
        tokenREID_original = cursor.fetchall()
        # print("tokenREID_original : ", tokenREID_original)
        if tokenREID_original == []:
            #插入資料表
            query = 'INSERT into [buildVocabulary ].[dbo].[tokenRE] (tokenID, RE) OUTPUT [INSERTED].tokenREID VALUES (?, ?);'
            args = [int(request.POST.get('tokenID')), request.POST.get('RE') ]
            # print(args)
            cursor.execute(query, args)
            tokenREID = cursor.fetchall()
            # print(tokenREID[0])       
            result['status'] = '0'
            record['tokenREID'] = tokenREID[0][0]            
            result['data'].append(record)
            # print("data saved(tokenRE)")
        else:
            result['status'] = 'already_exist'
    
        conn.commit()
        conn.close()

    return JsonResponse(result)

    #新增至tokenREItem並回傳tokenREID.serialNo.itemName.tokenREItemID
@csrf_exempt
def inserttokenREItem(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
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
        query = 'INSERT into [buildVocabulary].[dbo].[tokenREItem] (tokenREID, serialNo, itemName) OUTPUT [INSERTED].tokenREID VALUES (?, ?, ?);'
        args = [int(request.POST.get('tokenREID')), request.POST.get('serialNo'), request.POST.get('itemName') ]
        # print(args)
        cursor.execute(query, args)
        tokenREItemID = cursor.fetchall()
        # print(tokenREItemID[0])
        result['status'] = '0'
        record['tokenREItemID'] = tokenREItemID[0][0]
        result['data'].append(record)
        # print("data saved(tokenREItem)")
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
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        Token = request.GET.getlist('Name[]')
        tokenID = []
        tokenType = []
        print("Token : ", Token)

        for i in range(len(Token)):
            query = 'SELECT * FROM [buildVocabulary ].[dbo].[Vocabulary] WHERE token = ?;'
            args = [Token[i]]
            cursor.execute(query, args)
            token = cursor.fetchone()
            print("token : ", token)
            if token:
                tokenID.append(token.tokenID)
                if token.token == '[NUM]':
                    tokenType.append('U')
                else:                    
                    tokenType.append(token.tokenType)
        # print(token)
        # # print(tokenType)
# 
        # 有找到
        if token:
            result['status'] = '0'
            result['tokenID'] = tokenID
            result['tokenType'] = tokenType
        
        print("result : ", result)
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
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        TokenID = request.GET.getlist('tokenID[]')
        RE = []
        TokenREID = []

        for i in range(len(TokenID)):
            query = 'SELECT * FROM [buildVocabulary ].[dbo].[tokenRE] WHERE tokenID = ?;'
            args = [TokenID[i]]
            # # print(args)
            ## print(query)
            cursor.execute(query, args)
            tokenREID = cursor.fetchone()
            if tokenREID:
                RE.append(tokenREID.RE)
                TokenREID.append(tokenREID.tokenREID)
        # print("RE : ", RE)
        # print("TokenREID : ", TokenREID)

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
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        query = 'SELECT * FROM [buildVocabulary ].[dbo].[analyseText];'
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
        #     # print(token[0])
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
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        # query = 'SELECT * FROM [buildVocabulary].[dbo].[analyseText] where reportID = 10002;'
        # query = 'SELECT * FROM analyseText;'
        query = 'SELECT * FROM [buildVocabulary].[dbo].[analyseText] where reportID >= ? and reportID <= ?'
        args = [request.GET['reportID1'], request.GET['reportID2']]
        
        cursor.execute(query, args)
        reportID = cursor.fetchall()
        # # print(reportID)

        #有找到
        if reportID != None:
            result['status'] = '0'
            result['data'] = []
            record = {}
            for item in reportID:
                if item.analysed == 0:
                    record[str(item.reportID)] = item.reportText
                else:
                    record[str(item.reportID)] = item.residualText
            result['data'].append(record)
        #     # print(token[0])
        # print(result)
        
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
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        #插入資料表
        query = 'SELECT * FROM [buildVocabulary ].[dbo].[analyseText] where reportID = ?;'
        args = [request.GET['reportID']]
        cursor.execute(query, args)
        reportID = cursor.fetchone()

        #有找到
        if reportID != None:
            ## print(reportID.reportText)
            result['status'] = '0'
            result['reportText'] = []
            # result['reportText'].append(reportID.reportText)
            if reportID.analysed == 0:
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
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        # # print("patch in")
        #更新資料表
        query = 'update [buildVocabulary ].[dbo].[analyseText]  set analysed = ?, residualText = ? output INSERTED.reportID,INSERTED.reportText,INSERTED.residualText where reportID = ?;'
        raw = request.body.decode('utf-8')
        body = json.loads(raw)
        # # print('data : ' + data.getlist['residualText'])
        # print( body['reportID'])
        
        args = [1, body['residualText'], body['reportID']]
        
        cursor.execute(query, args)
        reportID = cursor.fetchone()

        #有找到
        if reportID != None:
            ## print(reportID.reportText)
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
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        # # print(request.POST)
        reportID = request.POST.getlist('reportID[]')
        posStart = request.POST.getlist('posStart[]')
        posEnd = request.POST.getlist('posEnd[]')
        tokenID = request.POST.getlist('tokenID[]')
        # # print(len(reportID), len(posStart), len(posEnd), len(tokenID))
        # # print(reportID, posStart, posEnd, tokenID)
        for i in range(len(reportID)):
            # # print(reportID[i], posStart[i], posEnd[i], tokenID[i])
            query = "select * from [buildVocabulary ].[dbo].[Vocabulary] where token = ?"
            args = [tokenID[i]]
            cursor.execute(query, args)
            id = cursor.fetchone()
            
            result['status'] = '0'
            if id.tokenType == 'U':
                result = {'status':'U'}
            #插入資料表
            query = 'INSERT into [buildVocabulary ].[dbo].[textToken] (reportID, posStart, posEnd, tokenID) OUTPUT [INSERTED].reportID, [INSERTED].posStart VALUES (?, ?, ?, ?);'
            args = [reportID[i], posStart[i], posEnd[i], id.tokenID]
            # # print("args : ", args)
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
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        data = []
        #取締一個取成功
        if request.is_ajax():
            # # print('Raw Data: "%s"' % request.body)
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            for i in body:
                data.append(i)
            # # print("data : ", data)
            # content = body[0]
            # # print('Data: "%s"' % content['year'])
        tokenIDArray = []
        tokentypeArray = []
        tokenREIDArray = []
        tokenREItemIDArray = []
                                        
        temp = []
        
        for i in range(len(data)):
            temp.clear()
            # # print("data[i] : ", data[i])
            if data[i]['tokenID']:
                #查詢tokenType
                query = 'SELECT * FROM [buildVocabulary ].[dbo].[Vocabulary] where tokenID = ?;'
                args = [data[i]['tokenID']]
                cursor.execute(query, args)
                tokenType = cursor.fetchone()
                # # print("tokenType ", tokenID.tokenType)
                if tokenType:
                    tokenIDArray.append(tokenType.tokenID)
                    tokentypeArray.append(tokenType.tokenType)

                if tokenType.tokenType != 'T' or tokenType.tokenType != 'U':
                    #查詢tokenREID
                    # print("tokentype is not T or U")
                    query = 'SELECT * FROM [buildVocabulary ].[dbo].[tokenRE] where tokenID = ?;'
                    args = [data[i]['tokenID']]
                    cursor.execute(query, args)
                    tokenREID = cursor.fetchone()
                    if tokenREID:
                        tokenREIDArray.append(tokenREID.tokenREID)
                    # print("data[i].keys()", data[i].keys())
                    for j in range(len(list(data[i].keys()))):
                        if tokenType.tokenType != 'T' or tokenType.tokenType != 'U':
                            # # print(j)
                            #查詢tokenREItemID
                            query = 'SELECT * FROM [buildVocabulary].[dbo].[tokenREItem] where tokenREID = ? and itemName = ?;'
                            args = [tokenREID.tokenREID, list(data[i].keys())[j]]
                            cursor.execute(query, args)
                            tokenREItemID = cursor.fetchone()
                        if tokenREItemID:
                            temp.append(tokenREItemID.tokenREItemID)
                            # print("temp : ", temp)
                        # print("j : ", j)
                        # print("len : ", len(list(data[i].keys()))-1)
                        if len(list(data[i].keys()))-1 == j:
                            tokenREItemIDArray.append(copy.deepcopy(temp))
                            # print("tokenREItemIDArray : ", tokenREItemIDArray)

        record = {}
        result['data'] = []
        record['tokenID'] = tokenIDArray
        record['tokenREID'] = tokenREIDArray
        record['tokenType'] = tokentypeArray
        record['tokenREItemID'] = tokenREItemIDArray
        result['data'].append(record)
        # # print(result)
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
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        # # print("request: ", request.POST.getlist('tokenID[]'))

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
        # # print("tokenREItemID: ", tokenREItemID)

        # 處理Value二維陣列(用逗號分開)
        for i in range(len(Value)):
            Value[i] = Value[i].split(',')
        # print("Value: ", len(Value))
        # print("Value: ", Value)
        
        # # print("tokenREItemID: ", len(tokenREItemID))
        tokenREItemIDIndex = 0
        #插入資料表()
        for i in range(len(reportID)):
            # # print("i : ", i)
            if tokenType[i]  != 'T' or tokenType[i]  != 'U':
                # print("TU")
                for j in range(len(tokenREItemID[tokenREItemIDIndex])):
                    # # print("j : ", j)
                    # # print(tokenType[i])
                    # # print(reportID[i], posStart[i], tokenREItemID[i][j], Value[i][j])
                    query = 'INSERT into [buildVocabulary ].[dbo].[extractedValueFromToken] (reportID, posStart, tokenREItemID, extractedValue) OUTPUT [INSERTED].reportID, [INSERTED].posStart VALUES (?, ?, ?, ?);'
                    Value[tokenREItemIDIndex][j] = Value[tokenREItemIDIndex][j].replace("|", ",")
                    args = [reportID[i], posStart[i], tokenREItemID[tokenREItemIDIndex][j], Value[tokenREItemIDIndex][j]]
                    # print(args)
                    cursor.execute(query, args)
                tokenREItemIDIndex += 1

        conn.commit()
        conn.close()
        result['status'] = '0'
        # # print(result)
    return JsonResponse(result)


@csrf_exempt
def getToken(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設失敗
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824' 
        password = 'test81218' 
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()
        # # print("request: ", request.POST.getlist('tokenID[]'))

        #取得資料
        tokenID1 = request.POST.getlist('tokenID1[]')
        tokenID2 = request.POST.getlist('tokenID2[]')
        # # print(tokenID1)        
        # # print(tokenID2)
        token1 = []
        token2 = []
        for i in tokenID1:
            # # print(i)
            query = 'select * from [buildVocabulary ].[dbo].[Vocabulary] where tokenID = ?;'
            args = [i]
            cursor.execute(query, args)
            token = cursor.fetchone()
            # # print(token.token)
            token1.append(token.token)

        for i in tokenID2:
            # # print(i)
            query = 'select * from [buildVocabulary ].[dbo].[Vocabulary] where tokenID = ?;'
            args = [i]
            cursor.execute(query, args)
            token = cursor.fetchone()
            # # print(token.token)
            token2.append(token.token)

        # # print(token1)
        # # print(token2)
        result['data'] = []
        record = {}
        record['token1'] = token1
        record['token2'] = token2
        result['data'].append(record)
        conn.commit()
        conn.close()
        result['status'] = '0'
        # # print(result)
    return JsonResponse(result)

        #讀取tokenID再檢查textToken是否為正值
@csrf_exempt
def getTokenIDCheckTextToken(request):
    if request.method == 'POST':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        token = request.POST.getlist('token[]')
        # # print(token)

        PNarray = []
        for i, t in enumerate(token):
            pn = 0
            # print("Index:", i, "Token:", t)
            query = 'SELECT * FROM [buildVocabulary ].[dbo].[Vocabulary] where token = ?;'
            args = [t]
            # # print(i)

            
            cursor.execute(query, args)
            tokenID = cursor.fetchone()

            # 有找到
            if tokenID != None:
                # # print(tokenID.tokenID)
                
                query = 'SELECT * FROM [buildVocabulary ].[dbo].[textToken] where tokenID = ?;'
                args = [tokenID.tokenID]

                cursor.execute(query, args)
                textTokenData = cursor.fetchall()

                if textTokenData != []:
                    # # print(textTokenData)
                    result['status'] = '0'
                    for jcount, j in enumerate(textTokenData) :
                        result['status'] = '0'
                        if (j[1] > 0 and j[2] > 0) == False:
                            # print("negative")
                            PNarray.append(1)
                            pn = 1      
                            break
                        # print("jcount :", jcount, " len : ", len(textTokenData))
                        if jcount == len(textTokenData)-1 and pn == 0:
                            PNarray.append(0)
                else:
                    pn = 0      
                    PNarray.append(2)
        
        result['data'] = PNarray
        # # print("PNarray : ", PNarray)
        conn.commit()
        conn.close()
    return JsonResponse(result)



@csrf_exempt
def getNextWord(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        num = int(request.GET['word'])
        firstToken = request.GET['firstToken']
        # print(firstToken)
        # # print(token)

        token = ''
        mergetoken = ''
        innerjoinpos = ''
        innerjointoken = ''
        groupby = ''
        #如果>=3就遞迴增加
        if num >= 3:
            for i in range(num-2):
                token += f', c{i+5}.token as token{i+5}'
                mergetoken += f' + c{i+5}.token'
                if i == 0:
                    innerjoinpos += f' inner join [buildVocabulary ].[dbo].[textToken] as b{i+4} on a1.reportID = b{i+4}.reportID and (a1.posEnd + 1) = b{i+4}.posStart and a1.posStart > 0 and b{i+4}.posStart > 0'
                else:
                    innerjoinpos += f' inner join [buildVocabulary ].[dbo].[textToken] as b{i+4} on a1.reportID = b{i+4}.reportID and (b{i+3}.posEnd + 1) = b{i+4}.posStart and b{i+3}.posStart > 0 and b{i+4}.posStart > 0'

                innerjointoken += f' inner join [buildVocabulary ].[dbo].[Vocabulary] as c{i+5} on b{i+4}.tokenID = c{i+5}.tokenID'
                groupby += f' , c{i+5}.token'
                text = innerjoinpos
        #如果<3就固定抓三個字
        else:
            token = f''' , a5.token as token3'''
            mergetoken = f''' + a5.token'''
            innerjoinpos = f''' inner join [buildVocabulary ].[dbo].[textToken] as a4 on a1.reportID = a4.reportID and (a1.posEnd + 1) = a4.posStart and a1.posStart > 0 and a4.posStart > 0'''
            innerjointoken = f''' inner join [buildVocabulary ].[dbo].[Vocabulary] as a5 on a4.tokenID = a5.tokenID'''
            groupby = f''' , a5.token'''
            text = innerjoinpos

        query = f'''
                select textTokenData.* from (
                '''
        query +=f'''
                 select a2.token as token1, a3.token as token2
                '''
        # query +=f''' , a{num+2}.token as token{num}'''
        query += token

        query +=f''' , COUNT(*) as times, a2.token + a3.token'''

        # query +=f''' + a{num+2}.token'''
        query += mergetoken

        query +=f''' as mergeToken
                from [buildVocabulary ].[dbo].[textToken] as a0
                inner join [buildVocabulary ].[dbo].[textToken] as a1 on a0.reportID = a1.reportID and (a0.posEnd + 1) = a1.posStart and a0.posStart > 0 and a1.posStart > 0
                '''
        # query +=f''' inner join [buildVocabulary ].[dbo].[textToken] as a4 on a1.reportID = a{num+1}.reportID and (a1.posEnd + 1) = a{num+1}.posStart and a1.posStart > 0 and a{num+1}.posStart > 0'''
        query += innerjoinpos
        # 找第一個字
        if firstToken != "":
            query +=f''' inner join [buildVocabulary ].[dbo].[Vocabulary] as a2 on a0.tokenID = a2.tokenID and a2.token = '{firstToken}'
                    inner join [buildVocabulary ].[dbo].[Vocabulary] as a3 on a1.tokenID = a3.tokenID
                    '''
        else:
            query +=f''' inner join [buildVocabulary ].[dbo].[Vocabulary] as a2 on a0.tokenID = a2.tokenID
                    inner join [buildVocabulary ].[dbo].[Vocabulary] as a3 on a1.tokenID = a3.tokenID
                    '''
        # query +=f''' inner join [buildVocabulary ].[dbo].[Vocabulary] as a{num+2} on a{num+1}.tokenID = a{num+2}.tokenID'''
        query += innerjointoken
        query +=f''' group by a2.token, a3.token
                '''
        # query +=f''' , a{num+2}.token'''
        query += groupby
        
        query +=f'''
                ) as textTokenData
                left join [buildVocabulary ].[dbo].[Vocabulary] as word on textTokenData.mergeToken = word.token
                where word.tokenID is null
                order by times desc;
                '''
        # print("query : ", query)
        # print("text : ", text)
        
        
        cursor.execute(query)
        texttoken = cursor.fetchall()
        # print("texttoken : ", texttoken)
        # for i in texttoken:
        #     # if i[0] == '[NUM]':
        #     print("texttoken : ", i)
        result['data'] = []
        record = {}
        if texttoken != []:
            record['reportID'] = texttoken[0][num + 1]

            for ind,i in enumerate(texttoken):
                # print("i[0] : ",i[0])
                dataDict = {}
                if num >= 3:
                    # print("i[ind] : ", type(i))
                    if type(i) != int:
                        for index,j in enumerate(i):
                            # print("j : ", j)
                            # print("i[index] : ", i[index])
                            dataDict[str(index + 1)] = j
                    dataDict["No"] = ind+1
                    dataDict["times"] = i[len(i)-2]
                    # print("dataDict : ", dataDict)
                    result['data'].append(dataDict)
                else:
                    print(i[len(i)-2])
                    result['data'].append({
                        'No': ind+1,
                        '1': i[0],
                        '2': i[1],
                        '3': i[2],
                        'times': i[len(i)-2],
                    })

        # print("PNarray : ", PNarray)
        conn.commit()
        conn.close()
    return JsonResponse(result)

@csrf_exempt
def getNextWordReport(request):
    if request.method == 'GET':
        #取得資料
        result = {'status':'1'} #預設沒找到
        
        #建立連線
        server = '172.31.6.22' 
        database = 'buildVocabulary' 
        username = 'N824'
        password = 'test81218'
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+'; DATABASE='+database+'; ENCRYPT=yes; UID='+username+'; PWD='+ password +'; TrustServerCertificate=yes;')
        cursor = conn.cursor()

        num = int(request.GET['word'])
        firstToken = request.GET['firstToken']
        print(firstToken)
        # # print(token)

        token = ''
        mergetoken = ''
        innerjoinpos = ''
        innerjointoken = ''
        groupby = ''
        #如果>=3就遞迴增加
        if num >= 3:
            for i in range(num-2):
                token += f', c{i+5}.token as token{i+5}'
                mergetoken += f' + c{i+5}.token'
                if i == 0:
                    innerjoinpos += f' inner join [buildVocabulary ].[dbo].[textToken] as b{i+4} on a1.reportID = b{i+4}.reportID and (a1.posEnd + 1) = b{i+4}.posStart and a1.posStart > 0 and b{i+4}.posStart > 0'
                else:
                    innerjoinpos += f' inner join [buildVocabulary ].[dbo].[textToken] as b{i+4} on a1.reportID = b{i+4}.reportID and (b{i+3}.posEnd + 1) = b{i+4}.posStart and b{i+3}.posStart > 0 and b{i+4}.posStart > 0'

                innerjointoken += f' inner join [buildVocabulary ].[dbo].[Vocabulary] as c{i+5} on b{i+4}.tokenID = c{i+5}.tokenID'
                groupby += f' , c{i+5}.token'
                text = innerjoinpos
        #如果<3就固定抓三個字
        else:
            token = f''' , a5.token as token3'''
            mergetoken = f''' + a5.token'''
            innerjoinpos = f''' inner join [buildVocabulary ].[dbo].[textToken] as a4 on a1.reportID = a4.reportID and (a1.posEnd + 1) = a4.posStart and a1.posStart > 0 and a4.posStart > 0'''
            innerjointoken = f''' inner join [buildVocabulary ].[dbo].[Vocabulary] as a5 on a4.tokenID = a5.tokenID'''
            groupby = f''' , a5.token'''
            text = innerjoinpos

        query = f'''
                select textTokenData.* from (
                '''
        query +=f'''
                 select a2.token as token1, a3.token as token2
                '''
        # query +=f''' , a{num+2}.token as token{num}'''
        query += token

        query +=f''' , COUNT(*) as times, a2.token + a3.token'''

        # query +=f''' + a{num+2}.token'''
        query += mergetoken

        query +=f''' as mergeToken
                from [buildVocabulary ].[dbo].[textToken] as a0
                inner join [buildVocabulary ].[dbo].[textToken] as a1 on a0.reportID = a1.reportID and (a0.posEnd + 1) = a1.posStart and a0.posStart > 0 and a1.posStart > 0
                '''
        # query +=f''' inner join [buildVocabulary ].[dbo].[textToken] as a4 on a1.reportID = a{num+1}.reportID and (a1.posEnd + 1) = a{num+1}.posStart and a1.posStart > 0 and a{num+1}.posStart > 0'''
        query += innerjoinpos
        # 找第一個字
        if firstToken != "":
            query +=f''' inner join [buildVocabulary ].[dbo].[Vocabulary] as a2 on a0.tokenID = a2.tokenID and a2.token = '{firstToken}' and a2.tokenType != 'E'
                    inner join [buildVocabulary ].[dbo].[Vocabulary] as a3 on a1.tokenID = a3.tokenID
                    '''
        else:
            query +=f''' inner join [buildVocabulary ].[dbo].[Vocabulary] as a2 on a0.tokenID = a2.tokenID
                    inner join [buildVocabulary ].[dbo].[Vocabulary] as a3 on a1.tokenID = a3.tokenID
                    '''
        # query +=f''' inner join [buildVocabulary ].[dbo].[Vocabulary] as a{num+2} on a{num+1}.tokenID = a{num+2}.tokenID'''
        query += innerjointoken
        query +=f''' group by a2.token, a3.token
                '''
        # query +=f''' , a{num+2}.token'''
        query += groupby
        
        query +=f'''
                ) as textTokenData
                left join [buildVocabulary ].[dbo].[Vocabulary] as word on textTokenData.mergeToken = word.token
                where word.tokenID is null
                order by times desc;
                '''
        print("query : ", query)
        print("text : ", text)
        
        
        cursor.execute(query)
        texttoken = cursor.fetchall()
        print("texttoken : ", texttoken)
        # for i in texttoken:
        #     # if i[0] == '[NUM]':
        #     print("texttoken : ", i)
        result['data'] = []
        record = {}
        if texttoken != []:
            record['reportID'] = texttoken[0][num + 1]

            for ind,i in enumerate(texttoken):
                # print("i[0] : ",i[0])
                dataDict = {}
                if num >= 3:
                    # print("i[ind] : ", type(i))
                    if type(i) != int:
                        for index,j in enumerate(i):
                            # print("j : ", j)
                            # print("i[index] : ", i[index])
                            dataDict[str(index + 1)] = j
                    dataDict["No"] = ind+1
                    dataDict["times"] = i[len(i)-2]
                    # print("dataDict : ", dataDict)
                    result['data'].append(dataDict)
                else:
                    print(i[len(i)-2])
                    result['data'].append({
                        'No': ind+1,
                        '1': i[0],
                        '2': i[1],
                        '3': i[2],
                        'times': i[len(i)-2],
                    })

        # print("PNarray : ", PNarray)
        conn.commit()
        conn.close()
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


    
