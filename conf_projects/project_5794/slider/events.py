async def permissions(form):
    #form.s.project_id=0
    if getattr(form.request.state,'project',None):

      for name in ('photo','photo_bg','photo_mob'):
        if proto_fld:=form.get_field(name):
          proto_fld['filedir']=proto_fld['filedir'].replace('[project_id]',str(form.request.state.project['project_id']) )

      #form.pre(icon_fld)

events={
  'permissions':permissions,
}