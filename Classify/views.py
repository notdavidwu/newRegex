from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import pathlib

def Classify(request):
    au = request.session.get('au')
    return render(request, 'Classify/Classify.html',{'au':au})

@csrf_exempt
def WordCategory(request):
    query = '''select * from WordCategory'''
    cursor = connections['default'].cursor()
    cursor.execute(query)

    CategoryNo = []
    CategoryName = []

    result = cursor.fetchall()
    for i in range(len(result)):
        CategoryNo.append(result[i][0])
        CategoryName.append(result[i][1])
    return JsonResponse({'CategoryNo': CategoryNo,'CategoryName': CategoryName})

@csrf_exempt
def Leading(request):
    CategoryNo = request.POST.get('CategoryNo')
    query = '''select * from leading where CategoryNo=  '''+CategoryNo+'''and LeadingID<>1288'''
    cursor = connections['default'].cursor()

    CategoryNo=[]
    LeadingID = []
    Purpose = []
    rules = []
    cursor.execute(query)
    result = cursor.fetchall()
    print(query)
    for i in range(len(result)):
        CategoryNo.append(result[i][0])
        LeadingID.append(result[i][1])
        Purpose.append(result[i][2])
        rules.append(result[i][3])

    return JsonResponse({'CategoryNo': CategoryNo,'LeadingID': LeadingID,'Purpose': Purpose,'rules': rules})
