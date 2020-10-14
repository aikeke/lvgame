#/usr/bin/python
#-*- coding: utf-8 -*-
#author: aikeke
#获取当前所有线上游戏的版本号
from ssh_connect import Ssh
from common import get_redis
from mul_pool import Mul_pool
import threading
def get_version(key,value,port=2208,user="master"):
    ver={}
    #global ver
    redis_obj=get_redis()
    ssh_obj=Ssh(value,port,user,redis_obj.get(value))
    ssh_obj.connect()
    try:
        result=ssh_obj.cmd('''cat /ss/login/ver|grep name ''')
        version=result.strip().split()[2]
        ver[key]=version
    except Exception as e:
        ver[key]='error'
        pass
    ssh_obj.close()
    return ver

def check():
    res={}
    redis_obj=get_redis()
    data=redis_obj.hgetall('login_server')
    pool=Mul_pool()
    pool_list=[]
    for key,value in data.items():
        pool_list.append(pool.get_pool(get_version,key,value))
    for item in pool_list:
        res.update(item.get())   
    pool.close()
    return res

def thread_check():
    redis_obj=get_redis()
    data=redis_obj.hgetall('login_server')
    thread_list=[]
    for key,value in data.items():
        t=threading.Thread(target=get_version,args=[key,value,])
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()

if __name__=='__main__':
#实测当前情况多线程比多进程快了一倍,主要限于进程数量的限制导致。
    import time
    start_time=time.time()
    ver={}
    #global ver
    thread_check()
    print time.time()-start_time    
    print ver
