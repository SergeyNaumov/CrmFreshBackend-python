from lib.core import exists_arg

def permissions(form):
  entity = exists_arg('cgi_params;entity',form.R)
  if entity=='5':
    form.title='Расторжения РегРФ'
  else:
    form.errors.append('Неузвестное значение entity')
  #pass
  if form.manager['login'] in ('akulov','anna','admin'):
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