from fastapi import APIRouter, File, UploadFile
from lib.all_configs import read_config
from .edit_form.one_to_m import process_one_to_m

router = APIRouter()


@router.get('/1_to_m/{config}/{field_name}/{id}')
def get_value_for_slide(config: str, field_name: str, id: int):

  return process_one_to_m(
      config=config,
      action='get_slide_data',
      field_name=field_name,
      id=id
    )

@router.post('/1_to_m/insert/{config}/{field_name}/{id}')
async def insert(config:str,field_name:str,id:int,R:dict):
  return process_one_to_m(
    config=config,
    field_name=field_name,
    id=id,
    R=R,
    action='insert'
  )

# INSERT to 1_to_m
@router.post('/1_to_m/update/{config}/{field_name}/{id}/{one_to_m_id}')
async def insert(config:str,field_name:str,id:int,one_to_m_id:int,R:dict):
  return process_one_to_m(
    config=config,
    field_name=field_name,
    id=id,
    one_to_m_id=one_to_m_id,
    R=R,
    action='update'
  )

# UPDATE field
@router.post('/1_to_m/update_field/{config}/{field_name}/{child_field_name}/{id}')
async def update_field(config:str,field_name:str,child_field_name:str,id:int,R:dict):
  #print('UPDATE_FIELD')
  one_to_m_id=R['cur_id']
  return process_one_to_m(
    config=config,
    field_name=field_name,
    child_field_name=child_field_name,
    id=id,
    one_to_m_id=one_to_m_id,
    R=R,
    action='update_field'
  )

# sort in slide 1_to_m
@router.post('/1_to_m/sort/{config}/{field_name}/{id}')
async def sort_slide(config:str,field_name:str,id:int,R:dict):
  return process_one_to_m(
    config=config,
    field_name=field_name,
    id=id,
    R=R,
    action='sort'
  )

# delete record
@router.get('/1_to_m/delete/{config}/{field_name}/{id}/{one_to_m_id}')
async def delete_record(config:str,field_name:str,id:int,one_to_m_id:int):
  #print('DELETE!')
  return process_one_to_m(
    config=config,
    field_name=field_name,
    id=id,
    R={},
    one_to_m_id=one_to_m_id,
    action='delete'
  )

# Upload file
@router.post('/1_to_m/upload_file/{config}/{field_name}/{child_field_name}/{id}/{one_to_m_id}')
async def route_upload_file(
    config:str,
    field_name:str,
    child_field_name:str,
    id:int,
    one_to_m_id:int,
    attach: UploadFile = File(...)
):
  
  return process_one_to_m(
    config=config,
    field_name=field_name,
    child_field_name=child_field_name,
    id=id,
    action='upload_file',
    one_to_m_id=one_to_m_id,
    attach=attach
  )

# Upload file (multiload)
@router.post('/1_to_m/upload_file/{config}/{field_name}/{child_field_name}/{id}')
async def route_upload_file(
    config:str,
    field_name:str,
    child_field_name:str,
    id:int,
    
    attach: UploadFile = File(...)
):
  
  return process_one_to_m(
    config=config,
    field_name=field_name,
    child_field_name=child_field_name,
    id=id,
    action='upload_file',
    one_to_m_id=0,
    attach=attach
  )



@router.get('/1_to_m/download/{config}/{field_name}/{child_field_name}/{id}/{one_to_m_id}/{filename}')
async def download(
      config:str,
    field_name:str,
    child_field_name:str,
    id:int,
    one_to_m_id:int,
    filename:str,
    view:int
):
  # вывести картинку на stdout!
  return {
    'filename':filename,
    'view':view
  }

  #return {'success':'delete'}


  #orig_filename=attach.filename
  #print(f'orig_filename: {orig_filename}')
  
  

  #with open("ZZZ.png", "wb") as buffer:
  #    shutil.copyfileobj(attach.file, buffer)
 # return {'success':1}