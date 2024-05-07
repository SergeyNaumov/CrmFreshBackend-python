#from .get_values import get_values

async def permissions(form):
    pass

async def after_save(form):
    pass
    # form.nv=get_values(form)
    # #print('nv:',form.nv)

events={
  'permissions':[
      permissions,
      
  ],
  'after_save':after_save

}