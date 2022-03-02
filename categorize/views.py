from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import pathlib
import numpy as np
@csrf_exempt
def categorize(request):
    au = request.session.get('au')
    return render(request, 'categorize/categorize.html',{'au':au})

@csrf_exempt
def getCategory(request):
    query = '''
        SELECT a.CategoryNo,a.Category,COUNT(a.Category) AS Total FROM Infection_Category AS a
        left outer join InfectionCategoryPool AS b on a.CategoryNo=b.CategoryNo where b.checked=1 
        GROUP BY a.CategoryNo,a.Category
    '''
    cursor = connections['AIC_Infection'].cursor()
    CategoryNo=[]
    Category=[]
    Total = []
    cursor.execute(query)
    result = cursor.fetchall()
    for i in range(len(result)):
        CategoryNo.append(result[i][0])
        Category.append(result[i][1])
        Total.append(result[i][2])
    return JsonResponse({'CategoryNo':CategoryNo,'Category': Category,'Total':Total})

@csrf_exempt
def getComfirmCategory(request):
    query = '''
        SELECT a.CategoryNo,a.Category,COUNT(a.Category) AS Total FROM Infection_Category AS a
        inner join InfectionCategoryPool AS b on a.CategoryNo=b.CategoryNo where b.checked=0 
        GROUP BY a.CategoryNo,a.Category
    '''
    cursor = connections['AIC_Infection'].cursor()
    CategoryNo = []
    Category = []
    Total = []
    cursor.execute(query)
    result = cursor.fetchall()
    for i in range(len(result)):
        CategoryNo.append(result[i][0])
        Category.append(result[i][1])
        Total.append(result[i][2])
    return JsonResponse({'CategoryNo':CategoryNo,'Category': Category,'Total':Total})

@csrf_exempt
def PoolList(request):
    keyword = request.POST.get('keyword')
    keyword = '%'+keyword+'%'
    category = request.POST.get('category')

    query = '''
        SELECT B.TokenID,REPLACE(Token,'[space]',' ') AS Token ,categorized
        FROM InfectionCategoryPool as A
        INNER JOIN Ontology as B ON A.TokenID=B.TokenID 
        WHERE A.CategoryNo=%s and Token like %s AND A.checked=1
    '''
    cursor = connections['AIC_Infection'].cursor()
    cursor.execute(query,[category,keyword])
    result = cursor.fetchall()
    TokenID=[]
    Token=[]
    categorized = []
    for i in range(len(result)):
        TokenID.append(result[i][0])
        Token.append(result[i][1])
        categorized.append(result[i][2])
    return JsonResponse({'TokenID':TokenID,'Token': Token,'categorized':categorized})

@csrf_exempt
def comfirmList(request):
    category = request.POST.get('category')
    query = '''
        SELECT B.TokenID,REPLACE(Token,'[space]',' ') AS Token 
        FROM InfectionCategoryPool as A
        INNER JOIN Ontology as B ON A.TokenID=B.TokenID 
        WHERE A.CategoryNo=%s AND A.checked=0
    '''
    cursor = connections['AIC_Infection'].cursor()
    cursor.execute(query,[category])
    result = cursor.fetchall()
    TokenID=[]
    Token=[]
    for i in range(len(result)):
        TokenID.append(result[i][0])
        Token.append(result[i][1])

    return JsonResponse({'TokenID':TokenID,'Token': Token})


@csrf_exempt
def add2Category(request):
    CategoryID = request.POST.get('CategoryID')
    Category = request.POST.get('Category')
    query = '''
        SELECT * FROM Infection_Conversion_Category WHERE Category=%s
    '''
    cursor = connections['AIC_Infection'].cursor()
    cursor.execute(query,[Category])
    result = cursor.fetchall()
    if(len(result)==0):
        query = '''
            INSERT INTO Infection_Conversion_Category (CategoryNo,Category) VALUES(%s,%s)
        '''
        cursor.execute(query,[CategoryID,Category])

    return JsonResponse({})

