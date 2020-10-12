import redis
import json
def modify_host(host_name,host_ip,host_pass):
    redis_obj=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
    redis_obj.set(host_ip,host_pass)
    if 'war' in host_name:
        redis_obj.hset('wargame_server',host_name,host_ip)
        return 0
    elif 'login' in host_name:
        redis_obj.hset('login_server',host_name,host_ip)
        return 0
    elif 'game' in host_name:
        redis_obj.hset('game_server',host_name,host_ip)
        return 0
    else:
        return 1
def scan_host():
    res={}
    redis_obj=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
    game=redis_obj.hgetall('game_server')
    war=redis_obj.hgetall('wargame_server')
    login=redis_obj.hgetall('login_server')
    res['game']=game
    res['login']=login
    res['war']=war
    return res

def del_host(host_name,host_ip,host_pass):
    redis_obj=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
    oldpass=redis_obj.get(host_ip)
    if oldpass != host_pass:
        return 1
    if 'war' in host_name:
        redis_obj.hde1('wargame_server',host_name)
        return 0
    elif 'login' in host_name:
        redis_obj.hdel('login_server',host_name)
        return 0
    elif 'game' in host_name:
        redis_obj.hdel('game_server',host_name)
        return 0
    else:
        return 1
def test(host_name,host_ip,host_pass):
    redis_obj=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
    oldpass=redis_obj.get(host_ip)
    return oldpass
