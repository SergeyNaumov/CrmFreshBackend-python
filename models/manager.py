import datetime
from peewee import *
from db import dbhandle, BaseModel


class Model(BaseModel):
    id = PrimaryKeyField(null=False)
    login = CharField(max_length=20)
    password = CharField(max_length=50)
    email = CharField(max_length=50)
    name = CharField(max_length=50)
    phone = CharField(max_length=50)
    registered = DateTimeField(default=datetime.datetime.now())
    type = SmallIntegerField(default=0)
    #updated_at = DateTimeField(default=datetime.datetime.now())
    
    class Meta:
        db_table = "manager"
        order_by = ('registered desc',)