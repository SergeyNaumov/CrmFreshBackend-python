async def permissions(form):
    #form.s.project_id=0
    if getattr(form.request.state,'project',None):
      proto_fld=form.get_field('photo')
      proto_fld['filedir']=proto_fld['filedir'].replace('[project_id]',str(form.request.state.project['project_id']) )


      #form.pre(icon_fld)

events={
  'permissions':permissions,
}