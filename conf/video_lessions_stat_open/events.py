from lib.CRM.plugins.search.xlsx import go as init_search_plugin

def permissions(form):
  init_search_plugin(form)
  
events={
  'permissions':[
      permissions
  ],
}