@csrf_exempt
def Item2(request):
    LeadingID = request.POST.get('LeadingID')
    status= request.POST.get('status')
    print(status)
    if status=='1':
        query='''
        select * from(
            select Leading,Token1,Token2,Token3,Token4,Token5,Token6,Token7,Token8,total
            ,b.TokenID as 'Token1ID',c.TokenID as 'Token2ID',d.TokenID as 'Token3ID',e.TokenID as 'Token4ID'
            ,f.TokenID as 'Token5ID',g.TokenID as 'Token6ID',h.TokenID as 'Token7ID',i.TokenID as 'Token8ID' from (
            select DISTINCT Leading,
            Token1,Token2,Token3,Token4,Token5,Token6,Token7,Token8,count(*) as 'total' from (
            select 'a'as'Leading' , 
            case 
                  when b.Token is null then NULL
                  else b.Token 
                  END as'Token1',
                  case 
                  when  c.Token is null then NULL
                  else c.Token
                  END as 'Token2',
                  case 
                  when  c.Token='EndLine'  or d.Token is null then NULL
                  else d.Token 
                  end as 'Token3',
                  case
                  when d.Token='EndLine' OR c.Token='EndLine' or e.Token is null  then NULL
                  else e.Token
                  end as 'Token4',
                  case
                  when e.Token='EndLine' OR c.Token='EndLine' OR d.Token='EndLine' 
                   or f.Token is null or f.TokenID in(3,4) then NULL
                  else f.Token
                  end as 'Token5',
                  case
                  when e.Token='EndLine' OR c.Token='EndLine' OR d.Token='EndLine' 
                  OR f.Token='EndLine'  or g.TokenID in(3,4) or f.TokenID in(3,4)  
                  or g.Token is null then NULL
                  else g.Token
                  end as 'Token6',
                  case
                  when e.Token='EndLine' OR c.Token='EndLine' OR d.Token='EndLine' 
                  OR f.Token='EndLine' OR g.Token='EndLine' or g.TokenID in(3,4)  or f.TokenID in(3,4)
                  or h.Token is null then NULL
                  else h.Token
                  end as 'Token7',
                  case
                  when e.Token='EndLine' OR c.Token='EndLine' OR d.Token='EndLine' 
                  OR f.Token='EndLine' OR g.Token='EndLine' OR h.Token='EndLine'or g.TokenID in(3,4)or f.TokenID in(3,4)
                     or i.Token is null then NULL
                  else i.Token
                  end as 'Token8'
                from Ontology as B inner join nGram as a on B.TokenID=a.Token_1
                    inner join ontologyTrans as A on a.Token_1=A.TokenID and PosStart>0
                    inner join ontologyTrans as b on a.Token_2=b.TokenID and PosStart>0
                    inner join ontologyTrans as c on a.Token_3=c.TokenID and PosStart>0
                    inner join ontologyTrans as d on a.Token_4=d.TokenID and PosStart>0
                    inner join ontologyTrans as e on a.Token_5=e.TokenID and PosStart>0
                    inner join ontologyTrans as f on a.Token_6=f.TokenID and PosStart>0
                    inner join ontologyTrans as g on a.Token_7=g.TokenID and PosStart>0
                    inner join ontologyTrans as h on a.Token_8=h.TokenID and PosStart>0
                    inner join ontologyTrans as i on a.Token_9=i.TokenID and PosStart>0
                where B.TokenID='''+LeadingID+''' or B.SynonymWord='''+LeadingID+ ''' ) as a
                group by rollup (Leading,Token1,Token2,Token3,Token4,Token5,Token6,Token7,Token8)
            )as a left outer join ontologyTrans as b on a.Token1=b.Token
              left outer join ontologyTrans as c on a.Token2=c.Token
              left outer join ontologyTrans as d on a.Token3=d.Token
              left outer join ontologyTrans as e on a.Token4=e.Token
              left outer join ontologyTrans as f on a.Token5=f.Token
              left outer join ontologyTrans as g on a.Token6=g.Token
              left outer join ontologyTrans as h on a.Token7=h.Token
              left outer join ontologyTrans as i on a.Token8=i.Token
            where Leading is not null
        )as a 
        left outer join Type as b on a.Token1ID=b.TokenID
        where b.TokenID is  null
        order by 1, 2, 3,4,5,6,7,8,9,10'''
    elif status=='2':
        query = '''
        select * from(
            select Leading,Token1,Token2,Token3,Token4,Token5,Token6,Token7,Token8,total
                ,b.TokenID as 'Token1ID',c.TokenID as 'Token2ID',d.TokenID as 'Token3ID',e.TokenID as 'Token4ID'
                ,f.TokenID as 'Token5ID',g.TokenID as 'Token6ID',h.TokenID as 'Token7ID',i.TokenID as 'Token8ID' from (
                select DISTINCT Leading,
                Token1,Token2,Token3,Token4,Token5,Token6,Token7,Token8,count(*) as 'total' from (
                select 'a'as'Leading' , 
                case 
                      when b.Token is null then NULL
                      else b.Token 
                      END as'Token1',
                      case 
                      when  c.Token is null then NULL
                      else c.Token
                      END as 'Token2',
                      case 
                      when  c.Token='EndLine'  or d.Token is null then NULL
                      else d.Token 
                      end as 'Token3',
                      case
                      when d.Token='EndLine' OR c.Token='EndLine' or e.Token is null  then NULL
                      else e.Token
                      end as 'Token4',
                      case
                      when e.Token='EndLine' OR c.Token='EndLine' OR d.Token='EndLine' 
                       or f.Token is null or f.TokenID in(3,4) then NULL
                      else f.Token
                      end as 'Token5',
                      case
                      when e.Token='EndLine' OR c.Token='EndLine' OR d.Token='EndLine' 
                      OR f.Token='EndLine'  or g.TokenID in(3,4) or f.TokenID in(3,4)  
                      or g.Token is null then NULL
                      else g.Token
                      end as 'Token6',
                      case
                      when e.Token='EndLine' OR c.Token='EndLine' OR d.Token='EndLine' 
                      OR f.Token='EndLine' OR g.Token='EndLine' or g.TokenID in(3,4)  or f.TokenID in(3,4)
                      or h.Token is null then NULL
                      else h.Token
                      end as 'Token7',
                      case
                      when e.Token='EndLine' OR c.Token='EndLine' OR d.Token='EndLine' 
                      OR f.Token='EndLine' OR g.Token='EndLine' OR h.Token='EndLine'or g.TokenID in(3,4)or f.TokenID in(3,4)
                         or i.Token is null then NULL
                      else i.Token
                      end as 'Token8'
                    from Ontology as B inner join nGram as a on B.TokenID=a.Token_1
                        inner join ontologyTrans as A on a.Token_1=A.TokenID and PosStart>0
                        inner join ontologyTrans as b on a.Token_2=b.TokenID and PosStart>0
                        inner join ontologyTrans as c on a.Token_3=c.TokenID and PosStart>0
                        inner join ontologyTrans as d on a.Token_4=d.TokenID and PosStart>0
                        inner join ontologyTrans as e on a.Token_5=e.TokenID and PosStart>0
                        inner join ontologyTrans as f on a.Token_6=f.TokenID and PosStart>0
                        inner join ontologyTrans as g on a.Token_7=g.TokenID and PosStart>0
                        inner join ontologyTrans as h on a.Token_8=h.TokenID and PosStart>0
                        inner join ontologyTrans as i on a.Token_9=i.TokenID and PosStart>0
                    where B.TokenID=''' + LeadingID + ''' or B.SynonymWord=''' + LeadingID + ''' ) as a
                group by rollup (Leading,Token1,Token2,Token3,Token4,Token5,Token6,Token7,Token8)
            )as a left outer join ontologyTrans as b on a.Token1=b.Token
                  left outer join ontologyTrans as c on a.Token2=c.Token
                  left outer join ontologyTrans as d on a.Token3=d.Token
                  left outer join ontologyTrans as e on a.Token4=e.Token
                  left outer join ontologyTrans as f on a.Token5=f.Token
                  left outer join ontologyTrans as g on a.Token6=g.Token
                  left outer join ontologyTrans as h on a.Token7=h.Token
                  left outer join ontologyTrans as i on a.Token8=i.Token
            where Leading is not null
        )as a 
        left outer join Type as b on a.Token1ID=b.TokenID
        where b.TokenID is not null
                order by 1, 2, 3,4,5,6,7,8,9,10'''
    elif status=='3':
        query = '''select Leading,Token1,Token2,Token3,Token4,Token5,Token6,Token7,Token8,total
                ,b.TokenID as 'Token1ID',c.TokenID as 'Token2ID',d.TokenID as 'Token3ID',e.TokenID as 'Token4ID'
                ,f.TokenID as 'Token5ID',g.TokenID as 'Token6ID',h.TokenID as 'Token7ID',i.TokenID as 'Token8ID' from (
                select DISTINCT Leading,
                Token1,Token2,Token3,Token4,Token5,Token6,Token7,Token8,count(*) as 'total' from (
                select 'a'as'Leading' , 
                case 
                      when b.Token is null then NULL
                      else b.Token 
                      END as'Token1',
                      case 
                      when  c.Token is null then NULL
                      else c.Token
                      END as 'Token2',
                      case 
                      when  c.Token='EndLine'  or d.Token is null then NULL
                      else d.Token 
                      end as 'Token3',
                      case
                      when d.Token='EndLine' OR c.Token='EndLine' or e.Token is null  then NULL
                      else e.Token
                      end as 'Token4',
                      case
                      when e.Token='EndLine' OR c.Token='EndLine' OR d.Token='EndLine' 
                       or f.Token is null or f.TokenID in(3,4) then NULL
                      else f.Token
                      end as 'Token5',
                      case
                      when e.Token='EndLine' OR c.Token='EndLine' OR d.Token='EndLine' 
                      OR f.Token='EndLine'  or g.TokenID in(3,4) or f.TokenID in(3,4)  
                      or g.Token is null then NULL
                      else g.Token
                      end as 'Token6',
                      case
                      when e.Token='EndLine' OR c.Token='EndLine' OR d.Token='EndLine' 
                      OR f.Token='EndLine' OR g.Token='EndLine' or g.TokenID in(3,4)  or f.TokenID in(3,4)
                      or h.Token is null then NULL
                      else h.Token
                      end as 'Token7',
                      case
                      when e.Token='EndLine' OR c.Token='EndLine' OR d.Token='EndLine' 
                      OR f.Token='EndLine' OR g.Token='EndLine' OR h.Token='EndLine'or g.TokenID in(3,4)or f.TokenID in(3,4)
                         or i.Token is null then NULL
                      else i.Token
                      end as 'Token8'
                    from Ontology as B inner join nGram as a on B.TokenID=a.Token_1
                        inner join ontologyTrans as A on a.Token_1=A.TokenID and PosStart>0
                        inner join ontologyTrans as b on a.Token_2=b.TokenID and PosStart>0
                        inner join ontologyTrans as c on a.Token_3=c.TokenID and PosStart>0
                        inner join ontologyTrans as d on a.Token_4=d.TokenID and PosStart>0
                        inner join ontologyTrans as e on a.Token_5=e.TokenID and PosStart>0
                        inner join ontologyTrans as f on a.Token_6=f.TokenID and PosStart>0
                        inner join ontologyTrans as g on a.Token_7=g.TokenID and PosStart>0
                        inner join ontologyTrans as h on a.Token_8=h.TokenID and PosStart>0
                        inner join ontologyTrans as i on a.Token_9=i.TokenID and PosStart>0
                    where B.TokenID=''' + LeadingID + ''' or B.SynonymWord=''' + LeadingID + ''' ) as a
                group by rollup (Leading,Token1,Token2,Token3,Token4,Token5,Token6,Token7,Token8)
            )as a left outer join ontologyTrans as b on a.Token1=b.Token
                  left outer join ontologyTrans as c on a.Token2=c.Token
                  left outer join ontologyTrans as d on a.Token3=d.Token
                  left outer join ontologyTrans as e on a.Token4=e.Token
                  left outer join ontologyTrans as f on a.Token5=f.Token
                  left outer join ontologyTrans as g on a.Token6=g.Token
                  left outer join ontologyTrans as h on a.Token7=h.Token
                  left outer join ontologyTrans as i on a.Token8=i.Token
            where Leading is not null
                order by 1, 2, 3,4,5,6,7,8,9,10'''

    cursor = connections['default'].cursor()

    Token1 = []
    Token2 = []
    Token3 = []
    Token4 = []
    Token5 = []
    Token6 = []
    Token7 = []
    Token8 = []
    Sum = []
    Token1ID = []
    Token2ID = []
    Token3ID = []
    Token4ID = []
    Token5ID = []
    Token6ID = []
    Token7ID = []
    Token8ID = []


    cursor.execute(query)
    result = cursor.fetchall()

    for i in range(len(result)):
        Token1.append(result[i][1])
        Token2.append(result[i][2])
        Token3.append(result[i][3])
        Token4.append(result[i][4])
        Token5.append(result[i][5])
        Token6.append(result[i][6])
        Token7.append(result[i][7])
        Token8.append(result[i][8])
        Sum.append(result[i][9])
        Token1ID.append(result[i][10])
        Token2ID.append(result[i][11])
        Token3ID.append(result[i][12])
        Token4ID.append(result[i][13])
        Token5ID.append(result[i][14])
        Token6ID.append(result[i][15])
        Token7ID.append(result[i][16])
        Token8ID.append(result[i][17])
    return JsonResponse(
        {'Token1': Token1,'Token2': Token2,'Token3': Token3, 'Token4': Token4, 'Token5': Token5, 'Token6': Token6, 'Token7': Token7, 'Token8': Token8,'Sum': Sum,
         'Token1ID': Token1ID,'Token2ID': Token2ID,'Token3ID': Token3ID, 'Token4ID': Token4ID, 'Token5ID': Token5ID, 'Token6ID': Token6ID, 'Token7ID': Token7ID, 'Token8ID': Token8ID})
