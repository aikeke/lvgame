class BaseResponse(object):
    def __init__(self,status=True,data=None,error=None):
        self.status=status
        self.data=data
        self.error=error

    def dict(self):
        return self.__dict__
