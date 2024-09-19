from fastapi import APIRouter, Request
#from lib.core import cur_year,cur_date,  exists_arg
from lib.all_configs import read_config
from .edit_form.process_edit_form import process_edit_form

from .wysiwyg_routes import router as wysiwyg_routes
from .edit_form.multiconnect import multiconnect_process
router = APIRouter()


# форма добавления элемента
@router.post('/edit-form/{config}')
async def new_or_insert_form(config: str,R: dict,request:Request):
  action='new'
  if 'action' in R:
    if R['action'] in ('insert'):
      action=R['action']
  return await process_edit_form(
    request=request,
    action=action,
    config=config,
    R=R
  )

# class R_update(dict):


# update изменений в карте
@router.put('/edit-form/{config}/{id}')
async def update_form(config: str,id: int,R: dict,request:Request):
  return await process_edit_form(
    request=request,
    action='update',
    config=config,
    id=id,
    R=R
  )

@router.post('/edit-form/{config}/{id}')
async def work_form(config:str,id:int,R:dict,request:Request):
  action=''
  #values=None

  if 'action' in R: action=R['action']
  else:
    action='edit'
  #print('action:',action)
  return await process_edit_form(
    request=request,
    action=action,
    config=config,
    id=id,
    R=R
  )



@router.get('/delete-element/{config}/{id}')
async def delete_element(config: str,id:int,request:Request):
  form = await read_config(
    request=request,
    config=config,
    id=id,
    script='delete_element',
    action='delete'
  )
  if not form.make_delete:
    form.errors.append('удаление запрещено')

  await form.run_event('before_delete')
  if form.work_table_foreign_key and form.work_table_foreign_key_value:
    cnt = await form.db.query(
      query=f'select count(*) from {form.work_table} WHERE {form.work_table_id}=%s and {form.work_table_foreign_key}=%s',
      values=[form.id,form.work_table_foreign_key_value],
      onevalue=1
    )
    if not cnt:
      form.errors.append('действие запрещено. запрещённый foreign_key. обратитесь к разработчику')

  
  if form.success():
    await form.db.query(
      query=f'DELETE FROM {form.work_table} WHERE {form.work_table_id}=%s',
      values=[form.id],
      errors=form.errors
    )

    await form.run_event('after_delete')

    for f in form.fields:
      if 'after_delete' in f:
        await form.run_event('after_delete',{'field':f})

  return {'success':form.success(),'errors':form.errors,'log':form.log}

@router.post('/multiconnect/{config}/{field_name}')
async def multiconnect(config:str,field_name:str,R:dict, request:Request):
  return await multiconnect_process(
    request=request,
    config=config,
    field_name=field_name,
    R=R
  )


router.include_router(wysiwyg_routes)
