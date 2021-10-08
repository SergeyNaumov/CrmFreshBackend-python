from fastapi import APIRouter, File, UploadFile, Form, Depends
from lib.all_configs import read_config
from .edit_form.wysiwyg_process import wysiwyg_process


router = APIRouter()


# , file: bytes = File(...), fileb: UploadFile = File(...)
#, 
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
  #with open(file.filename, "wb") as buffer:
  #        shutil.copyfileobj(file.file, buffer)

  # return {
  #   'manager':form.manager,
  #   'path':path,
  #   'filename':file.filename
  # }
  #return {"file_size": len(file)}

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
