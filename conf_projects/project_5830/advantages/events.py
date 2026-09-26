async def permissions(form):
  ...
    #project_id=form.request.state.project['project_id']
    #if project_id:
    #  icon_fld=form.get_field('icon')
    #  icon_fld['filedir']=icon_fld['filedir'].replace('[project_id]',str(project_id) )

      #form.pre(icon_fld)

events={
  'permissions':permissions,
}
