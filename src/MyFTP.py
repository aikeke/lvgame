# /usr/bin/env python
# -*- coding: utf-8 -*-
# date:20201105

from ftplib import FTP
import os

class MyFTP(object):
    def __init__(self,host,port=21):
        self.host=host
        self.port=port
        self.ftp=FTP()

    def login(self,username,password):
        try:
            self.ftp.connect(self.host,self.port)
            self.ftp.login(username,password)
        except Exception as e:
            print('ftp connect fail!')
            return -1

    def download_file(self,remote_file,local_file):
        try:
            buf_size=1024
            file_handler=open(local_file,'wb')
            self.ftp.retrbinary('RETR {}'.format(remote_file),file_handler.write,buf_size)
            file_handler.close()
        except Exception as e:
            print('file download error!')
            return -1

    def upload_file(self, local_file, remote_file):
        if not os.path.isfile(local_file):
            print('%s 不存在' % local_file)
            return
        buf_size = 1024
        file_handler = open(local_file, 'rb')
        self.ftp.storbinary('STOR %s' % remote_file, file_handler, buf_size)
        file_handler.close()
        print('上传: %s' % local_file + "成功!")