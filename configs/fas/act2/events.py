from .get_values import get_values

async def permissions(form):
  if form.id:
    form.ov=await get_values(form)
    #form.pre(form.ov)
    #print('ov:',form.ov)
    #form.title=f"Акт №{form.ov['number']} от {form.ov['registered']}"

async def after_save(form):
    pass
    # form.nv=get_values(form)
    # #print('nv:',form.nv)

events={
  'permissions':[ permissions
  ],
  'after_save':after_save
  #'before_delete':before_delete,
  #'before_code':events_before_code
}