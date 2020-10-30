import importlib
import sys
sys.path.append('../')
from lvanapi.settings import PLUGIN_CALSS_DICT
def run():
    for key,path in PLUGIN_CALSS_DICT.items():
        module_path,class_name=path.rsplit('.',1)
        module=importlib.import_module(module_path)
        cls=getattr(module,class_name)
        plugin_obj=cls()
        info=plugin_obj.process('10.1.11.210',2208,'master','xxx')
        return key,info

if __name__=="__main__":
    print(run())       
