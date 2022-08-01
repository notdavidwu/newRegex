import django.forms
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.db import connections


class UserForm(forms.Form):
    username = forms.CharField(label='帳號', max_length=100)
    password = forms.CharField(label='密碼', widget=forms.PasswordInput())
    realname = forms.CharField(label='姓名', max_length=100)
    hospital_type_choices = (
        (0, '中山附醫'),
        (1, '台大'),
    )
    hospital = forms.ChoiceField(label='院別', widget=forms.Select(attrs={"id": "select_0"}),
                                 choices=hospital_type_choices,
                                 initial=hospital_type_choices[0])


def index(request):
    au = request.session.get('au')
    return render(request, 'home.html',{'au':au})


def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            realname = uf.cleaned_data['realname']
            hospital = uf.cleaned_data['hospital']
            re = User.objects.filter(username=username)
            # print(len(re))
            if len(re) != 0:

                return render(request, 'accounts/register.html', {'register_error': '該帳號已經註冊過', 'uf': uf})
            else:
                registAdd = User.objects.create_user(username=username, password=password, first_name=realname,
                                                     last_name=hospital,is_active=0)
                # print(registAdd)
                if registAdd == False:
                    return render(request, 'accounts/register.html', {'registAdd': registAdd, 'username': username})
                else:
                    # return render(request, 'home.html')
                    return redirect('/', {'user': re})

    else:
        uf = UserForm()
        return render(request, 'accounts/register.html', {'uf': uf})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        re = auth.authenticate(username=username, password=password)
        # print(username, password)
        if re is not None:
            au = Auth(username)
            de_identification = de_identification_check(username)
            all_annotations = all_annotations_check(username)
            eventDefinition_edit = eventDefinition_edit_check(username)
            request.session['au'] = au
            request.session['de_identification'] = de_identification
            request.session['all_annotations'] = all_annotations
            request.session['eventDefinition_edit'] = eventDefinition_edit
            auth.login(request, re)
            return redirect('/', {'user': re})
            # return render(request, 'home.html', {'user': re})

        else:
            return render(request, 'accounts/login.html', {'login_error': '帳號或密碼錯誤，可點此重新註冊'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
    # return render(request,'home.html')


def Auth(username):
    query = '''select Authority_app from auth_app where username=%s'''
    cursor = connections['default'].cursor()
    cursor.execute(query, [username])
    res = cursor.fetchall()
    au = []
    for i in range(len(res)):
        au.append(res[i][0])
    return au

def de_identification_check(username):
    query = '''select de_identification from auth_user where username=%s'''
    cursor = connections['default'].cursor()
    cursor.execute(query, [username])
    res = cursor.fetchall()
    de_identification=res[0][0]
    return de_identification

def all_annotations_check(username):
    query = '''select all_annotations from auth_user where username=%s'''
    cursor = connections['default'].cursor()
    cursor.execute(query, [username])
    res = cursor.fetchall()
    all_annotations=res[0][0]
    return all_annotations

def eventDefinition_edit_check(username):
    query = '''select eventDefinition_edit from auth_user where username=%s'''
    cursor = connections['default'].cursor()
    cursor.execute(query, [username])
    res = cursor.fetchall()
    eventDefinition_edit=res[0][0]
    return eventDefinition_edit
