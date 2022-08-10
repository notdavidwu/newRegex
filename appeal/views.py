from django.shortcuts import render,HttpResponse
from django.template.context import RequestContext
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import pathlib


@csrf_exempt
def appeal(request):
    au = request.session.get('au')
    return render(request, 'appeal/appeal.html',{'au':au})


@csrf_exempt
def appeallist(request):
    query = '''select * from appeal order by appealState asc,appealTime desc'''
    cursor = connections['default'].cursor()
    cursor.execute(query)
    appealID = []
    appealDate = []
    appealTime = []
    ResidentNo = []
    appealText = []
    appealcalldate = []
    appealState = []
    res = cursor.fetchall()
    for i in range(len(res)):
        appealID.append(res[i][0])
        appealDate.append(res[i][1])
        appealTime.append(res[i][2])
        ResidentNo.append(res[i][3])
        appealText.append(res[i][4])
        appealcalldate.append(res[i][5])
        appealState.append(res[i][6])
        #print(appealID)
    return JsonResponse({
        'appealID': appealID,'appealDate': appealDate,'appealTime': appealTime,'ResidentNo': ResidentNo,
        'appealText': appealText,'appealcalldate':appealcalldate,'appealState': appealState})


@csrf_exempt
def appealdealwith(request):
    appealID = request.POST.get('appealID')
    #print(appealID)
    query = '''update appeal set appealState =1 where appealID ='''+appealID
    #print(query)
    cursor = connections['default'].cursor()
    cursor.execute(query)

    query2="select appealID from appeal"
    cursor = connections['default'].cursor()
    cursor.execute(query2)
    appealID = []
    res = cursor.fetchall()
    for i in range(len(res)):
        appealID.append(res[i][0])

    return JsonResponse({'appealID':appealID})

@csrf_exempt
def SearchWord(request):
    Wordnum= request.GET.get('Wordnum')
    Word1 = request.GET.get('Word1')
    Word2 = request.GET.get('Word2')
    Word3 = request.GET.get('Word3')
    #query = "insert into appeal(appealDate,appealTime,ResidentNo,appealText,appealcalldate,appealState)"+"values('"+appealDate+"',Convert(varchar(8),'"+appealTime+"',108),'A-4F-5','"+appealreason+"',Convert(varchar(8),Getdate(),108),0)"
    #print(query)
    #print(Wordnum)
    #print(Word1)
    #print(Word2)
    #print(Word3)
    if Wordnum=='2':
        cursor = connections['NursingRecord'].cursor()
        query = f'''select top 1 a.*,b.Token as 'Token5',b.TokenType as 'TokenType5',c.Token as 'Token6',c.TokenType as 'TokenType6' from mergeToken as a
                    inner join ontologyTrans as b on a.Token_5=b.TokenID
                    inner join ontologyTrans as c on a.Token_6=c.TokenID
                    and b.TokenType='{Word1}' and c.TokenType='{Word2}'
                    where merged=0 and Token_7 is null
                    order by Sum desc'''
        #print(query)
        cursor.execute(query)
        Item = []
        Token_5 = []
        Token_6 = []
        Token_7 = []
        Sum = []
        merged = []
        Token5 = []
        TokenType5 = []
        Token6 = []
        TokenType6 = []
        res = cursor.fetchall()
        for i in range(len(res)):
            Item.append(res[i][0])
            Token_5.append(res[i][1])
            Token_6.append(res[i][2])
            Token_7.append(res[i][3])
            Sum.append(res[i][4])
            merged.append(res[i][5])
            Token5.append(res[i][6])
            TokenType5.append(res[i][7])
            Token6.append(res[i][8])
            TokenType6.append(res[i][9])
        return JsonResponse({
            'Item': Item,'Token_5': Token_5,'Token_6': Token_6,'Token_7': Token_7,
            'Sum': Sum,'merged':merged,'Token5': Token5,'TokenType5': TokenType5,'Token6':Token6,'TokenType6': TokenType6})
    elif Wordnum=='3':
        cursor = connections['NursingRecord'].cursor()
        query = f'''select top 1 a.*,b.Token as 'Token5',b.TokenType as 'TokenType5',c.Token as 'Token6',c.TokenType as 'TokenType6',d.Token as 'Token6',d.TokenType as 'TokenType7' from mergeToken as a
                    inner join ontologyTrans as b on a.Token_5=b.TokenID
                    inner join ontologyTrans as c on a.Token_6=c.TokenID
                    inner join ontologyTrans as d on a.Token_7=d.TokenID
                    and b.TokenType='{Word1}' and c.TokenType='{Word2}' and d.TokenType='{Word3}'
                    where merged=0 and Token_7 is not null
                    order by Sum desc'''
        #print(query)
        cursor.execute(query)
        Item = []
        Token_5 = []
        Token_6 = []
        Token_7 = []
        Sum = []
        merged = []
        Token5 = []
        TokenType5 = []
        Token6 = []
        TokenType6 = []
        Token7 = []
        TokenType7 = []
        res = cursor.fetchall()
        for i in range(len(res)):
            Item.append(res[i][0])
            Token_5.append(res[i][1])
            Token_6.append(res[i][2])
            Token_7.append(res[i][3])
            Sum.append(res[i][4])
            merged.append(res[i][5])
            Token5.append(res[i][6])
            TokenType5.append(res[i][7])
            Token6.append(res[i][8])
            TokenType6.append(res[i][9])
            Token7.append(res[i][10])
            TokenType7.append(res[i][11])
        return JsonResponse({
            'Item': Item,'Token_5': Token_5,'Token_6': Token_6,'Token_7': Token_7,
            'Sum': Sum,'merged':merged,'Token5': Token5,'TokenType5': TokenType5,'Token6':Token6,'TokenType6': TokenType6,'Token7':Token7,'TokenType7':TokenType7})
        

