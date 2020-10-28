# from peewee import *
 
# user = 'crm'
# password = ''
# db_name = 'crm'
 
# dbhandle = MySQLDatabase(
#     db_name, user=user,
#     password=password,
#     host='localhost'
# )

# class BaseModel(Model):
#     class Meta:
#         database = dbhandle

from .freshdb import FreshDB
from config import config
#def connect():
#  return FreshDB(dbname='crm',user='crm')


crm_read=config['connects']['crm_read']
crm_write=config['connects']['crm_read']

#print('connect_read!')
db_read=FreshDB(
  dbname=crm_read['dbname'],
  user=crm_read['user'],
  password=crm_read['password'],
  host=crm_read['host'],
)
#print('connect_write')
db_write=FreshDB(
  dbname=crm_write['dbname'],
  user=crm_write['user'],
  password=crm_write['password'],
  host=crm_write['host'],
)
db=db_write
