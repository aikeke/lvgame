import redis
def get_redis():
    r=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0)
    redis_obj=redis.StrictRedis(connection_pool=r)
    return redis_obj