@csrf_exempt
def add2ConversionTable(request):
    CategoryID = request.POST.get('CategoryID')
    Category = request.POST.get('Category')
    TokenID = request.POST.getlist('TokenID[]')

    query = '''
        SELECT CategoryNo FROM Infection_Conversion_Category WHERE Category=%s
    '''
    cursor = connections['AIC_Infection'].cursor()
    cursor.execute(query,[Category])
    result = cursor.fetchall()

    CategoryNo = CategoryID
    
    query_insert = '''
        INSERT INTO Infection_Conversion_Table(CategoryNo,TokenID) VALUES(%s,%s)
    '''
    query_check = '''
        SELECT CategoryNo, TokenID FROM Infection_Conversion_Table WHERE CategoryNo=%s and TokenID=%s 
    '''
    query_update = '''
        UPDATE [AIC_Infection].[dbo].[InfectionCategoryPool] SET categorized=(
        select categorized from InfectionCategoryPool where TokenID=%s
        )+1 where TokenID=%s
    '''


    cursor = connections['AIC_Infection'].cursor()
    for i in range(len(TokenID)):
        cursor.execute(query_check,[CategoryNo,TokenID[i]])
        result = cursor.fetchall()
        if len(result)==0:
            cursor.execute(query_insert,[CategoryNo,TokenID[i]])
            cursor.execute(query_update,[TokenID[i],TokenID[i]])


    return JsonResponse({'CategoryNo':CategoryNo[0]})

@csrf_exempt
def removeList(request):
    removeObjectID = request.POST.getlist('removeObjectID[]')
    category = request.POST.get('category')

    cursor = connections['AIC_Infection'].cursor()
    query = '''
        DELETE FROM Infection_Conversion_Table WHERE CategoryNo=%s AND TokenID=%s
    '''
    query_update = '''
        UPDATE [AIC_Infection].[dbo].[InfectionCategoryPool] SET categorized=(
        select categorized from InfectionCategoryPool where TokenID=%s
        )-1 where TokenID=%s
    '''
    for i in range(len(removeObjectID)):
        cursor.execute(query,[category,removeObjectID[i]])
        cursor.execute(query_update,[removeObjectID[i],removeObjectID[i]])

    querySearchResident='''
        SELECT COUNT(CategoryNo) as num
        FROM Infection_Conversion_Table where CategoryNo=%s
                        '''
    cursor.execute(querySearchResident,[category])
    res=cursor.fetchall()

    if res[0][0]==0:
        queryDeleteCatergory='''DELETE FROM Infection_Conversion_Category WHERE CategoryNo=%s'''
        cursor.execute(queryDeleteCatergory,[category])
        delete='T'
    else:
        delete='F'
    return JsonResponse({'delete':delete})


@csrf_exempt
def confirmAndAbandon(request):
    comfirmListID = request.POST.getlist('comfirmListID[]')
    abandonListID = request.POST.getlist('abandonListID[]')
    comfirmIDString, abandonIDString = '',''
    for i,ID in enumerate(comfirmListID):
        if i == 0:
            comfirmIDString += ID
        else:
            comfirmIDString += ', '+ID

    for i,ID in enumerate(abandonListID):
        if i == 0:
            abandonIDString += ID
        else:
            abandonIDString += ', '+ID
  
    cursor = connections['AIC_Infection'].cursor()
    queryAbandon = 'UPDATE InfectionCategoryPool SET checked=-1 WHERE TokenID IN ('+abandonIDString+')'
    queryComfirm = 'UPDATE InfectionCategoryPool SET checked=1 WHERE TokenID IN ('+comfirmIDString+')'
    if len(abandonListID)>0:
        cursor.execute(queryAbandon)
    if len(comfirmListID)>0:
        cursor.execute(queryComfirm)
    return JsonResponse({})

@csrf_exempt
def getCategoriedClass(request):
    query = '''
        select a.*,COUNT(a.CategoryNo) as Total from Infection_Conversion_Category as a
        inner join Infection_Conversion_Table as b on a.CategoryNo=b.CategoryNo
        group by a.CategoryNo,a.Category order by a.CategoryNo
    '''
    cursor = connections['AIC_Infection'].cursor()
    CategoryNo = []
    Category = []
    Total = []
    cursor.execute(query)
    result = cursor.fetchall()
    for i in range(len(result)):
        CategoryNo.append(result[i][0])
        Category.append(result[i][1])
        Total.append(result[i][2])
    return JsonResponse({'CategoryNo':CategoryNo,'Category': Category,'Total':Total})

@csrf_exempt
def getCategoriedList(request):
    category = request.POST.get('category')

    query = '''
        SELECT B.TokenID,REPLACE(Token,'[space]',' ') AS Token 
        FROM Infection_Conversion_Table as A
        INNER JOIN Ontology as B ON A.TokenID=B.TokenID 
        WHERE A.CategoryNo=%s
    '''
    cursor = connections['AIC_Infection'].cursor()
    cursor.execute(query,[category])
    result = cursor.fetchall()
    TokenID=[]
    Token=[]
    for i in range(len(result)):
        TokenID.append(result[i][0])
        Token.append(result[i][1])

    return JsonResponse({'TokenID':TokenID,'Token': Token})