@csrf_exempt
def back_word(request):
    array = request.GET.getlist("ArrTest")
    #print(array)
    cursor = connections['NursingRecord'].cursor()
    if len(array)==2:
        query = f'''select Token_7,b.Token,count(*) as 'Sum2' from nGram as a 
                    inner join ontologyTrans as b on a.Token_7=b.TokenID
                    where Token_5={array[0]} and Token_6={array[1]}
                    and PosStart>0
                    group by Token_7,b.Token
                    order by Sum2 desc'''
    elif len(array)==3:
        query = f'''select Token_8,b.Token,count(*) as 'Sum2' from nGram as a 
                    inner join ontologyTrans as b on a.Token_8=b.TokenID
                    where Token_5={array[0]} and Token_6={array[1]} and Token_7={array[2]}
                    and PosStart>0
                    group by Token_8,b.Token
                    order by Sum2 desc'''
    #print(query)
    cursor.execute(query)
    TokenID = []
    Token = []
    Sum = []
    res = cursor.fetchall()
    for i in range(len(res)):
        TokenID.append(res[i][0])
        Token.append(res[i][1])
        Sum.append(res[i][2])
    return JsonResponse({'TokenID':TokenID,'Token':Token,'Sum':Sum})


@csrf_exempt
def front_word(request):
    array = request.GET.getlist("ArrTest")
    #rint(array)
    cursor = connections['NursingRecord'].cursor()
    if len(array)==2:
        query = f'''select Token_4,b.Token,count(*) as 'Sum2' from nGram as a 
                    inner join ontologyTrans as b on a.Token_4=b.TokenID
                    where Token_5={array[0]} and Token_6={array[1]}
                    and PosStart>0
                    group by Token_4,b.Token
                    order by Sum2 desc'''
    elif len(array)==3:
        query = f'''select Token_4,b.Token,count(*) as 'Sum2' from nGram as a 
                    inner join ontologyTrans as b on a.Token_4=b.TokenID
                    where Token_5={array[0]} and Token_6={array[1]} and Token_7={array[2]}
                    and PosStart>0
                    group by Token_4,b.Token
                    order by Sum2 desc'''
    #print(query)
    cursor.execute(query)
    TokenID = []
    Token = []
    Sum = []
    res = cursor.fetchall()
    for i in range(len(res)):
        TokenID.append(res[i][0])
        Token.append(res[i][1])
        Sum.append(res[i][2])
    
    return JsonResponse({'TokenID':TokenID,'Token':Token,'Sum':Sum})




