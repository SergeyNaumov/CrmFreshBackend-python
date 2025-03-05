from lib.send_mes import send_mes
from lib.core import gen_pas

def events_permissions(form):
    if not ( str(form.manager['type']) == "1" ):
      form.errors.append('доступ запрещён!')


def after_save(form):
  form.log.append(form.values)  
  ov=form.values
  nv=form.new_values
  
  

  #print(ov)
  #print(nv)



  #if !ov['accepted'] and nv['accepted']==1:
  #  print('Включили галку!')

#def events_before_code(form):
    

def before_delete(form):
    print('before_detele STARTED!')
    #form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
      events_permissions
    
  ],
  'after_save':after_save,
  'before_delete':before_delete,
#  'before_code':events_before_code
}