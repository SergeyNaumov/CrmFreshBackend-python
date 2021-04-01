from lib.core import cur_year,cur_date, exists_arg
from fastapi import FastAPI, APIRouter
from lib.engine import s

#import re
from lib.send_mes import send_mes
from lib.all_configs import read_config


#valid_email=re.compile(r"^[a-zA-Z0-9\-_\.]+@[a-zA-Z0-9\-_\.]+\.[a-zA-Z0-9\-_\.]+$")
#valid_phone=re.compile(r"")
router = APIRouter()

# изменение пароля
@router.post('/password/{config}/{field_name}/{id}')
async def password(config:str,field_name:str,id:int,R: dict):
  errors=[]
  response={'success':1}

  if R['action'] == 'change':
      form=read_config(
        script='password', config=config,
        action=R['action'], R=R, id=id
      )

      field=form.get_field(field_name)
      if not field:
        errors.append(f'Не найдено поле {field_name}')

      if form.read_only or exists_arg('read_only',field):
        errors.append(f'Нет прав на изменение пароля')
      
      if not(R['new_password']):
        errors.append(f'В запросе не указан новый пароль. обратитесь к разработчику')

      if not len(errors):
        if form.s.config['encrypt_method'] == 'mysql_sha2':
          form.db.query(
            query=f'UPDATE {form.work_table} SET {field_name}=sha2(%s,256) where id=%s',
            values=[R['new_password'],form.id]
          )
        else:
          errors.append('encrypt_method не указан или указан неизвестный метод. обратитесь к разработчику')
      
      if len(errors):
        response['success']=0
        response['errors']=errors




  return  response
        

      
    
  