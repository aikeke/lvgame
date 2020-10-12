import paramiko
import redis
class Ssh(object):
    def __init__(self,host,port,username,passwd):
        self.host=host
        self.port=port
        self.username=username
        self.passwd=passwd
    def connect(self):
        transport=paramiko.Transport((self.host,self.port))
        transport.connect(username=self.username,password=self.passwd)
        self.__transport=transport
    def close(self):
        self.__transport.close()
    def cmd(self,command,sudo=False):
        ssh_client=paramiko.SSHClient()
        ssh_client._transport=self.__transport
        if sudo and self.username != "root":
            command='''sudo -p '' {}'''.format(command)
            stdin,stdout,stderr=ssh_client.exec_command(command)
            stdin.write(self.passwd + '\n')
            stdin.flush()
        else:
            stdin,stdout,stderr=ssh_client.exec_command(command)
        result=stdout.read()+stderr.read()
        return result
    def getfile(self,remote_path,local_path):
        sftp=paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path,local_path)
   
