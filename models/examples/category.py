import datetime
from peewee import *
from db import dbhandle, BaseModel

class Model(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)
 
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())
 
    class Meta:
        db_table = "categories"
        order_by = ('created_at',)