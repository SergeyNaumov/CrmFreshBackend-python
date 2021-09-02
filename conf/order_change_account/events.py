#from lib.send_mes import send_mes
#from lib.core import gen_pas
from lib.anna.get_apt_list import get_apt_managers_ids
def events_permissions(form):
    #form.pre(form.manager['id'])
    if form.manager['type'] == 1: # менеджер АннА
      pass
    elif form.manager['type']==2: # представитель юр.лица
      #form.pre(form.script)
        
        
        # получаем id-шники менеджеров, которые привязаны к аптекам данного юрлица:
        managers_ids=get_apt_managers_ids(form,form.manager['id'])
        if not len(managers_ids):
          managers_ids=['0']



        form.manager['managers_ids']=[str(x) for x in managers_ids]
        
        if form.script == 'edit_form':
          if form.id:
            ov=form.db.query(
              query='select * from order_change_account where id=%s',
              values=[form.id],
              onerow=1
            )
            
          if ov and ov['manager_id'] not in managers_ids:
            form.errors.append('доступ запрещён!')
        


    else:
      form.errors.append('доступ запрещён!')

def before_search(form):
  
  #if not len(form.manager['managers_ids']): form.manager['managers_ids']=['0']
  #form.query_search.
  if form.manager['type']==2:
    form.query_search['WHERE'].append(
      f"wt.manager_id in ({ ','.join(form.manager['managers_ids']) },{form.manager['id']})"
    )
    #form.explain=1
  #form.pre({'manager':form.manager})
  #form.pre(form.query_search)
def after_save(form):
  #form.log.append(form.values)  
  ov=form.values
  nv=form.new_values
  
  



#def events_before_code(form):
    

def before_delete(form):
    pass
    #print('before_detele STARTED!')
    #form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
      events_permissions
  ],
  'before_search':before_search
#  'after_save':after_save,
#  'before_delete':before_delete,
#  'before_code':events_before_code
}