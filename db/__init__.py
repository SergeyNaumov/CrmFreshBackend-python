#from config import config
import os
from .freshdb import FreshDB
from .freshdbs import FreshDB as FreshDBSync




db_user=os.environ.get('DB_USER')
db_host=os.environ.get('DB_HOST')
db_port=os.environ.get('DB_PORT')
db_password=os.environ.get('DB_PASSWORD','')
db_name=os.environ.get('DB_NAME')
PRODUCTION = os.environ.get('PRODUCTION')

if not(db_name):
    db_user='crm'
    db_host='localhost'
    db_name='crm'
    db_port='3306'

if db_port:
    db_port=int(db_port)

crm_write={
  'user':db_user,
  'password':db_password,
  'host':db_host,
  'port':db_port,
  'dbname':db_name,
}
#crm_write=config['connects']['crm_write']
#crm_read=config['connects']['crm_read']

db=None

def get_db(**arg):
    global db
    if db:
        return db

    if arg.get('sync'):
        db=FreshDBSync(crm_write)
    else:
        db=FreshDB(crm_write)
    return db


# {'host':'localhost', 'port':3306, 'user':'fas', 'password':'', 'db':'fas'}

    #with engine.connect() as conn:
    #    result = conn.execute(text("SELECT * FROM user limit 1"))
    #    pprint(result.all())
