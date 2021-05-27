from lib.engine import s
from lib.core import exists_arg
from lib.form_control import check_rules, is_email, is_phone

def change_apteka_order(R):
  errors=[]
  success=1
  rules=[
     [ (exists_arg('apteka_id',R) and str(R['apteka_id']).isdigit()) ,'Не указан comp_id. обратитесь к разработчику'],
     [ (R['phone']),'Телефон не указан'],
     [ is_phone(R['phone']),'Телефон указан не корректно' ],
     [ (R['email']),'Email не указан'],
     [ is_email(R['email']),'Email указан не корректно, укажите валидный email' ],
     [ (R['header']),'Заполните наименование компании'],
     [ (  not(R['inn']) or len(R['inn'])==10 or len(R['inn'])==12 ),'ИНН должен быть 10 или 12 цифр'],
     
     
  ]
  check_rules(rules,errors)

  if not len(errors):
      R['manager_id']=s.manager['id']
      s.db.save(
          table="change_apteka_order",
          data=R,
          errors=errors
      )
  
  

  if len(errors):
      success=0

  return {'success':success,'errors':errors}