from fastapi import APIRouter, Request
#from lib.core import cur_year,cur_date,  exists_arg
from lib.all_configs import read_config
from .edit_form.process_edit_form import process_edit_form

from .wysiwyg_routes import router as wysiwyg_routes
from .edit_form.multiconnect import multiconnect_process
router = APIRouter()


# get-ы нужны для обработки кастомных запросов
@router.get('/edit-form/{config}')
async def edit_form_custom(config: str, request: Request):
  # request.query_params - это мультидикт, преобразуем в обычный dict
  R = dict(request.query_params)
  return await process_edit_form(
    request=request,
    action=R.get('action',''),
    config=config,
    id=R.get('id'),
    R=R
  )
  return R
@router.get('/edit-form/{config}/{_id}')
async def edit_form_custom(config: str, _id:int, request: Request):
  # request.query_params - это мультидикт, преобразуем в обычный dict
  R = dict(request.query_params)
  return await process_edit_form(
    request=request,
    action=R.get('action',''),
    config=config,
    id=_id,
    R=R
  )
  return R

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
    # Каскад перед удалением записи: файлы (base+ресайзы) записи и её file-полей,
    # дети 1_to_m, потомки дерева — чтобы не оставалось файловых «хвостов».
    try:
      from lib.svcmsmanager import ds_files
      await ds_files.cascade_delete(form, form.id)
    except Exception as e:
      form.errors.append(f'ошибка удаления связанных данных: {e}')

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

@router.get('/children-count/{config}/{id}')
async def children_count(config: str, id: int, request: Request):
  """Число дочерних (1_to_m) и потомков дерева — для попапа подтверждения удаления."""
  form = await read_config(
    request=request, config=config, id=id,
    script='delete_element', action='delete',
  )
  n = 0
  if not form.errors:
    try:
      from lib.svcmsmanager import ds_files
      n = await ds_files.children_count(form, id)
    except Exception:
      n = 0
  return {'success': 1, 'children_count': n, 'errors': form.errors}

@router.post('/multiconnect/{config}/{field_name}')
async def multiconnect(config:str,field_name:str,R:dict, request:Request):
  return await multiconnect_process(
    request=request,
    config=config,
    field_name=field_name,
    R=R
  )


router.include_router(wysiwyg_routes)
