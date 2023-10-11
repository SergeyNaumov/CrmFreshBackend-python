from lib.core import exists_arg

def permissions(form):
  entity = exists_arg('cgi_params;entity',form.R)
  if entity=='6':
    form.title='Уклонения РегРФ'
  else:
    form.errors.append('Неузвестное значение entity')
  
  if form.manager['login'] in ('akulov','anna','admin'):
        form.search_links.append({
          'link':"/vue/admin_table/assignment6",
          'description':"Менеджеры для распределения",
          'target':'contract_termination_stat'
        })

def before_search(form):
  entity = exists_arg('cgi_params;entity',form.R)
  qs = form.query_search
  if entity in ('6',):
    form.query_search['WHERE'].append(f"tr.type={entity}")
    



events={
  'permissions':permissions,
  'before_search':before_search
}