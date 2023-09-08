from fastapi import APIRouter #, File, UploadFile, Form, Depends
from lib.all_configs import read_config
#import datetime as dt
from lib.save_base64_file import save_base64_file
from lib.core import  get_ext, join_ids
from .list import action_list
from .init_new_docpack_form import action_init_new_docpack_form
from .docpack_delete import action_docpack_delete
from .create_docpack import action_create_docpack
from .get_bills import action_get_bills
from .create_bill import action_create_bill
#import os

router = APIRouter()

#
@router.post('/{config}/{field_name}')
async def get_list(config:str, field_name:str, R:dict): # 
    form=read_config(
        action='get',
        config=config,
        id=R['id'],
        R=R,
        script='const'
    )
    action=R['action']
    field=form.get_field(field_name)
    
    if action=='list':
        return action_list(form,field)

    if action=='init_new_docpack_form':
        return action_init_new_docpack_form(form,field)
    
    if action == 'create_docpack':
        return action_create_docpack(form,field,R)
    
    if action == 'docpack_delete':
        return action_docpack_delete(form,R)

    if action=='get_bills':
        return action_get_bills(form,field,R)
    
    if action == 'create_bill':
        return action_create_bill(form,field, R)