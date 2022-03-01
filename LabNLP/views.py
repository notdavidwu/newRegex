from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
@csrf_exempt
def LabNLP(request):
    au = request.session.get('au')
    return render(request, 'LabNLP/LabNLP.html',{'au':au})

@csrf_exempt
def InsertIntoDB(request):
    Token5ID=request.POST.get('Token5ID')
    Token6ID=request.POST.get('Token6ID')

    query_back = '''
    declare @ SQLString
    nvarchar(500);
    declare @ ParmDefinition
    nvarchar(500);

    set @ SQLString = 'appendTwoWords @w1, @w2'
    set @ ParmDefinition = '@w1 int, @w2 int'
    exec
    sp_executesql @ SQLString,@ParmDefinition,@w1='''+Token5ID+''',@w2='''+Token6ID
    query='''
        declare @s int;
        exec appendTwoWords '''+Token5ID+','''+Token6ID+''',@s output 
        select @s'''
    print(query)
    cursor = connections['default'].cursor()
    cursor.execute(query)
    state = []
    res = cursor.fetchall()
    for i in range(len(res)):
        state.append(res[i][0])
    return JsonResponse({'state': state})
@csrf_exempt
def InsertIntoDB_THREE(request):
    Token5ID=request.POST.get('Token5ID')
    Token6ID=request.POST.get('Token6ID')
    Token7ID=request.POST.get('Token7ID')
    cursor = connections['default'].cursor()
    print(Token5ID)
    print(Token6ID)
    print(Token7ID)
    query2 = '''
    begin transaction
        declare @NewID
        int;
        exec
        appnedNewWord3Ontology '''+Token5ID+','''+Token6ID+''','''+Token7ID+'''
        set @NewID = IDENT_CURRENT('Ontology');
        --exec
        appnedNewWord3TokenComponent @NewID,'''+Token5ID+','''+Token6ID+''','''+Token7ID+'''
    
        --exec
        mergeThreeWordsOnNGram @NewID,'''+Token5ID+','''+Token6ID+''','''+Token7ID+'''
    
        --exec
        mergeThreeWordsOnTexttoken @NewID,'''+Token5ID+','''+Token6ID+''','''+Token7ID+'''
    commit'''
    query='''
        declare @s int;
        exec appendThreeWords '''+Token5ID+','''+Token6ID+''','''+Token7ID+''',@s output 
        select @s'''
    print(query)
    cursor = connections['default'].cursor()
    cursor.execute(query)
    state = []
    res = cursor.fetchall()
    for i in range(len(res)):
        state.append(res[i][0])
    return JsonResponse({'state': state})

@csrf_exempt
def ThreeWord(request):
    Type1=request.POST.get('Type1')
    Type2=request.POST.get('Type2')
    Type3 = request.POST.get('Type3')

    query = '''select * from threeWordsCount(\''''+Type1+'''',\''''+Type2+'''',\''''+Type3+'''') order by Appearance desc'''
    print(query)
    cursor = connections['default'].cursor()
    cursor.execute(query)
    Token5ID=[]
    Token6ID = []
    Token7ID=[]
    SUM=[]
    Token5=[]
    Token6=[]
    Token7=[]

    Token = cursor.fetchall()

    for i in range(len(Token)):
        Token5.append(Token[i][0])
        Token6.append(Token[i][1])
        Token7.append(Token[i][2])
        SUM.append(Token[i][9])
        Token5ID.append(Token[i][3])
        Token6ID.append(Token[i][4])
        Token7ID.append(Token[i][5])

    return JsonResponse({'Token5ID': Token5ID,'Token6ID': Token6ID,'Token7ID':Token7ID,'SUM': SUM,'Token5': Token5,'Token6': Token6,'Token7':Token7})
