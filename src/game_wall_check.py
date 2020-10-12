from ssh_connect import Ssh
import redis
import json
def check():
    redis_obj=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
    res={}
    data=redis_obj.hgetall('game_server')
    for key,value in data.items():
        ssh_obj=Ssh(value,2208,"master",redis_obj.get(value))
        ssh_obj.connect()
        try:
            result=ssh_obj.cmd('''cat /etc/sysconfig/iptables|grep '#'|wc -l ''',sudo=True)
            wall_num=result.strip()
            if wall_num == '2':
                res[key]='open'
            else:
                res[key]='close'
        except Exception as e:
            res[key]='wrong'
            pass
        ssh_obj.close()
        continue
    return res