@csrf_exempt
def MultipleWords(request):
    Token1ID = request.POST.get('Token1ID')
    Token2ID = request.POST.get('Token2ID')
    Token3ID = request.POST.get('Token3ID')
    Token4ID = request.POST.get('Token4ID')
    Token5ID = request.POST.get('Token5ID')
    Token6ID = request.POST.get('Token6ID')
    Token7ID = request.POST.get('Token7ID')
    Token8ID = request.POST.get('Token8ID')
    Token9ID = request.POST.get('Token9ID')
    str=''
    i=1;
    if Token1ID!='null':
        str = str + ',' + Token1ID
    if Token2ID!='null':
        str = str + ',' + Token2ID
    if Token3ID!='null':
        str = str + ',' + Token3ID
    if Token4ID != 'null':
        str = str + ',' + Token4ID
    if Token5ID != 'null':
        str = str + ',' + Token5ID
    if Token6ID!='null':
        str = str + ',' + Token6ID
    if Token7ID!='null':
        str = str + ',' + Token7ID
    if Token8ID!='null':
        str = str + ',' + Token8ID
    print(str)
    query='''declare @res tinyint;
    exec appendMultipleWords @res '''+str+'''
        select @res as 'state' '''
    print(query)
    cursor = connections['default'].cursor()
    state = []
    cursor.execute(query)

    res = cursor.fetchall()

    for i in range(len(res)):
        state.append(res[i][0])
    return JsonResponse({'state': state})


