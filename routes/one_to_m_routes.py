from fastapi import APIRouter, File, UploadFile, Request
from lib.all_configs import read_config
from .edit_form.one_to_m import process_one_to_m

router = APIRouter()


@router.get('/1_to_m/{config}/{field_name}/{id}')
async def get_value_for_slide(config: str, field_name: str, id: int, request: Request):

  return await process_one_to_m(
      request=request,
      config=config,
      action='get_slide_data',
      field_name=field_name,
      id=id
    )

@router.post('/1_to_m/insert/{config}/{field_name}/{id}')
async def insert(config:str,field_name:str,id:int,R:dict,request:Request):
  return await process_one_to_m(
    request=request,
    config=config,
    field_name=field_name,
    id=id,
    R=R,
    action='insert'
  )

# INSERT to 1_to_m
@router.post('/1_to_m/update/{config}/{field_name}/{id}/{one_to_m_id}')
async def insert(config:str,field_name:str,id:int,one_to_m_id:int,R:dict,request:Request):
  return await process_one_to_m(
    request=request,
    config=config,
    field_name=field_name,
    id=id,
    one_to_m_id=one_to_m_id,
    R=R,
    action='update'
  )

# UPDATE field
@router.post('/1_to_m/update_field/{config}/{field_name}/{child_field_name}/{id}')
async def update_field(config:str,field_name:str,child_field_name:str,id:int,R:dict,request:Request):
  #print('UPDATE_FIELD')
  one_to_m_id=R['cur_id']
  return await process_one_to_m(
    request=request,
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
async def sort_slide(config:str,field_name:str,id:int,R:dict,request:Request):
  return await process_one_to_m(
    request=request,
    config=config,
    field_name=field_name,
    id=id,
    R=R,
    action='sort'
  )

# delete record
@router.get('/1_to_m/delete/{config}/{field_name}/{id}/{one_to_m_id}')
async def delete_record(config:str,field_name:str,id:int,one_to_m_id:int,request:Request):
  #print('DELETE!')
  return await process_one_to_m(
    request=request,
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
    request:Request,
    config:str,
    field_name:str,
    child_field_name:str,
    id:int,
    one_to_m_id:int,
    attach: UploadFile = File(...),
):
  
  return await process_one_to_m(
    request=request,
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
    request:Request,
    config:str,
    field_name:str,
    child_field_name:str,
    id:int,
    attach: UploadFile = File(...),

):
  
  return await process_one_to_m(
    request=request,
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
    view:int,
    request:Request
):
  # вывести картинку на stdout!
  return {
    'filename':filename,
    'view':view
  }
@router.get('/1_to_m/delete_file/{config}/{field_name}/{child_field_name}/{id}/{one_to_m_id}')
async def delete_file(config: str, field_name:str, child_field_name:str, id:int, one_to_m_id:int,request:Request):
  return await process_one_to_m(
    request=request,
    config=config,
    field_name=field_name,
    child_field_name=child_field_name,
    id=id,
    action='delete_file',
    one_to_m_id=one_to_m_id,
  )
  #return {'success':'delete'}


  #orig_filename=attach.filename
  #print(f'orig_filename: {orig_filename}')
  
  

  #with open("ZZZ.png", "wb") as buffer:
  #    shutil.copyfileobj(attach.file, buffer)
 # return {'success':1}


# Пересчёт итоговой суммы родителя из 1_to_m-таблицы.
# Конфиг задаёт: total_sum_from (имя 1_to_m-поля), total_sum_field (колонка
# родителя), total_sum_expr (SQL-выражение, напр. 'price*cnt').
@router.post('/recalc_total/{config}/{id}')
async def recalc_total(config: str, id: int, request: Request):
  form = await read_config(
    request=request,
    config=config,
    id=id,
    script='recalc_total',
    action='edit',
  )
  if not form.success():
    return {'success': 0, 'errors': form.errors}

  # Защита: запись должна принадлежать текущему проекту.
  if getattr(form, 'foreign_key', '') and getattr(form, 'foreign_key_value', ''):
    cnt = await form.db.query(
      query=f'SELECT COUNT(*) FROM {form.work_table} '
            f'WHERE {form.work_table_id}=%s AND {form.foreign_key}=%s',
      values=[form.id, form.foreign_key_value], onevalue=1, errors=form.errors,
    )
    if not cnt:
      return {'success': 0, 'errors': ['Запись принадлежит другому проекту']}

  from_field = getattr(form, 'total_sum_from', '')
  sum_field = getattr(form, 'total_sum_field', '')
  expr = getattr(form, 'total_sum_expr', '') or '1'
  if not (from_field and sum_field):
    return {'success': 0, 'errors': ['конфиг не поддерживает пересчёт суммы']}

  f = form.get_field(from_field)
  if not f:
    return {'success': 0, 'errors': [f'не найдено поле {from_field}']}

  total = await form.db.query(
    query=f'SELECT COALESCE(SUM({expr}),0) FROM {f["table"]} WHERE {f["foreign_key"]}=%s',
    values=[form.id], onevalue=1, errors=form.errors,
  )
  total = int(total or 0)
  await form.db.query(
    query=f'UPDATE {form.work_table} SET {sum_field}=%s WHERE {form.work_table_id}=%s',
    values=[total, form.id], errors=form.errors,
  )
  return {'success': form.success(), 'errors': form.errors, 'total_sum': total}