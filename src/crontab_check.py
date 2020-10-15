#/usr/bin/python
#-*- coding: utf-8 -*-
#author: aikeke
# 获取定时任务数
from ssh_connect import Ssh
from common import get_redis
from get_logger import get_logger
import threading
res={}
def get_cron(key,value,port=2208,user="master"):
    global res
    redis_obj=get_redis()
    ssh_obj=Ssh(value,2208,"master",redis_obj.get(value))
    try:
        ssh_obj.connect()
        result,err=ssh_obj.cmd('''cat /etc/crontab|wc -l ''',sudo=True)
        wall_num=result.strip()
        res[key]=wall_num
    except Exception as e:
        res[key]='wrong'
        get_logger().error("pass is wrong")
        pass
    ssh_obj.close()

def thread_check():
    redis_obj=get_redis()
    data=redis_obj.hgetall('game_server')
    thread_list=[]
    for key,value in data.items():
        t=threading.Thread(target=get_cron,args=[key,value])
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
