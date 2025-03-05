from lib.send_mes import send_mes
from lib.core import gen_pas
from lib.anna.get_apt_list import get_apt_list_ids



def events_permissions(form):
    if not ( form.manager['type'] in [1,2] ): # доступ для менеджера АннА и для юрлица
      form.errors.append('доступ запрещён!')




def after_save(form,opt):
  form.log.append(form.values)  
  ov=form.values
  nv=form.new_values
  
  

  #print(ov)
  #print(nv)



  if int(ov['accepted'])==0 and int(nv['accepted'])==1:
    print('Включили галку!')

#def events_before_code(form):
    
def before_search(form):
  #form.pre(form.query_search)
  if form.manager['type']==2: # для юрлица разрешаем поиск только по своим аптекам
    apt_list=get_apt_list_ids(form, form.manager['id'])
    form.query_search['WHERE'].append("wt.apteka_id IN ("+','.join(apt_list)+')')
    #form.explain=1
    #form.pre(apt_list)

def before_delete(form,opt):
    print('before_detele STARTED!')
    #form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
      events_permissions
    
  ],
  'after_save':after_save,
  'before_search':before_search,
  'before_delete':before_delete,
#  'before_code':events_before_code
}