import importlib
import sys
import requests
sys.path.append('../')
from lvanapi.settings import PLUGIN_CALSS_DICT
def run():
    res={}
    for key,path in PLUGIN_CALSS_DICT.items():
        module_path,class_name=path.rsplit('.',1)
        module=importlib.import_module(module_path)
        cls=getattr(module,class_name)
        plugin_obj=cls()
        info=plugin_obj.process('10.1.11.210',2208,'master','exg%1lurpym0nowakqsh')
        res[key]=info.strip()
    return res

def hostinfo_update():
    data=run()
    print data
    url='http://10.1.11.210:8080/hostinfo/api/'
    r=requests.post(url,data)
    print r.content

if __name__=="__main__":
    hostinfo_update()