@csrf_exempt
def Sort(request):
    LeadingID = request.POST.get('LeadingID')
    TokenID = request.POST.get('TokenID')
    query = '''
    insert into Type (LeadingID,TokenID) values('''+LeadingID+''','''+TokenID+''')'''
    query2 = '''
    select c.Token as'child',b.Token as 'dad' from Type as a 
        inner join ontologyTrans as b on a.LeadingID=b.TokenID
        inner join ontologyTrans as c on a.TokenID=c.TokenID
    where LeadingID='''+LeadingID+''' and a.TokenID='''+TokenID+''''''
    print(query)
    cursor = connections['default'].cursor()
    cursor2 = connections['default'].cursor()
    child = []
    dad = []
    cursor.execute(query)
    cursor2.execute(query2)
    res = cursor2.fetchall()
    for i in range(len(res)):
        child.append(res[i][0])
        dad.append(res[i][1])
    return JsonResponse({'child':child,'dad':dad})


@csrf_exempt
def FinishSort(request):
    LeadingID = request.POST.get('LeadingID')

    query = '''
    select c.Token as'child',b.Token as 'dad' from Type as a 
        inner join ontologyTrans as b on a.LeadingID=b.TokenID
        inner join ontologyTrans as c on a.TokenID=c.TokenID
    where LeadingID='''+LeadingID+''''''
    cursor = connections['default'].cursor()

    child = []
    dad = []
    cursor.execute(query)
    res = cursor.fetchall()
    for i in range(len(res)):
        child.append(res[i][0])
        dad.append(res[i][1])
    return JsonResponse({'child':child,'dad':dad})
