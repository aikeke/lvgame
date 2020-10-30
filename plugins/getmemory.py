from plugins.base import Base
from src.ssh_connect import Ssh
class GetMem(Base):
    def __init__(self):
        pass

    def process(self,host,port,user,passwd):
        cmd='''free -m |grep Mem|awk '{print $2}' '''
        ssh=Ssh(host,port,user,passwd)
        ssh.connect()
        res,err=ssh.cmd(cmd)
        if err:
            return err
        else:
            return res
