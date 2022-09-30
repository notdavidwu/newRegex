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
    return render(request, 'PowerBI/PowerBI.html',{})

'''Returns report embed uration'''
AUTHENTICATION_MODE = 'ServicePrincipal'
# Workspace Id in which the report is present
WORKSPACE_ID = '7c6c9886-7fc8-42bb-8dff-ae28b2a4c77d'
# Report Id for which Embed token needs to be generated
REPORT_ID = 'e572b80b-05c6-41f3-b331-d40706b2f35c'
# Id of the Azure tenant in which AAD app and Power BI report is hosted. Required only for ServicePrincipal authentication mode.
TENANT_ID = 'be4937e1-5c7a-4f12-bd7f-cc51a82d238b' 
# Client Id (Application Id) of the AAD app
CLIENT_ID = '2916a788-a3f5-4dee-a7a7-5811ef212e9c'
# Client Secret (App Secret) of the AAD  Required only for ServicePrincipal authentication mode.
CLIENT_SECRET = 'JYB8Q~bRVNA73_i_VMgvcIzbWYhr5aKxNsmGTbVJ'
# Scope Base of AAD  Use the below uration to use all the permissions provided in the AAD app through Azure portal.
SCOPE_BASE = ['https://analysis.windows.net/powerbi/api/.default']
# URL used for initiating authorization request
AUTHORITY_URL = 'https://login.microsoftonline.com/organizations'
# Master user email address. Required only for MasterUser authentication mode.
POWER_BI_USER = ''
# Master user email password. Required only for MasterUser authentication mode.
POWER_BI_PASS = ''

@csrf_exempt
def get_embed_info(request):

    embed_info = PbiEmbedService().get_embed_params_for_single_report(WORKSPACE_ID, REPORT_ID)
    tokenId = embed_info[0]
    accessToken = embed_info[1]
    tokenExpiry = embed_info[2]
    reportConfig = embed_info[3]
    print(tokenId)
    return JsonResponse({'data':f'{embed_info}' })