@csrf_exempt
def Schedule(request):
    Wordnum= request.GET.get('Wordnum')
    Word1 = request.GET.get('Word1')
    Word2 = request.GET.get('Word2')
    Word3 = request.GET.get('Word3')
    #query = "insert into appeal(appealDate,appealTime,ResidentNo,appealText,appealcalldate,appealState)"+"values('"+appealDate+"',Convert(varchar(8),'"+appealTime+"',108),'A-4F-5','"+appealreason+"',Convert(varchar(8),Getdate(),108),0)"
    #print(query)
    if Wordnum=='2':
        cursor = connections['NursingRecord'].cursor()
        query = f'''select top 1000 a.*,b.Token as 'Token5',b.TokenType as 'TokenType5',c.Token as 'Token6',c.TokenType as 'TokenType6' from mergeToken as a
                    inner join ontologyTrans as b on a.Token_5=b.TokenID
                    inner join ontologyTrans as c on a.Token_6=c.TokenID
                    and b.TokenType='{Word1}' and c.TokenType='{Word2}'
                    and Token_7 is null
                    order by Sum desc'''
        cursor.execute(query)
        #print(query)
        Item = []
        Token_5 = []
        Token_6 = []
        Token_7 = []
        Sum = []
        merged = []
        Token5 = []
        TokenType5 = []
        Token6 = []
        TokenType6 = []
        res = cursor.fetchall()
        for i in range(len(res)):
            Item.append(res[i][0])
            Token_5.append(res[i][1])
            Token_6.append(res[i][2])
            Token_7.append(res[i][3])
            Sum.append(res[i][4])
            merged.append(res[i][5])
            Token5.append(res[i][6])
            TokenType5.append(res[i][7])
            Token6.append(res[i][8])
            TokenType6.append(res[i][9])
        return JsonResponse({
            'Item': Item,'Token_5': Token_5,'Token_6': Token_6,'Token_7': Token_7,
            'Sum': Sum,'merged':merged,'Token5': Token5,'TokenType5': TokenType5,'Token6':Token6,'TokenType6': TokenType6})
    elif Wordnum=='3':
        cursor = connections['NursingRecord'].cursor()
        query = f'''select top 1000 a.*,b.Token as 'Token5',b.TokenType as 'TokenType5',c.Token as 'Token6',c.TokenType as 'TokenType6',d.Token as 'Token7',d.TokenType as 'TokenType7' from mergeToken as a
                    inner join ontologyTrans as b on a.Token_5=b.TokenID
                    inner join ontologyTrans as c on a.Token_6=c.TokenID
                    inner join ontologyTrans as d on a.Token_7=d.TokenID
                    and b.TokenType='{Word1}' and c.TokenType='{Word2}' and d.TokenType='{Word3}'
                    and Token_7 is not null
                    order by Sum desc'''
        #print(query)
        cursor.execute(query)
        Item = []
        Token_5 = []
        Token_6 = []
        Token_7 = []
        Sum = []
        merged = []
        Token5 = []
        TokenType5 = []
        Token6 = []
        TokenType6 = []
        Token7 = []
        TokenType7 = []
        res = cursor.fetchall()
        for i in range(len(res)):
            Item.append(res[i][0])
            Token_5.append(res[i][1])
            Token_6.append(res[i][2])
            Token_7.append(res[i][3])
            Sum.append(res[i][4])
            merged.append(res[i][5])
            Token5.append(res[i][6])
            TokenType5.append(res[i][7])
            Token6.append(res[i][8])
            TokenType6.append(res[i][9])
            Token7.append(res[i][10])
            TokenType7.append(res[i][11])
        return JsonResponse({
            'Item': Item,'Token_5': Token_5,'Token_6': Token_6,'Token_7': Token_7,
            'Sum': Sum,'merged':merged,'Token5': Token5,'TokenType5': TokenType5,'Token6':Token6,'TokenType6': TokenType6,'Token7':Token7,'TokenType7':TokenType7})
 
