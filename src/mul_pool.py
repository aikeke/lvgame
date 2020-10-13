import multiprocessing


class Mul_pool(object):
    def __init__(self):
        self.cores=multiprocessing.cpu_count()
        self.pool=multiprocessing.Pool(processes=self.cores)
    
    def get_pool(self,f,*args):
        return self.pool.apply_async(f,tuple(args))
        
    def close(self):
        self.pool.close()
        self.pool.join()
