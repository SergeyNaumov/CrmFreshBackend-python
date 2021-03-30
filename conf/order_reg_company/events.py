from lib.send_mes import send_mes
from lib.core import gen_pas

# def events_permissions(form):
#     if(form.action=='edit'):
#       form.get_values()
#       create_new_ur_lico(form.values,form)


# def create_new_ur_lico(values,form):
#     #form.log.append(form.values)  
#     # Проверяем, есть ли уже юрлицо с указанным ИНН
#     comp_id=0
#     comp=form.db.getrow(
#       table='comp',
#       where='inn = %s',
#       values=[values['inn']],
#       debug=1
#     )
    
#     if comp: # такое юрлицо уже существут, привязываем к нему нового менеджера
#       print('comp:',comp)
#       comp_id=comp['id']
#     else:
#       print(values)
#       # Создаём юрлицо
#       comp_id=form.db.save(
#         table='comp',
#         data={
#           'inn':values['inn'],
#           'header':values['firm'],
#           'ur_address':values['ur_address'],
#           'phone':values['phone'],
#           'email':values['login'],
#         }
#       )


#     # СОЗДАЁМ УЧЁТКУ
#     # проверяем, существует ли уже учётка с таким логином
#     manager=form.db.getrow(
#       table='manager',
#       where='login = %s',
#       values=[values['login']]
#     )

#     if manager:
#       form.errors.append('Не удалось создать новую учётную запись '+values['login']+', поскольку такая запись уже существует')
#     else:
#       password=gen_pas()
#       form.db.save(
#         table='manager',
#         data={
#           'login':values['login'],
#           'password':f'func::sha2("{password}",256)',
#           'email':values['login'],
#           'name':''
#         }
#       )
      
#       send_mes(
#         to=values['login'],
#         subject="Анна: ваша заявка на регистрацию Юридического лица одобрена",
#         message=f"""
#           Ваша заявка на регистрацию в системе "Анна" одобрена!<br><br>
#           Для Входа в систему используйте:<br>
#           Логин: { values['login'] }<br>
#           Пароль: { password }<br>
#           <a href="https://anna.crm-dev.ru/login">https://anna.crm-dev.ru/login</a>
#         """
#       )

#       form.log.append({'comp_id':comp_id})


def after_save(form,opt):
  form.log.append(form.values)  
  ov=form.values
  nv=form.new_values
  
  

  #print(ov)
  #print(nv)



  if int(ov['accepted'])==0 and int(nv['accepted'])==1:
    print('Включили галку!')

#def events_before_code(form):
    

def before_delete(form,opt):
    print('before_detele STARTED!')
    #form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
      #events_permissions
    
  ],
  'after_save':after_save,
  'before_delete':before_delete,
#  'before_code':events_before_code
}