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
            if FormInputText != None and FormRegexText != None:
                text123 = Text.objects.create(author=request.user) #建立新表單
                #text123.author = request.user
                text123.regexText = FormRegexText #將解析完的資料丟到物件內
                text123.inputText = FormInputText #將解析完的資料丟到物件內
                result = {'status':'0'}
                text123.save() #存檔
            # print(result)
        else:
            print("form is NOT valid.")
        
        
    return JsonResponse(result)


class Home(ListView):
    model = Text
    template_name = 'index.html'


    
