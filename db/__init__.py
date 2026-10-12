from config import config
from .freshdb import FreshDB
from .freshdbs import FreshDB as FreshDBSync

crm_write=config['connects']['crm_write']
#crm_read=config['connects']['crm_read']

db=None
# Второе подключение -- внешняя CRM (БД strateg) для стартовой страницы
# svcmsmanager. Настраивается ключом config['connects']['strateg'].
strateg_db=None

def get_db(**arg):
    global db
    if db:
        return db

    if arg.get('sync'):
        db=FreshDBSync(crm_write)
    else:
        db=FreshDB(crm_write)
    return db

def get_strateg_db():
    global strateg_db
    if strateg_db:
        return strateg_db
    strateg_conf=config.get('connects',{}).get('strateg')
    if not strateg_conf:
        return None
    strateg_db=FreshDB(strateg_conf)
    return strateg_db


# {'host':'localhost', 'port':3306, 'user':'fas', 'password':'', 'db':'fas'}

    #with engine.connect() as conn:
    #    result = conn.execute(text("SELECT * FROM user limit 1"))
    #    pprint(result.all())