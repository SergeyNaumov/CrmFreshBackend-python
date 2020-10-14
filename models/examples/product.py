import datetime
from peewee import *
from db import dbhandle, BaseModel
from models.category import Model as Category
class Model(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)
    price = FloatField(default=None)
    category = ForeignKeyField(Category, related_name='fk_cat_prod', to_field='id', on_delete='cascade',
                               on_update='cascade')
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())
 
    class Meta:
        db_table = "products"
        order_by = ('created_at',)