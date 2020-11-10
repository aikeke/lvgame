from django.shortcuts import render,HttpResponse,redirect
import sys
sys.path.append('../')
from lvanapi import models
from functools import wraps
from src import game_wall_check
from src import login_wall_check
from src import crontab_check
from src import update_register_check
from src import version_check
from src import game_status
from src import login_status
from src import modify_host
from src import modify_iptables
from src import get_logger

def check_login(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        if request.session.get('is_login')=='1':
            return func(request,*args,**kwargs)
        else:
            return redirect('/login/')
    return wrapper

def sep(data):
    zxy={}
    sm={}
    for key,values in data.items():
        if 'zxy' in key:
            zxy[key]=values
        else:
            sm[key]=values
    return sm,zxy
# Create your views here.

def hostinfo_api(request):
    if request.method=='POST':
        hostname=request.POST.get('hostname','')
        inner_ip=request.POST.get('inner_ip')
        outer_ip=request.POST.get('outer_ip','')
        disk_size=request.POST.get('disk_size','')
        memory=request.POST.get('memory','')
        cpu=request.POST.get('cpu','')
        models.HostInfo.objects.filter(inner_ip=inner_ip).delete()
        models.HostInfo.objects.create(hostname=hostname,inner_ip=inner_ip,outer_ip=outer_ip,disk_size=disk_size,memory=memory,cpu=cpu)
        return HttpResponse(' info post ok')
    else:
        return HttpResponse('ok')

@check_login
def index(request):
    return render(request,'index.html')

@check_login
def game_iptables_check(request):
    data=game_wall_check.check()
    sm,zxy=sep(data)
    return render(request,'game_iptables_check.html',{"sm": sm,"zxy":zxy})

@check_login
def login_iptables_check(request):
    data=login_wall_check.check()
    sm,zxy=sep(data)
    return render(request,'login_iptables_check.html',{"sm": sm,"zxy":zxy})

@check_login
def ver(request):
    data=version_check.check()
    sm,zxy=sep(data)
    return render(request,'version_check.html',{"sm": sm,"zxy":zxy})

@check_login
def update(request):
    data=update_register_check.check()
    sm,zxy=sep(data)
    return render(request,'update.html',{"sm": sm,"zxy":zxy})

@check_login
def game_check(request):
    data=game_status.check()
    sm,zxy=sep(data)
    return render(request,'game_check.html',{"sm": sm,"zxy":zxy})

@check_login
def login_check(request):
    data=login_status.check()
    sm,zxy=sep(data)
    return render(request,'login_check.html',{"sm": sm,"zxy":zxy})

@check_login
def cron(request):
    data=crontab_check.check()
    sm,zxy=sep(data)
    return render(request,'cron_check.html',{"sm": sm,"zxy":zxy})

@check_login
def iptables(request):
    rule=request.GET.get('rules')
    #modify_iptables.excute_iptables(rule)
    if rule=='gmoff' or rule=='gmon':
        return redirect('/game_iptables_check/')
    else:
        return redirect('/login_iptables_check/')

@check_login
def host(request):
    if request.method=='GET':
        data=modify_host.scan_host()
        return render(request,'host.html',{"game":data['game'],"login":data['login'],"war":data['war']})
    elif request.method=="POST":
        ac=request.POST.get('ac')
        hostname=request.POST.get('hostname')
        hostip=request.POST.get('hostip')        
        hostpass=request.POST.get('hostpass')
        if ac=='add':
            flag=modify_host.modify_host(hostname,hostip,hostpass)
            if flag==1:
                return HttpResponse('hostname error!')
            return HttpResponse('modify host success!')
        else:
            flag=modify_host.del_host(hostname,hostip,hostpass)
            if flag==1:
                return HttpResponse('hostname error or pass error!')
            return HttpResponse('delete host success!')
    else:
        return render(request,'login.html')


def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    elif request.method=='POST':
        username=request.POST.get('user')
        pwd=request.POST.get('pass')
        user=models.UserInfo.objects.filter(username=username,password=pwd)
        if user:
            request.session['is_login']='1'
            return redirect('/index/')
        return redirect('/login/')

