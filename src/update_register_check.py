#/usr/bin/python
#-*- coding: utf-8 -*-
#author: aikeke
# 查看更新机注册信息
from ssh_connect import Ssh
from common import get_redis
from get_logger import get_logger
import threading
res={}
def get_update(key,value,port=2208,user="master"):
    global res
    redis_obj=get_redis()
    ssh_obj=Ssh(value,2208,"master",redis_obj.get(value))
    try:
        ssh_obj.connect()
        result=ssh_obj.cmd(''' grep 'Up' `ls -rt /ss/login/log/login*|tail -1` ''')
        update=result.strip()
        res[key]=update
    except Exception as e:
        res[key]='error'
        get_logger().error("pass is wrong")
        pass

def thread_check():
    redis_obj=get_redis()
    data=redis_obj.hgetall('login_server')
    thread_list=[]
    for key,value in data.items():
        t=threading.Thread(target=get_update,args=[key,value])
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()

def check():
    thread_check()
    return res

if __name__=='__main__':
    result=check()
    print result
