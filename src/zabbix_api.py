#/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
class ZabbixApi(object):
    def __init__(self):
        self.__url = 'http://XXX/zabbix/api_jsonrpc.php'
        self.__user = 'aiyanfeng'
        self.__password = 'XXX'
        self.__header = {"Content-Type": "application/json"}
        self.__token_id = self.UserLogin()

    def UserLogin(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.__user,
                "password": self.__password
            },
            "id": 0,
        }
        return self.PostRequest(data)

    def PostRequest(self, data):
        request = requests.post(self.__url,headers=self.__header,data=json.dumps(data))        
        res=json.loads(request.text)['result']
        return res

    def HostGet(self,hostip=None):
        data = {
            "jsonrpc":"2.0",
            "method":"host.get",
            "params":{
                "output": [ "hostid","host",'name' ],
                "filter": {
                        "host": hostip
                }
                #"selectGroups": "extend",
                #"selectParentTemplates": ["templateid","name"],
                #"selectInterfaces": ["interfaceid","ip"],
                #"selectInventory": ["os"],
                #"selectItems":["itemid","name"],
                #"selectGraphs":["graphid","name"],
                #"selectApplications":["applicationid","name"],
                #"selectTriggers":["triggerid","name"],
                #"selectScreens":["screenid","name"]
            },
            "auth": self.__token_id,
            "id":1,
        }
       # if hostid:
        #    data["params"]={
         #       "output": "extend",
          #      "hostids": hostid,
          #      "sortfield": "name"
          #  }
        return  self.PostRequest(data)

    def ItemGet(self,hostid=None,itemid=None):
        data = {
            "jsonrpc":"2.0",
            "method": "item.get",
            "params": {
                "output": ["itemid","hostid"],
                "hostids": hostid,
                #"itemids": itemid,
                "search": {
                    "key_":"time_diff"
                },
            },
            "auth": self.__token_id,
            "id":1,
        }
        return  self.PostRequest(data)

    def History(self,itemid,data_type):
        data = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": data_type,
                "itemids": itemid,
                "sortfield": "clock",
                "sortorder": "DESC",
                "limit": 50
            },
            "auth": self.__token_id,
            "id": 2
        }
        return self.PostRequest(data)

za_obj=ZabbixApi()
host_list=['10.1.11.139', '10.1.11.142', '10.1.11.135', '10.1.11.137', '10.1.11.203', '10.1.11.222', '10.1.11.144', '10.1.11.107', '10.1.11.112', '10.1.11.116', '10.1.11.118', '10.1.11.138', '10.1.11.117', '10.1.11.233', '10.1.11.122', '10.1.11.244', '10.1.11.204', '10.1.11.234', '10.1.11.120', '10.1.11.195', '10.1.11.125', '10.1.11.130', '10.1.11.224', '10.1.11.176', '10.1.11.193', '10.1.11.238', '10.1.11.239', '10.1.11.240', '10.1.11.172', '10.1.11.174', '10.1.11.249', '10.1.11.114', '10.1.11.230', '10.1.11.150', '10.1.11.188', '10.1.11.128', '10.1.11.228', '10.1.11.236', '10.1.11.225']
res=za_obj.HostGet(host_list)
hostid_list=[]
for i in res:
    hostid_list.append(i['hostid'])
item_res=za_obj.ItemGet(hostid_list)
itemid_list=[]
for i in item_res:
    itemid_list.append(i['itemid'])
time_res=za_obj.History(itemid_list,0)
for item in res:
    for i in item_res:
        if item['hostid']==i['hostid']:
            item['itemid']=i['itemid']
for item in res:
    for i in time_res:
        if item['itemid']==i['itemid']:
            item['value']=i['value']
for item in res:
    print(json.dumps(item,encoding='utf-8',ensure_ascii=False))
