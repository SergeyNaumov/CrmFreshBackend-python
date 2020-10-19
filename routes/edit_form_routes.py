from fastapi import APIRouter
#from lib.core import cur_year,cur_date,  exists_arg
from lib.all_configs import read_config
from .edit_form.process_edit_form import process_edit_form

from .wysiwyg_routes import router as wysiwyg_routes

router = APIRouter()


# форма добавления элемента
@router.post('/edit-form/{config}')
async def new_or_insert_form(config: str,R: dict):
  action='new'
  if 'action' in R:
    if R['action'] in ('insert'):
      action=R['action']
  return process_edit_form(
    action=action,
    config=config,
    R=R
  )

# class R_update(dict):


# update изменений в карте
@router.put('/edit-form/{config}/{id}')
async def update_form(config: str,id: int,R: dict):

  return process_edit_form(
    action='update',
    config=config,
    id=id,
    R=R
  )

@router.post('/edit-form/{config}/{id}')
async def worm_work(config:str,id:int,R:dict):
  action=''
  values=None
  print('R:',R)
  if 'action' in R: action=R['action']
  #if 'values' in R: values=R['values']
  return process_edit_form(
    action=action,
    config=config,
    id=id,
    R=R
  )




@router.get('/delete-element/{config}/{id}')
async def delete_element(config: str,id:int):
  form=read_config(
    config=config,
    id=id,
    script='delete_element',
    action=''
  )
  if not form.make_delete:
    form.errors.append('удаление запрещено')

  form.run_event('before_delete')
  if form.work_table_foreign_key and form.work_table_foreign_key_value:
    cnt=form.db.query(
      query=f'select count(*) from {form.work_table} WHERE {form.work_table_id}=%s and {form.work_table_foreign_key}=%s',
      values=[form.id,form.work_table_foreign_key_value],
      onevalue=1
    )
    if not cnt:
      form.errors.append('действие запрещено. запрещённый foreign_key. обратитесь к разработчику')

  
  if form.success():
    form.db.query(
      query=f'DELETE FROM {form.work_table} WHERE {form.work_table_id}=%s',
      values=[form.id],
      debug=1,
      errors=form.errors
    )

    form.run_event('after_delete')

    for f in form.fields:
      if 'after_delete' in f:
        form.run_event('after_delete',
          {
          'field':f
          }
        )

  return {'success':form.success(),'errors':form.errors,'log':form.log}


router.include_router(wysiwyg_routes)