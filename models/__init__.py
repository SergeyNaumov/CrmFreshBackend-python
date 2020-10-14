
import peewee
from db import dbhandle
import os
import importlib

try:
    print('connect to database')
    dbhandle.connect()
except peewee.InternalError as px:
    print(str(px))


models={}
files = os.listdir('./models')
for f in files:

    filename, ext = os.path.splitext(f)
    if  ext=='.py' and f !='__init__.py':
        spec = importlib.util.spec_from_file_location(filename, './models/'+f)
        cur_module = importlib.util.module_from_spec(spec)
        print('init_model:',cur_module)
        spec.loader.exec_module(cur_module)
        models[filename]=cur_module.Model

        try:
            cur_module.Model().create_table()
        except peewee.InternalError as px:
            print('str: ',str(px))
        
def get_all_models():
    lst=[]
    for k in models.keys():
        lst.append(k)
    return lst