@csrf_exempt
def update_schedule(request):
    array = request.GET.getlist("ArrTest")
    #print(array)
    cursor = connections['NursingRecord'].cursor()
    if(len(array)==2):
        query = f'''update mergeToken set merged=1  
                    where Token_5={array[0]} and Token_6={array[1]} and Token_7 is null'''
    elif(len(array)==3):
        query = f'''update mergeToken set merged=1  
                    where Token_5={array[0]}  and Token_6={array[1]} and Token_7={array[2]}'''
    cursor.execute(query)
    #print(query)
    return JsonResponse({})       

@csrf_exempt
def select_huge_data(request):
    array = request.GET.getlist("ChangeableArrTest")
    leng = request.GET.get("len")
    
    #print(leng)
    if int(leng)%2==0:
        #print('///////////////////////////////////////////////////')
        start=5-((int(leng)/2)-1)
        t=''
        join=''
        #print(int(start))
        #print(int(start)+int(leng)+1)
        for i in range(int(start),int(start)+int(leng)):
            #print(array[i-int(start)])
            t=t+' and Token_'+str(i)+' ='+str(array[i-int(start)])+''
            join+='inner join ontologyTrans as b'+str(i)+' on a.Token_'+str(i)+'=b'+str(i)+'.TokenID\n'
            #and Token_4 =124 and Token_5 =15 and Token_6 =16 and Token_7 =123     
        backjoin=join+'inner join ontologyTrans as b'+str(int(start)+int(leng))+' on a.Token_'+str(int(start)+int(leng))+'=b'+str(int(start)+int(leng))+'.TokenID'
        frontjoin='inner join ontologyTrans as b'+str(int(start)-1)+' on a.Token_'+str(int(start)-1)+'=b'+str(int(start)-1)+'.TokenID\n'+join
        #print(backjoin)
        top=str(int(start)+int(leng))
        low=str(int(start)-1)
        #print(t)
        #print('///////////////////////////////////////////////////')
    elif int(leng)%2==1:
        #print('///////////////////////////////////////////////////')
        #print(int(leng))
        #print((int(leng)/2))
        start=5-((int(leng)/2)-0.5)
        t=''
        join=''
        #print(int(start))
        #print(int(start)+int(leng)+1)
        for i in range(int(start),int(start)+int(leng)):
            #print(array[i-int(start)])
            t=t+' and Token_'+str(i)+' ='+str(array[i-int(start)])+''
            join+='inner join ontologyTrans as b'+str(i)+' on a.Token_'+str(i)+'=b'+str(i)+'.TokenID\n'
            #and Token_4 =124 and Token_5 =15 and Token_6 =16 and Token_7 =123     
        backjoin=join+'inner join ontologyTrans as b'+str(int(start)+int(leng))+' on a.Token_'+str(int(start)+int(leng))+'=b'+str(int(start)+int(leng))+'.TokenID'
        frontjoin='inner join ontologyTrans as b'+str(int(start)-1)+' on a.Token_'+str(int(start)-1)+'=b'+str(int(start)-1)+'.TokenID\n'+join
        #print(backjoin)
        top=str(int(start)+int(leng))
        low=str(int(start)-1)
        #print(t)
        #print('///////////////////////////////////////////////////')
    #往後
    if int(top)<10:
        cursor = connections['NursingRecord'].cursor()
        query = f'''select Token_{top},b{top}.Token,count(*) as 'Sum' from nGram as a
        {backjoin}
        where PosStart>0 {t}
        group by Token_{top},b{top}.Token
        order by Sum desc'''
        #print('往後：\n',query)
        cursor.execute(query)
        res = cursor.fetchall()
        TokenID = []
        Token = []
        Sum = []
        for i in range(len(res)):
            TokenID.append(res[i][0])
            Token.append(res[i][1])
            Sum.append(res[i][2])
    else:
        TokenID=-1
        Token=-1
        Sum=-1
    #往前
    if int(low)>0:
        cursor = connections['NursingRecord'].cursor()
        query2 = f'''select Token_{low},b{low}.Token,count(*) as 'Sum' from nGram as a
        {frontjoin}
        where PosStart>0 {t}
        group by Token_{low},b{low}.Token
        order by Sum desc'''
        #print('往前：\n',query2)
        cursor.execute(query2)
        result = cursor.fetchall()
        TokenID2 = []
        Token2 = []
        Sum2 = []
        for i in range(len(result)):
            TokenID2.append(result[i][0])
            Token2.append(result[i][1])
            Sum2.append(result[i][2])
    else:
        TokenID2=-1
        Token2=-1
        Sum2=-1
    #計算個數
    cursor = connections['NursingRecord'].cursor()
    query3 = f'''select count(*) as 'Sum' from nGram as a
                where PosStart>0 {t}'''
    #print('數量：\n',query3)
    cursor.execute(query3)
    results = cursor.fetchall()
    TotalSum = []
    for i in range(len(results)):
        TotalSum.append(results[i][0])
    return JsonResponse({'TokenID':TokenID,'Token':Token,'Sum':Sum,'TokenID2':TokenID2,'Token2':Token2,'Sum2':Sum2,'TotalSum':TotalSum})


