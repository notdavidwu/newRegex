
from cv2 import resize
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import numpy as np

@csrf_exempt
def subjectPatientDecide(request):
    au = request.session.get('au')
    de_identification = request.session.get('de_identification')
    return render(request, 'subjectPatientDecide/subjectPatientDecide.html',{'au':au,'de_identification':de_identification})

