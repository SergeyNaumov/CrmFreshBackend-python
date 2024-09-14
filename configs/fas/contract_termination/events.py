from lib.core import exists_arg

async def permissions(form):
  entity = exists_arg('cgi_params;entity',form.R)
  if entity=='5':
    form.title='Расторжения РегРФ'
  elif entity=='8':
    form.title='Расторжения НС "Ревизор"'
  elif entity=='14':
    form.title='Расторжения BzInfo'
  elif entity=='18':
    form.title='Расторжения ФАС-сервис'
  elif entity=='22':
    form.title='Расторжения AUZ'
  elif not(form.id):
    form.errors.append('Неузвестное значение entity')
  
  form.QUERY_SEARCH_TABLES=[
      {'t':'contract_termination','a':'wt'},
      {'t':'transfere_result','a':'tr', 'l':f'tr.parent_id = wt.id and tr.type={entity}','lj':1},
      {'t':'manager','a':'m','l':'tr.manager_id=m.id','lj':True},
      {'t':'user','a':'u','l':'tr.user_id=u.id','lj':True},
  ]
  login=form.manager['login']
  #  form.explain=1
  if login in ('akulov','pzm','sed','anna','admin') or \
    (entity in ('5','18') and login=='lgf') or \
    (entity in '8' and login in ('naumova','ahmetova')) or \
    (entity in ('14') and login in ('veronika')) or \
    (entity in ('22') and login in ('anna')):
        form.search_links.append({
          'link':f"/vue/admin_table/assignment?entity={entity}",
          'description':"Менеджеры для распределения",
          'target':'contract_termination_stat'
        })

# async def before_search(form):
#   entity = exists_arg('cgi_params;entity',form.R)
#   qs = form.query_search
#   if entity.isnumeric():
#     form.query_search['WHERE'].append(f"tr.type={entity}")

events={
  'permissions':permissions
}