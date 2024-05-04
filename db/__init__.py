from config import config
from .freshdb import FreshDB
crm_write=config['connects']['crm_write']
#crm_read=config['connects']['crm_read']


db_read=db_write=db=FreshDB(crm_write)

# {'host':'localhost', 'port':3306, 'user':'fas', 'password':'', 'db':'fas'}

    #with engine.connect() as conn:
    #    result = conn.execute(text("SELECT * FROM user limit 1"))
    #    pprint(result.all())