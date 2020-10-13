import redis
def get_redis():
    redis_obj=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
    return redis_obj
