def permissions(form):
    #form.s.project_id=0
    if hasattr(form.s,'project_id') and form.s.project_id:
      icon_fld=form.get_field('icon')
      icon_fld['filedir']=icon_fld['filedir'].replace('[project_id]',str(form.s.project_id) )

      #form.pre(icon_fld)

events={
  'permissions':permissions,
}