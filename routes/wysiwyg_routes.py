from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import HTMLResponse

from lib.all_configs import read_config
from .edit_form.wysiwyg_process import wysiwyg_process
from config import config as system_config

router = APIRouter()



# Загрузка файла в wysiwyg
@router.post('/wysiwyg/{config}/{field_name}/{_id}/upload')
async def wysiwyg_upload(
  config:str,
  field_name:str,
  _id:int,
  path: str=Form(...),
  file: UploadFile = File(...)
): # 


  return await wysiwyg_process(
    action='upload',
    path=path,
    file=file,
    config=config,
    id=_id,
    field_name=field_name,
    script='wysiwyg',
    R={}
  )

# Загрузка файла в wysiwyg: пришлось сделать дубль при заливке в визивиг фото, когда запись ещё не создана (нет id)
@router.post('/wysiwyg/{config}/{field_name}/upload')
async def wysiwyg_upload(
  config:str,
  field_name:str,
  path: str=Form(...),
  file: UploadFile = File(...)
): # 

  #print('path:',path)
  return await wysiwyg_process(
    action='upload',
    path=path,
    file=file,
    config=config,
    field_name=field_name,
    script='wysiwyg',
    R={}
  )

@router.post('/wysiwyg/{config}/{field_name}')
async def wysiwyg1(config:str,field_name:str,R:dict):
  return await wysiwyg_process(
    config=config,
    field_name=field_name,
    script='wysiwyg',
    R=R
  )

@router.post('/wysiwyg/{config}/{field_name}/{id}')
async def wysiwyg2(config:str,field_name:str,id:int,R:dict):
  return await wysiwyg_process(
    config=config,
    field_name=field_name,
    id=id,
    R=R,
    script='wysiwyg'
  )

# опции инициализации
@router.get('/wysiwyg/{config}/{field}/init_options')
async def wysiwyg_init_options(config:str,field:str):
  form = await read_config(
    script='wysiwyg', config=config,
    R={},
  )
  
  response={
    #'project_id':form.s.project_id,
    'success':True,
  }

  if ('wysiwyg' in system_config) and system_config['wysiwyg']:
    response['step1']=True
    ww=system_config['wysiwyg']
    #print('ww:',ww)
    if 'options_modify' in ww:
      response['step2']=True
      response['options']=ww['options_modify'](form,field)
    
    if not(response['options']) and 'options' in ww:
      response['step3']=True
      response['options']=ww['get_options']()

  return response

# загрузка шаблона в wysiwyg
@router.get('/wysiwyg/load-template/{config}/{field}/{template_id}')
async def load_template(config:str,field:str,template_id:int):
  form = await read_config(
    script='wysiwyg', config=config,
    R={},
  )
  if ('wysiwyg' in system_config) and system_config['wysiwyg']:
    ww=system_config['wysiwyg']
    if 'out_template' in ww and ww['out_template']:
      return HTMLResponse(ww['out_template'](form,field,template_id))

  # Если не нашли как отдать шаблон
  return None
