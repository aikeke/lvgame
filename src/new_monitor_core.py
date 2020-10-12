#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os,sys,commands,re
import getopt,traceback
import time
from zabbix_sender import *

reload(sys)
sys.setdefaultencoding("utf-8")


def usage():
    print __doc__

def trace_back():
    try:
        return traceback.print_exc()
    except:
        return ""

def datarecv_print(datarecv):
    for key in datarecv.keys():
        print "%s: %s" % (key, datarecv[key])

__doc__ = '''Usage: python process.status.py [OPTIONS]
        -z, --zbx_host=name
            Connect to host of Zabbix Server.
        --zbx_port[=#]
            Port number of Zabbix Server to use for connection, built-in default (10051).
        -?, --help
            Display this help and exit.
    '''
def new_zbsend(zbx_target,zbx_host,zbx_port,flag):
    try:
        zbxdata = []
        zbxdata.append({"host":zbx_target, "key":"core_file", "value":int(flag)})
        zbxsender = zabbix_sender(zbx_host, zbx_port)
        zbxsender.send(zbxdata, datarecv_print)
    except:
        print trace_back()



if __name__ == "__main__":
    zbx_host = "10.1.11.46"
    zbx_port = 10051
    zbx_target = ""

    opts, args = getopt.getopt(sys.argv[1:], "z:s:?", ["zbx_host=", "zbx_port=", "help"])

    localip = commands.getoutput("/sbin/ifconfig eth1|grep Bcast|awk -F'addr:' '{print $2}'|awk '{print $1}'")
    if not zbx_target:
        zbx_target = localip

    record_file="/home/monitorCoreRecord/core_history.txt"
    if not os.path.exists(record_file):
        os.mknod(record_file)
    core_dir='/ss/game'
    for i in range(11):
        flag=0
        core_list=[]
        for filename in os.listdir(core_dir):
            if "core" in filename:
                core_list.append(filename)
        if len(core_list)==0:
            new_zbsend(zbx_target,zbx_host,zbx_port,flag)
            #print flag
            time.sleep(5)
        else:
            f=open(record_file,'r')
            data=f.read()
            f.close()
            for core in core_list:
                if core in data:
                    continue
                else:
                    flag=1
                    f2=open(record_file,'a')
                    f2.write(core)
                    f2.close()
            new_zbsend(zbx_target,zbx_host,zbx_port,flag)
            #print flag
            time.sleep(5)
                
             
