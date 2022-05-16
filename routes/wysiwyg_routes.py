from fastapi import APIRouter, File, UploadFile, Form, Depends
from lib.all_configs import read_config
from .edit_form.wysiwyg_process import wysiwyg_process


router = APIRouter()



# Загрузка файла в wysiwyg
@router.post('/wysiwyg/{config}/{field_name}/{id}/upload')
async def wysiwyg_upload(
  config:str,
  field_name:str,
  id:int,
  path: str=Form(...),
  file: UploadFile = File(...)
): # 

  #print('path:',path)
  return wysiwyg_process(
    action='upload',
    path=path,
    file=file,
    config=config,
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
  return wysiwyg_process(
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
  return wysiwyg_process(
    config=config,
    field_name=field_name,
    script='wysiwyg',
    R=R
  )

@router.post('/wysiwyg/{config}/{field_name}/{id}')
async def wysiwyg2(config:str,field_name:str,id:int,R:dict):
  return wysiwyg_process(
    config=config,
    field_name=field_name,
    id=id,
    R=R,
    script='wysiwyg'
  )
