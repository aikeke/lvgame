from plugins.base import Base
from src.ssh_connect import Ssh
class GetHostname(Base):
    def __init__(self):
        pass

    def process(self,host,port,user,passwd):
        cmd='''hostname |awk -F. '{print $1}' '''
        ssh=Ssh(host,port,user,passwd)
        ssh.connect()
        res,err=ssh.cmd(cmd)
        if err:
            return err
        else:
            return res
