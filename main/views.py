from django.shortcuts import render
from django.shortcuts import redirect,HttpResponse
from django.http import JsonResponse
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.template.defaulttags import register
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Q

import json,time
from main.models import Users as User
from main.models import recordinfo

import pymysql

@register.filter
def get_range(value):
    return range(value)

@login_required
def index(request):
    return render(request,"index2.html")

def register(request):
    if (request.method == 'POST'):
        username=request.POST['user_name']
        password=request.POST['pwd']
        superuser=request.POST['u_role']
        u=User.objects.filter(username=username).first()
        if u:
            return render(request, 'login.html', {'msg': u'此用户名已经被注册!'})
        else:
            user = User.objects.create_user(username=username, password=password, is_superuser=superuser)
            return redirect('/login')
    return render(request,'login.html',{'msg':u'注册'})

def v_login(request):
    if (request.method == 'POST'):
        u_name=request.POST['user_name']
        u_pwd = request.POST['pwd']
        user = authenticate(username=u_name, password=u_pwd)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'msg': u'该用户已被禁用!'})
        else:
            return render(request, 'login.html', {'msg': u'用户不存在或密码错误!'})

    return render(request,'login.html',{'msg':u'欢迎回来'})

def v_logout(request):
    logout(request)
    return redirect('/login')

from datetime import datetime
@login_required
def record(request):
    if (request.method == 'POST'):
        starttime = request.POST['starttime'].replace('T',' ')
        endtime = request.POST['endtime'].replace('T',' ')
        date1 = datetime.strptime(starttime, '%Y-%m-%d %H:%M')
        date2 = datetime.strptime(endtime, '%Y-%m-%d %H:%M')
        hours_diff = (date2 - date1).total_seconds() / 3600
        print(request.user.id,starttime,endtime,hours_diff)
        record=recordinfo()
        record.userid=request.user.id
        record.starttime=starttime
        record.endtime=endtime
        record.hours=hours_diff
        record.save()
        return redirect('/history')
    return render(request,"record10.html")

#把返回的结果集变为字典
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@login_required
def history(request):
    with connection.cursor() as cursor:
        sql1="select substr(starttime,0,11) as day,hours from main_recordinfo where userid={} order by starttime limit 10;".format(request.user.id)
        sql2="select substr(starttime,0,11) as day,sum(hours) as hours from main_recordinfo where userid={} group by day order by starttime limit 10;".format(request.user.id)
        sql3="select substr(starttime,0,11) as day,substr(starttime,12,2) as shour,substr(endtime,12,2) as whour,hours from main_recordinfo where userid={} order by starttime limit 10;".format(request.user.id)
        cursor.execute(sql3)
        data = dictfetchall(cursor)
    x=[]
    y1=[]
    y2=[]
    y3=[]
    print(data)
    for item in data:
        x.append(item['day'])
        y1.append(item['hours'])
        y2.append(item['shour'])
        y3.append(item['whour'])
    return render(request,"history4.html",{'x':x,'y1':y1,'y2':y2,'y3':y3})