@csrf_exempt
def insert_word(request):
    import re
    array = request.GET.getlist("InsertArray")
    Usertext=request.GET.get("Usertext")
    #print('矩陣：',array)
    #print('矩陣數量：',len(array))
    #print('逗號數量：',array[0].count(','))
    for j in range(0,len(array)):
        commasum=array[j].count(',')
        a=''
        for k in range(1,commasum+2):
            a+=', Token_'+str(k)
        cursor = connections['NursingRecord'].cursor()
        query=f'''insert into TempMergeToken(UserName{a}) values('{Usertext}',{array[j]})'''
        #print(query)
        cursor.execute(query)
    repeatquery=f'''SELECT DISTINCT Token_1,Token_2,Token_3,Token_4,Token_5,Token_6,Token_7,Token_8,Token_9
                    INTO duplicate_table
                    FROM TempMergeToken
                    GROUP BY Token_1,Token_2,Token_3,Token_4,Token_5,Token_6,Token_7,Token_8,Token_9
                    HAVING COUNT(*) > 1


                    DELETE TempMergeToken from TempMergeToken as a inner join duplicate_table as b 
                    on a.Token_1=b.Token_1 and a.Token_2=b.Token_2 and a.Token_3=b.Token_3 and a.Token_4=b.Token_4 and a.Token_5=b.Token_5 and a.Token_6=b.Token_6
                    and a.Token_7=b.Token_7 and a.Token_8=b.Token_8 and a.Token_9=b.Token_9

                    INSERT TempMergeToken(UserName,Token_1,Token_2,Token_3,Token_4,Token_5,Token_6,Token_7,Token_8,Token_9)
                    SELECT 'Duplicate',*
                    FROM duplicate_table

                    DROP TABLE duplicate_table
                    '''
    cursor.execute(repeatquery)
    return JsonResponse({})


@csrf_exempt
def question_word(request):
    array = request.GET.getlist("ArrTest")
    #print(array)
    cursor = connections['NursingRecord'].cursor()
    if(len(array)==2):
        query = f'''update mergeToken set merged=-1  
                    where Token_5={array[0]} and Token_6={array[1]}  and Token_7 is null'''
    elif(len(array)==3):
        query = f'''update mergeToken set merged=-1
                    where Token_5={array[0]}  and Token_6={array[1]} and Token_7={array[2]}'''
    cursor.execute(query)
    #print(query)
    return JsonResponse({})      