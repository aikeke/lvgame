from ssh_connect import Ssh
import redis
def check():
    res={}
    redis_obj=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
    data=redis_obj.hgetall('game_server')
    for key,value in data.items():
        ssh_obj=Ssh(value,2208,"master",redis_obj.get(value))
        ssh_obj.connect()
        try:
            result=ssh_obj.cmd('ps -ef|grep server|grep -v grep|wc -l')
            result=result.strip()
            if result == '6':
                res[key]='ok'
            else:
                res[key]='error'
        except Exception as e:
            res[key]='pass wrong'
            pass
        ssh_obj.close()
        continue
    
    data2=redis_obj.hgetall('wargame_server')
    for key,value in data2.items():
        ssh_obj=Ssh(value,2208,"master",redis_obj.get(value))
        ssh_obj.connect()
        try:
            result=ssh_obj.cmd('ps -ef|grep server|grep -v grep|wc -l')
            result=result.strip()
            if result == '6':
                res[key]='ok'
            else:
                res[key]='error'
        except Exception as e:
            res[key]='pass wrong'
            pass
        ssh_obj.close()
        continue
    return res
