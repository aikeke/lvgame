from ssh_connect import Ssh
import redis
import json
def check():
    redis_obj=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
    data=redis_obj.hgetall('login_server')
    result={}
    for key,value in data.items():
        ssh_obj=Ssh(value,2208,"master",redis_obj.get(value))
        ssh_obj.connect()
        try: 
            temp=ssh_obj.cmd('''cat /etc/sysconfig/iptables|grep '#'|wc -l ''',sudo=True)
            wall_num=temp.strip()
            if wall_num == '2':
                result[key]='open'
                #print '\033[1;32m{:15s} is open  to player!\033[0m'.format(key)
            else:
                result[key]='close'
                #print '\033[1;31m{:15s} is close to player!\033[0m'.format(key)
        except Exception as e:
            result[key]='error'
            #print('{} pass is wrong'.format(key))
            pass
        ssh_obj.close()
        continue
    return result

