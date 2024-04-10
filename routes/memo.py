from fastapi import APIRouter #, File, UploadFile, Form, Depends
from lib.all_configs import read_config
import datetime as dt
from lib.core import date_to_rus

router = APIRouter()


@router.get('/get/{config}/{field_name}/{id}')
async def get_memo(config:str, field_name:str,id:int): # 
  form=read_config(
    action='get',
    config=config,
    id=id,
    #R=R,
    script='memo'
  )
  #print('form:',form)
  field=form.get_field(field_name)
  errors=form.errors
  response={'success':False,'errors':errors}

  if not(field):
    errors.append(f"Поле {field_name} не найдено")

  
  if not len(errors):

    data=form.db.query(
      query=f"""
        SELECT
          memo.{field['memo_table_id']} id, user.{field['auth_id_field']} user_id,
          user.{field['auth_name_field']} user_name, memo.{field['memo_table_comment']} message, memo.{field['memo_table_registered']} date
        FROM
          {field['memo_table']} memo
          LEFT JOIN {field['auth_table']} user ON (memo.{field['memo_table_auth_id']} = user.{field['auth_id_field']} )
        WHERE
          memo.{field['memo_table_foreign_key']}=%s ORDER BY memo.{field['memo_table_registered']} desc

      """,
      log=form.log,
      values=[form.id],
      errors=form.errors
    )


    if 'before_out_tags' in field:
      field['before_out_tags'](form,data)

    for d in data:
      d['date']=date_to_rus(d['date'])

    response={
      'success':True,
      'field':{
        'description':field['description'],
        'type':field['type'],
        'name':field['name']
      },
      'errors':form.errors,
      'log':form.log,
      'data':data
    }

  return response


@router.post('/add/{config}/{field_name}/{id}')
async def get_memo(config:str, field_name:str,id:int, R:dict): 
  form=read_config(
    action='add',
    config=config,
    id=id,
    #R=R,
    script='memo'
  )
  field=form.get_field(field_name)
  errors=form.errors
  if not(field):
    errors.append(f"Поле {field_name} не найдено")
  
  if form.read_only or ('read_only' in field and field['read_only']):
    errors.append('вы не можете добавлять записи в это поле')

  memo_id=None
  if not len(errors) and 'message' in R and R['message']:
    data={
        field['memo_table_foreign_key']:form.id,
        field['memo_table_registered']:'func:now()',
        field['memo_table_auth_id']:form.manager['id'],
        field['memo_table_comment']:R['message']
    }
    memo_id=form.db.save(
      table=field['memo_table'],
      data=data
    )
    data['id']=memo_id

    form.run_event('after_add',{'field':field,'data':data})

  success=1
  if len(form.errors): success=0

  data={
    'id':memo_id,
    'date': dt.datetime.now(),
    'user_id':form.manager.get('id'),
    'user_name':form.manager.get('name'),
    'message':data.get(field['memo_table_comment'],'')
  }

  tags=[data]
  if 'before_out_tags' in field:
    field['before_out_tags'](form, tags)

  for t in tags:
    t['date']=date_to_rus(t['date'])

  return {
    'user_id': form.manager['id'], # legacy
    'user_name': form.manager['name'], # legacy
    'now':dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # legacy
    'errors':errors,
    'success':success,
    'memo_id':memo_id, # legacy
    'data':data # new format

  }
# Обновление записи
@router.post('/update/{config}/{field_name}/{id}/{memo_id}')
async def update_memo(config:str, field_name:str,id:int, memo_id:int, R:dict):
  form=read_config(
    config=config,
    id=id,
    #R=R,
    script='memo',
    action='update'
  )
  field=form.get_field(field_name)
  errors=form.errors
  if not(field):
    errors.append(f"Поле {field_name} не найдено")
  
  if form.read_only or ('read_only' in field and field['read_only']):
    errors.append('вы не можете изменить эту запись')

  if not len(errors) and 'message' in R and R['message']:
    form.db.query(
      query=f"""
        UPDATE
          {field['memo_table']}
        SET
          {field['memo_table_comment']}=%s,
          {field['memo_table_registered']}=now(),
          {field['memo_table_auth_id']}=%s

        WHERE {field['memo_table_id']}=%s and {field['memo_table_foreign_key']}=%s
      """,
      errors=errors,
      log=form.log,
      values=[R['message'], form.manager['id'], memo_id, form.id]
    )


  success=1
  if len(form.errors): success=0
  return {
    'user_id': form.manager['id'],
    'user_name': form.manager['name'],
    'now':dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'errors':errors,
    'log':form.log,
    'success':success,
  }

@router.get('/delete/{config}/{field_name}/{id}/{memo_id}')
async def delete_from_memo(config:str, field_name:str,id:int, memo_id:int):
  form=read_config(
    action='delete',
    config=config,
    id=id,
    #R=R,
    script='memo'
  )
  field=form.get_field(field_name)
  errors=form.errors
  
  if form.read_only or ('read_only' in field and field['read_only']):
    errors.append('вы не можете удалить эту запись')

  if not len(errors):
    form.db.query(
      query=f"""
        DELETE FROM {field['memo_table']} WHERE {field['memo_table_id']}=%s and {field['memo_table_foreign_key']}=%s
      """,
      errors=errors,
      log=form.log,
      values=[memo_id,form.id]
    )

  return{
    'success':not(len(errors)>0),
    'errors':errors
  }

#@router.post('/get_many_memo/{config}')