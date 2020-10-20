#/usr/bin/python
#-*- coding: utf-8 -*-
#author: aikeke
# 防火墙对内对外
from ssh_connect import Ssh
from common import get_redis
from get_logger import get_logger

ans={}

def modify_iptables(cmd_str,key,value,port=2208,user="lvantech"):
    global ans
    redis_obj=get_redis()
    ssh_obj=Ssh(value,2208,user,redis_obj.hget(user,value))
    try:
        ssh_obj.connect()
        result,err=ssh_obj.cmd(cmd_str,sudo=True)
        if not err.strip():
            ans[key]='sucess'
        else:
            print err
    except Exception as e:
        ans[key]='wrong'
        pass

if __name__=='__main__':
    prompt='''please input your choice:
1: 所有游戏对内
2: 所有游戏对外
3: 所有登录对内
4: 所有登录对外
'''
    argv=raw_input(prompt)
    redis_obj=get_redis()
    if argv=='1':
        data=redis_obj.hgetall('smgame_server')
        for key,value in data.items():
            result=modify_iptables('cat /etc/sysconfig/iptables|wc -l',key,value)
        get_logger('modify_iptables').info(ans)
    elif argv=='2':
        data=redis_obj.hgetall('smgame_server')
        for key,value in data.items():
            result=modify_iptables(game_outer_cmd,key,value)
    elif argv=='3':
        data=redis_obj.hgetall('smlogin_server')
        for key,value in data.items():
            result=modify_iptables(login_inside_cmd,key,value)
    elif argv=='4':
        data=redis_obj.hgetall('smlogin_server')
        for key,value in data.items():
            result=modify_iptables(login_outer_cmd,key,value)
    else:
        exit("输入异常")
