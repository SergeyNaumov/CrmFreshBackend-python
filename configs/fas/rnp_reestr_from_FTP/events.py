from lib.core import exists_arg

def permission(form):
    perm=form.manager['permissions']
    #form.explain=1
    for f in form.fields:
        f['filter_on']=True
    entity = exists_arg('cgi_params;entity',form.R)
    if entity=='7':
        form.title='Реестр РНП РегРФ'
    elif entity=='10':
        form.title='Реестр РНП "Ревизор"'
    elif entity=='16':
        form.title='Реестр РНП BzInfo'
    elif entity=='19':
        form.title='Реестр РНП ФАС-сервис'
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

    form.QUERY_SEARCH_TABLES=[ # перенёс в permissions
        {'t':'rnp_reestr_from_FTP','a':'wt'},
        {'t':'manager','a':'m','l':'wt.manager_id=m.id','lj':1},
        {'t':'user','a':'u','l':'wt.user_id=u.id','lj':1},
        {'t':'manager','a':'m_otk','l':'wt.manager_otk=m_otk.id','lj':1,'for_fields':['manager_otk']},
        {'t':'manager','a':'m_dt2','l':'wt.manager_dt2=m_dt2.id','lj':1,'for_fields':['manager_dt2']},
        {'t':'user','a':'u_otk','l':'wt.manager_otk_users_id=u_otk.id','lj':1,'for_fields':['manager_otk_is_double']},
        {'t':'user','a':'u_dt2','l':'wt.manager_dt2_users_id=u_dt2.id','lj':1,'for_fields':['manager_dt2_is_double']},
        {'t':'transfere_result','a':'tr', 'l':f'tr.parent_id = wt.id and tr.type={entity}','lj':1},
        #{'t':'manager','a':'m','l':'tr.manager_id=m.id','lj':True},
    ]
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
def before_search(form):
  entity = exists_arg('cgi_params;entity',form.R)
  qs = form.query_search
  if entity.isnumeric():
    form.query_search['WHERE'].append(f"tr.type={entity}")

events={
  'permissions':[
      permission,
      
  ],
  'before_search':before_search,
  'before_delete':before_delete,
  'before_code':events_before_code
}