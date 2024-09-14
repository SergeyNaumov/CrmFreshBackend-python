from lib.core import exists_arg

async def permissions(form):
  #form.explain=1
  entity = exists_arg('cgi_params;entity',form.R)
  if entity=='6':
    form.title='Уклонения РегРФ'
  elif entity=='9':
    form.title='Уклонения НС "Ревизор"'
  elif entity=='15':
    form.title='Уклонения BzInfo'
  elif entity=='17':
    form.title='Уклонения Фас-сервис'
  elif entity=='21':
    form.title='Уклонения AUZ'
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


  if login in ('akulov','pzm','sed','anna','admin') or \
  (entity in ('6','17') and login in('lgf') ) or \
  (entity in ('9') and login in ('naumova','ahmetova')) or \
  (entity in ('15') and login in ('veronika')) or \
  (entity in ('21') and login in ('anna')):
        form.search_links.append({
          'link':f"/vue/admin_table/assignment?entity={entity}",
          'description':"Менеджеры для распределения",
          'target':'contract_termination_stat'
        })

async def before_search(form):
  entity = exists_arg('cgi_params;entity',form.R)
  qs = form.query_search
  if entity.isnumeric():
    form.query_search['WHERE'].append(f"tr.type={entity}")
    



events={
  'permissions':permissions,
  'before_search':before_search
}