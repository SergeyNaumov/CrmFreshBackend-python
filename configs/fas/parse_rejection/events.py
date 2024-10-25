from lib.core import exists_arg

async def permissions(form):
  ...




async def before_search(form):
  entity = exists_arg('cgi_params;entity',form.R)
  qs = form.query_search

    



events={
  'permissions':permissions,
  'before_search':before_search
}