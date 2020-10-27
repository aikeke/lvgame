#/usr/bin/python 
#-*- coding: utf-8 -*-
#author: aikeke
#获取当前线上登录状态
from ssh_connect import Ssh
from common import get_redis
import threading
from get_logger import get_logger
res={}
def get_loginstatus(key,value,port=2208,user="master"):
    redis_obj=get_redis()
    global res
    ssh_obj=Ssh(value,2208,user,redis_obj.get(value))
    try:    
        ssh_obj.connect()
        result,err=ssh_obj.cmd('ps -ef|grep server|grep -v grep|wc -l')
        result=result.strip()
        if result == '2':
            res[key]='ok'
        else:
            res[key]='error'
    except Exception as e:
        res[key]='pass wrong'
        get_logger().error("pass is wrong")
        pass
    ssh_obj.close()

def thread_check():
    redis_obj=get_redis()
    data=redis_obj.hgetall('login_server')
    thread_list=[]
    for key,value in data.items():
        t=threading.Thread(target=get_loginstatus,args=[key,value])
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()

def check():
    #res={}
    thread_check()
    return res

if __name__=='__main__':
    result=check()
    print result
