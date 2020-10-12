from ssh_connect import Ssh
import redis
import json
def check():
    res={}
    redis_obj=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
    data=redis_obj.hgetall('login_server')
    for key,value in data.items():
        ssh_obj=Ssh(value,2208,"master",redis_obj.get(value))
        ssh_obj.connect()
        try: 
            result=ssh_obj.cmd('''cat /ss/login/ver|grep name ''')
            version=result.strip().split()[2]
            res[key]=version
        except Exception as e:
            res[key]='error'
            pass
        ssh_obj.close()
        continue
    return res
    
