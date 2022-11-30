from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import pathlib
import os
import platform 
import numpy as np
import time
from collections import OrderedDict
import json
import msal
from PowerBI.pbiembedservice import PbiEmbedService

def PowerBI(request):
    au = request.session.get('au',0)
    if not request.user.is_authenticated : 
        return redirect('/')
    return render(request, 'PowerBI/PowerBI.html',{'au':au})

@csrf_exempt
def get_dashboard(request):
    cursor = connections['practiceDB'].cursor()
    query = 'SELECT workspaceID,reportID,dashboardName FROM powerBI'
    cursor.execute(query,[])
    res = cursor.fetchall()
    workspaceID,reportID,dashboard_name=[],[],[]
    for row in res:
        workspaceID.append(row[0])
        reportID.append(row[1])
        dashboard_name.append(row[2])
    cursor.close()
    return JsonResponse({'workspaceID':workspaceID,'reportID':reportID,'dashboard_name':dashboard_name})

@csrf_exempt
def regist_dashboard(request):
    dashboard_name = request.POST.get('dashboard_name')
    dashboard_url = request.POST.get('dashboard_url')
    workspaceID = [dashboard_url.split('/')[i+1] for i,term in enumerate(dashboard_url.split('/')) if term=='groups'][0]
    reportID = [dashboard_url.split('/')[i+1] for i,term in enumerate(dashboard_url.split('/')) if term=='reports'][0]
    cursor = connections['practiceDB'].cursor()

    query = 'SELECT COUNT(*) as counter FROM powerBI WHERE workspaceID=%s and reportID=%s and dashboardName=%s'
    cursor.execute(query,[workspaceID,reportID,dashboard_name])
    check = cursor.fetchall()[0][0]
    if check == 0:
        query = 'INSERT INTO powerBI (workspaceID,reportID,dashboardName) VALUES (%s,%s,%s)'
        cursor.execute(query,[workspaceID,reportID,dashboard_name])
    cursor.close()
    return JsonResponse({})

@csrf_exempt
def get_embed_info(request):
    
    # Workspace Id in which the report is present
    WORKSPACE_ID = request.POST.get('workspaceID')
    # Report Id for which Embed token needs to be generated
    REPORT_ID = request.POST.get('reportID')
    embed_info = PbiEmbedService().get_embed_params_for_single_report(WORKSPACE_ID, REPORT_ID)
    tokenId = embed_info[0]
    accessToken = embed_info[1]
    tokenExpiry = embed_info[2]
    reportConfig = embed_info[3]
    return JsonResponse({'data':f'{embed_info}' })

