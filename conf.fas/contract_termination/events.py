def permissions(form):
  if form.manager['login'] in ('akulov','anna','admin'):
        form.search_links.append({
          'link':"./tools/contract_termination/report.pl",
          'description':"Статистика распределения",
          'target':'contract_termination_stat'
        })


events={
  'permissions':permissions
}