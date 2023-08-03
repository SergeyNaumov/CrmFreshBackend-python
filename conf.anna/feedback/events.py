from lib.CRM.plugins.search.xlsx import go as init_search_plugin

def permissions(form):
  init_search_plugin(form)
  if form.manager['type']!=1:
    form.errors.append('Доступ запрещён')

# def before_search(form):
#   qs=form.query_search
#   if not(len(qs['ORDER'])):
#     qs['ORDER'].append('wt.ts desc')
#   #form.explain=1
  

events={
  'permissions':[
      permissions
  ],
  #'before_search':before_search
}