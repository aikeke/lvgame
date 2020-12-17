import multiprocessing


class Mul_pool(object):
    def __init__(self):
        self.cores=multiprocessing.cpu_count()
        self.pool=multiprocessing.Pool(processes=self.cores)
        self.res=multiprocessing.Manager().dict()
    
    def get_pool(self,f,*args):
        return self.pool.apply_async(f,tuple(args))

    def get_dict(self):
        return self.res
        
    def Close(self):
        self.pool.close()
        self.pool.join()
