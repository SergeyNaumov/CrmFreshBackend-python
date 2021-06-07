import re
# Пример использования
#    rules=[
#       [ (R['phone']),'Телефон не указан'],
#       [ (re.match(r'^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$',R['phone'])),'Телефон указан не корректно' ],
#       [ (R['login']),'Логин не указан'],
#       [ (re.match(r'^[a-zA-Z0-9\-_\.]+@[a-zA-Z0-9\-_\.]+\.[a-zA-Z0-9\-_\.]+$',R['login'])),'Email указан не корректно' ],
#       [ not exist_login(R), 'Такой Emal уже существует в нашей системе. Пожалуйста укажите другой, или воспользуетесь <a href="/remember">формой восстановления пароля</a>']
#    ]

def check_rules(rules,errors):
  
  for (reg_res,message) in rules:
    if not reg_res:
      errors.append(message)
      break
  return errors

def is_email(email):
  if email:
    return re.match(r'^[a-zA-Z0-9\-_\.]+@[a-zA-Z0-9\-_]+\.[a-zA-Z0-8\-_\.]+$',email)
  else:
    return False


def is_phone(phone):
   return re.match(r'^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$',phone)
