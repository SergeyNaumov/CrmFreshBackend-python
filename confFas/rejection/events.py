from lib.core import exists_arg

def permissions(form):
  entity = exists_arg('cgi_params;entity',form.R)
  if entity=='6':
    form.title='Уклонения РегРФ'
  elif entity=='9':
    form.title='Уклонения НС "Ревизор"'
  elif not(form.id):
    form.errors.append('Неузвестное значение entity')
  form.QUERY_SEARCH_TABLES=[ # перенёс в permissions
      {'t':'rejection','a':'wt'},
      
      {'t':'transfere_result','a':'tr', 'l':f'tr.parent_id = wt.id and tr.type={entity}','lj':1},
      {'t':'manager','a':'m','l':'tr.manager_id=m.id','lj':True},

      
  ]
  
  #if form.manager['login']=='admin':
  #  form.explain=1
  login=form.manager['login']
  if login in ('akulov','pzm','sed','anna','admin') \
    or (entity=='6' and login=='lgf') or \
    (entity=='9' and login=='sheglova'):
        form.search_links.append({
          'link':f"/vue/admin_table/assignment?entity={entity}",
          'description':"Менеджеры для распределения",
          'target':'contract_termination_stat'
        })

def before_search(form):
  entity = exists_arg('cgi_params;entity',form.R)
  qs = form.query_search
  if entity>0:
    form.query_search['WHERE'].append(f"tr.type={entity}")
    



events={
  'permissions':permissions,
  'before_search':before_search
}