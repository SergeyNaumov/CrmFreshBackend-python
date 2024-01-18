from lib.core import exists_arg

def permission(form):
    perm=form.manager['permissions']
    for f in form.fields:
        f['filter_on']=True
    entity = exists_arg('cgi_params;entity',form.R)
    if entity=='7':
        form.title='Реестр РНП РегРФ'
    elif entity=='10':
        form.title='Реестр РНП "Ревизор"'

    elif not(form.id):
        form.errors.append('Неузвестное значение entity')

    login=form.manager['login']

    if login in ('akulov','pzm','sed','anna','admin') or \
    (entity=='7' and login=='lgf') or \
    (entity=='10' and login=='sheglova'):
        form.search_links.append({
          'link':f"/vue/admin_table/assignment?entity={entity}",
          'description':"Менеджеры для распределения",
          'target':f'{form.config}_stat'
        })
    #if form.manager['login']!='admin':
    #    form.errors.append('Доступ запрещён')

def events_permission2(form):
    pass

def events_before_code(form):
    #print('is_before_code')
    pass

def before_delete(form):
    pass
    #form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
      permission,
      
  ],
  'before_delete':before_delete,
  'before_code':events_before_code
}