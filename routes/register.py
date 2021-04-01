from lib.core import cur_year,cur_date, gen_pas
from fastapi import FastAPI, APIRouter
from config import config
#from db import db,db_read,db_write
from lib.engine import s
from lib.session import *
#import re
from lib.send_mes import send_mes
from lib.form_control import check_rules, is_email, is_phone

#valid_email=re.compile(r"^[a-zA-Z0-9\-_\.]+@[a-zA-Z0-9\-_\.]+\.[a-zA-Z0-9\-_\.]+$")
#valid_phone=re.compile(r"")
router = APIRouter()
errors=[]
def exist_login(R):
  # Проверяем заявку
  exists=s.db.get(
    table='order_reg_company',
    where='login = %s',
    errors=errors,
    values=[R['login']],

    onerow=1
  )
  
  # если заявки нет, проверяем есть ли такой менеджер
  if not exists:
    exists=s.db.get(
      table='manager',
      where='login = %s',
      errors=errors,
      values=[R['login']],
      onerow=1
    )
  
  if exists: return True
  return False





# Регистрация
@router.post('/register')
async def register(R: dict):
  errors=[]
  response={'success':0,'errors':[]}
  #print('REGISTER!')
  if R:
    rules=[
       [ (R['phone']),'Телефон не указан'],
       [ is_phone(R['phone']),'Телефон указан не корректно' ],
       [ (R['login']),'Email не указан'],
       [ is_email(R['login']),'Email указан не корректно' ],
       [ not exist_login(R), 'Такой Emal уже существует в нашей системе. Пожалуйста укажите другой, или воспользуетесь <a href="/remember">формой восстановления пароля</a>']
    ]

    check_rules(rules,response['errors'])

    if(not len(response['errors'])): # все проверки пройдены, сохраняем
      response['reg_order_id']=s.db.save(
        table='order_reg_company',
        errors=response['errors'],
        data=R
      );
      if not len(response['errors']):
        response['success']=1
        

      
    
  else:
    response['errors'].append('ошибка в запросе!')

  send_mes(
    to=R['login'],
    subject='Ваша заявка на регистрацию была успешно отправлена',
    message=f"""
      Ваши регистрационные данные:<br>
      Наименование компании: {R['firm']}<br><br>
      
      <b>Контактное лицо:</b><br>
      Фамилия: {R['name_f']}<br>
      Имя: {R['name_i']}<br>
      Отчество: {R['name_o']}<br>
      Юридический адрес: {R['ur_address']}<br>
      ИНН: {R['inn']}<br>
      
      Телефон: {R['phone']}<br>
      Email: {R['login']}<br><br>
      

      После того, как наш менеджер проверит Вашу заявку на регистрацию и утвердит её, Вы получите дополнительное подтверждение
    """
  )

  return response
# Напоминание пароля
@router.post('/remember/get-access-code')
async def remember_get_code(R: dict):
  response={'success':1,'errors':[]}
  if R:
    manager=s.db.get(
      table='manager',
      where='login = %s',
      values=[R['login']],
      onerow=1
    )
    
    if(manager):
      remember_code=gen_pas(10,'012345678')
      s.db.save(
        table='remember_code',
        data={
          'id':manager['id'],
          'code':remember_code
        },
        replace=1,
      )

      # отправка на manager.email
      print('Send Mes: ', manager['email'],remember_code)
      send_mes(
        to=manager['email'],
        subject='Восстановление пароля в система AннА',
        message=f"""
          <p>
            Вы запросили изменение пароля в Системе АннА!<br>
            Ваш код доступа: {remember_code}
          </p>


          <div style="color: red;">
            Внимание! Если Вы не запрашивали изменение пароля, проигнорируйте данное сообщение
          </div>

          После того, как наш менеджер проверит Вашу заявку на регистрацию и утвердит её, Вы получите дополнительное подтверждение
        """
      )
    
  
  return response

# Проверка кода
@router.post('/remember/check-access-code')
async def remember_check_code(R: dict):
  response={'success':0,'errors':[]}
  if R:
    code_value=s.db.get(
      table='remember_code',
      where='code = %s',
      values=[R['remember_code']],
      onerow=1
    )
    
    if(code_value):
      response['success']=1
      response['id']=code_value['id']
    else:
      response['errors'].append('код не подошёл')

  return response

# Проверка кода
@router.post('/remember/change-password')
async def remember_check_code(R: dict):
  response={'success':0,'errors':[]}
  if R:
    code_value=s.db.get(
      table='remember_code',
      tables=[
        {'t':'manager','a':'m','l':'m.id=wt.id'}
      ],
      where='wt.code = %s and wt.id= %s',
      values=[R['remember_code'],R['id']],
    )

    if(code_value):
      s.db.query(
        query='UPDATE manager set password=sha2(%s,256) where id=%s',
        values=[R['password'],R['id']],
      )
      # s.db.query(
      #   query='DELETE FROM remember_code where id=%s',
      #   values=[R['id']],
      #   debug=1
      # )
      response['success']=1
      #response['errors'].append('проверочный код не подошёл или устарел')
    else:
      response['errors'].append('код не подошёл')

  return response


# @router.get('/logout')
# async def logout():
#   session_logout(s)
#   return {"success":1}
