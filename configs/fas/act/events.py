from .get_values import get_values

async def permissions(form):
    form.ov=None
    form.is_admin=True

    perm=form.manager['permissions']
    #form.pre(perm)
    #form.explain=1
    if perm['admin_paids']:
        form.is_admin=True
        form.read_only=False
        form.make_delete=True
    
    if form.id:
        form.ov=await get_values(form)

        if form.ov:
            form.title=f"Акт №{form.ov['number']} от {form.ov['registered']}"

async def after_save(form):
    form.nv=await get_values(form)
    #print('nv:',form.nv)

events={
  'permissions':[
      permissions,
      
  ],
  'after_save':after_save
  #'before_delete':before_delete,
  #'before_code':events_before_code
}