@csrf_exempt
def TwoWord(request):
    Type4=request.POST.get('Type4')
    Type5=request.POST.get('Type5')
    query = '''select * from twoWordsCount(\''''+Type4+'''',\''''+Type5+'''') order by Times desc'''
    print(query)
    cursor = connections['default'].cursor()
    cursor.execute(query)
    Token5ID=[]
    Token6ID = []

    SUM=[]
    Token5=[]
    Token6=[]


    Token = cursor.fetchall()

    for i in range(len(Token)):
        Token5.append(Token[i][0])
        Token6.append(Token[i][1])
        SUM.append(Token[i][6])
        Token5ID.append(Token[i][2])
        Token6ID.append(Token[i][3])


    return JsonResponse({'Token5ID': Token5ID,'Token6ID': Token6ID,'SUM': SUM,'Token5': Token5,'Token6': Token6,})
@csrf_exempt
def Select(request):
    find = request.POST.get('find')
    text=request.POST.get('text')
    Type1 = request.POST.get('Type1')
    Type2 = request.POST.get('Type2')
    Type3 = request.POST.get('Type3')
    print(Type1)
    print(Type2)
    print(Type3)
    print(text)
    if (find=='First Word'):
        query = '''select * from threeWordsCount(\'''' + Type1 + '''',\'''' + Type2 + '''',\'''' + Type3 + '''') where FirstWord = \'''' + text + '''' order by Appearance desc'''
        print('1')
    elif (find=='Second Word'):
        query = '''select * from threeWordsCount(\'''' + Type1 + '''',\'''' + Type2 + '''',\'''' + Type3 + '''') where SecondWord = \'''' + text + '''' order by Appearance desc'''
        print('2')
    elif (find=='Third Word'):
        query = '''select * from threeWordsCount(\'''' + Type1 + '''',\'''' + Type2 + '''',\'''' + Type3 + '''') where ThirdWord = \'''' + text + '''' order by Appearance desc'''
        print('3')
    print(query)
    cursor = connections['default'].cursor()
    cursor.execute(query)
    Token5ID=[]
    Token6ID = []
    Token7ID=[]
    SUM=[]
    Token5=[]
    Token6=[]
    Token7=[]

    print(query)
    Token = cursor.fetchall()
    for i in range(len(Token)):
        Token5.append(Token[i][0])
        Token6.append(Token[i][1])
        Token7.append(Token[i][2])
        SUM.append(Token[i][9])
        Token5ID.append(Token[i][3])
        Token6ID.append(Token[i][4])
        Token7ID.append(Token[i][5])

    return JsonResponse({'Token5ID': Token5ID,'Token6ID': Token6ID,'Token7ID':Token7ID,'SUM': SUM,'Token5': Token5,'Token6': Token6,'Token7':Token7})

@csrf_exempt
def Select2(request):
    text=request.POST.get('text')
    Type1 = request.POST.get('Type1')
    Type2 = request.POST.get('Type2')
    find = request.POST.get('find')
    print(find)



    if (find == 'First Word'):
        query = '''select * from twoWordsCount(\'''' + Type1 + '''',\'''' + Type2 + '''') where FirstWord = \'''' + text + '''' order by Times desc'''
        print('4')
    elif (find == 'Second Word'):
        query = '''select * from twoWordsCount(\'''' + Type1 + '''',\'''' + Type2 + '''') where SecondWord = \'''' + text + '''' order by Times desc'''
        print('5')
    print(query)
    cursor = connections['default'].cursor()
    cursor.execute(query)
    Token5ID=[]
    Token6ID = []
    SUM=[]
    Token5=[]
    Token6=[]

    print(query)
    Token = cursor.fetchall()
    for i in range(len(Token)):
        Token5.append(Token[i][0])
        Token6.append(Token[i][1])

        SUM.append(Token[i][6])
        Token5ID.append(Token[i][2])
        Token6ID.append(Token[i][3])

    return JsonResponse({'Token5ID': Token5ID, 'Token6ID': Token6ID, 'SUM': SUM, 'Token5': Token5, 'Token6': Token6, })