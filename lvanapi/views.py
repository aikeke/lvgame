from django.shortcuts import render,HttpResponse
import sys
sys.path.append('../')
from src import game_wall_check
from src import login_wall_check
from src import crontab_check
from src import update_register_check
from src import version_check
from src import game_status
from src import modify_host
from src import get_logger
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
def index(request):
    return render(request,'login.html')
def login(request):
    return render(request,'login.html')
def game_iptables_check(request):
    data=game_wall_check.check()
    sm,zxy=sep(data)
    return render(request,'game_iptables_check.html',{"sm": sm,"zxy":zxy})
def login_iptables_check(request):
    data=login_wall_check.check()
    sm,zxy=sep(data)
    return render(request,'login_iptables_check.html',{"sm": sm,"zxy":zxy})
def ver(request):
    data=version_check.check()
    sm,zxy=sep(data)
    return render(request,'version_check.html',{"sm": sm,"zxy":zxy})
def update(request):
    data=update_register_check.check()
    sm,zxy=sep(data)
    return render(request,'update.html',{"sm": sm,"zxy":zxy})
def game_check(request):
    data=game_status.check()
    sm,zxy=sep(data)
    return render(request,'game_check.html',{"sm": sm,"zxy":zxy})
def cron(request):
    data=crontab_check.check()
    sm,zxy=sep(data)
    return render(request,'cron_check.html',{"sm": sm,"zxy":zxy})
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



