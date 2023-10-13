from lib.core import exists_arg

def permissions(form):
  entity = exists_arg('cgi_params;entity',form.R)
  if entity=='5':
    form.title='Расторжения РегРФ'
  elif not(form.id):
    form.errors.append('Неузвестное значение entity')
  
  form.QUERY_SEARCH_TABLES=[
      {'t':'contract_termination','a':'wt'},
      {'t':'transfere_result','a':'tr', 'l':f'tr.parent_id = wt.id and tr.type={entity}','lj':1},
      {'t':'manager','a':'m','l':'tr.manager_id=m.id','lj':True},
      {'t':'user','a':'u','l':'tr.user_id=u.id','lj':True},
  ]
  #if form.manager['login']=='admin':
  #  form.explain=1
  if form.manager['login'] in ('akulov','pzm','sed','anna','admin'):
        form.search_links.append({
          'link':"/vue/admin_table/assignment5",
          'description':"Менеджеры для распределения",
          'target':'contract_termination_stat'
        })

def before_search(form):
  entity = exists_arg('cgi_params;entity',form.R)
  qs = form.query_search
  if entity in ('1','2','3','4','5','6',):
    form.query_search['WHERE'].append(f"tr.type={entity}")

events={
  'permissions':permissions
}