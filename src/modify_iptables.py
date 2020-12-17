#/usr/bin/python
#-*- coding: utf-8 -*-
#author: aikeke
# 防火墙对内对外
from ssh_connect import Ssh
from common import get_redis
from get_logger import get_logger
from mul_pool import Mul_pool

game_inside_cmd=''' sed -i -e '/28880/s/^/#/' -e '/28881/s/^/#/' -e '/28882/s/^/#/' -e '/28883/s/^/#/' -e '/38887/s/^/#/' -e '/48887/s/^/#/' -e '/58887/s/^/#/' -e '/28885/s/^/#/' -e '/28958/s/^/#/' -e '/9002/s/^/#/' -e '/9003/s/^/#/' -e '/9005/s/^/#/' -e '/9006/s/^/#/' -e '/28886/s/^/#/' -e '/28887/s/^/#/' /etc/sysconfig/iptables '''

game_outer_cmd=''' sed -i -e  '/28880/s/^#\{1,50\}//' -e '/28881/s/^#\{1,50\}//'  -e '/28882/s/^#\{1,50\}//' -e '/28883/s/^#\{1,50\}//' -e '/38887/s/^#\{1,50\}//' -e '/48887/s/^#\{1,50\}//' -e '/58887/s/^#\{1,50\}//' -e '/28885/s/^#\{1,50\}//' -e '/28958/s/^#\{1,50\}//' -e '/9002/s/^#\{1,50\}//' -e '/9003/s/^#\{1,50\}//' -e '/9005/s/^#\{1,50\}//' -e '/9006/s/^#\{1,50\}//' -e '/28886/s/^#\{1,50\}//' -e '/28887/s/^#\{1,50\}//' /etc/sysconfig/iptables '''

login_inside_cmd=''' sed -i -e '/28885/s/^/#/' -e '/28958/s/^/#/' /etc/sysconfig/iptables '''

login_outer_cmd=''' sed -i -e '/28885/s/^#\{1,50\}//' -e '/28958/s/^#\{1,50\}//' /etc/sysconfig/iptables '''


def modify_iptables(res,cmd_str,key,value,port=2208,user="lvantech"):
    redis_obj=get_redis()
    ssh_obj=Ssh(value,2208,user,redis_obj.hget(user,value))
    try:
        ssh_obj.connect()
        result,err=ssh_obj.cmd(cmd_str,sudo=True)
        if not err.strip():
            cmd_str='''/etc/init.d/iptables restart '''
            result,err=ssh_obj.cmd(cmd_str,sudo=True)
            if err.strip():
                res[key]=err
            else:
                res[key]=result
    except Exception as e:
        res[key]='pass is wrong'
        pass
    #get_logger('modify_iptables').info(ans)

def excute_iptables(argv):
    redis_obj=get_redis()
    p=Mul_pool()
    res=p.get_dict()
    if argv=='gmoff':
        data=redis_obj.hgetall('smgame_server')
        for key,value in data.items():
            p.get_pool(modify_iptables,res,game_inside_cmd,key,value)
    elif argv=='gmon':
        data=redis_obj.hgetall('smgame_server')
        for key,value in data.items():
            p.get_pool(modify_iptables,res,game_outer_cmd,key,value)
    elif argv=='lgoff':
        data=redis_obj.hgetall('smlogin_server')
        for key,value in data.items():
            p.get_pool(modify_iptables,res,login_inside_cmd,key,value)
    elif argv=='lgon':
        data=redis_obj.hgetall('smlogin_server')
        for key,value in data.items():
            p.get_pool(modify_iptables,res,login_outer_cmd,key,value)
    p.Close()
    get_logger('modify_iptables').info(res)

if __name__=='__main__':
    prompt='''please input your choice:
1: 所有游戏对内
2: 所有游戏对外
3: 所有登录对内
4: 所有登录对外
'''
    argv=raw_input(prompt)
    p=Mul_pool()
    res=multiprocessing.Manager().dict()
    redis_obj=get_redis()
    if argv=='1':
        data=redis_obj.hgetall('smgame_server')
        for key,value in data.items():
            result=modify_iptables(game_inside_cmd,key,value)
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
            p.get_pool(modify_iptables,res,login_outer_cmd,key,value)
        p.Close()
        print(res)
    else:
        exit("输入异常")
