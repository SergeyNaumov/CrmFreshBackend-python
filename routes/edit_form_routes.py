from fastapi import APIRouter
#from lib.core import cur_year,cur_date,  exists_arg

from .edit_form.process_edit_form import process_edit_form
router = APIRouter()

# Форма редактирования
@router.get('/edit-form/{config}/{id}')
async def edit_form(config,id):
  return {'config':config,'id':id}

# форма добавления элемента
@router.get('/edit-form/{config}')
async def insert_form(config):
  return  {'config':config}

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
  if 'action' in R: action=R['action']
  #if 'values' in R: values=R['values']
  return process_edit_form(
    action=action,
    config=config,
    id=id,
    R=R
  )

@router.post('/wysiwyg/{config}/{field_name}')
async def wysiwyg1(config:str,field_name:str,R:dict):
  wysiwyg_process(
    config=config,
    field_name=field_name,
    id=id,
    script='wysiwyg'
  )

@router.post('/wysiwyg/{config}/{field_name}/{id}/{script}')
async def wysiwyg1(config:str,field_name:str,id:int,script:int):
  wysiwyg_process(
    config=config,
    field_name=field_name,
    id=id,
    script='wysiwyg'
  )

