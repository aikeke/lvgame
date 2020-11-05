# /usr/bin/env python
# -*- coding: utf-8 -*-
# date: 20201105

from MyFTP import MyFTP
import commands
from BaseResponse import BaseResponse
result=BaseResponse()
gmfile_list=['autorun.gmc','point_shop_item.csv','point_shop_type.csv','worldevent.csv']
game_path='/ss/game/'
temp_path='/tmp/'
cmd='cat /ss/game/server_user.ini|grep MaxLimit'
level=commands.getoutput(cmd).split('=')[1]
host_name=commands.getoutput('hostname')
if 'shumen' in host_name:
    host_name='sm'
else:
    host_name='zxy'
remote_path='/upload/{}/{}/'.format(host_name,level)

ftp=MyFTP('10.1.0.67')
ftp.login('uploadUI','xxx')
for item in gmfile_list:
    remote_path_file=remote_path+item
    temp_path_file=temp_path+item
    res=ftp.download_file(remote_path_file,temp_path_file)
    if res == -1:
        result.status=False
        result.error='error'
        print(result.dict())
        continue
    cmd='''\cp -f {} {}'''.format(temp_path_file,game_path)
    commands.getoutput(cmd)
    cmd2='/usr/bin/md5sum /ss/game/{}'.format(item)
    status,data=commands.getstatusoutput(cmd2)
    result.status=status
    result.data=data
    print(result.dict())