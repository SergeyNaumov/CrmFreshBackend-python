def permissions(form):
    #form.s.project_id=0
    if hasattr(form.s,'project_id') and form.s.project_id:
      proto_fld=form.get_field('photo')
      proto_fld['filedir']=proto_fld['filedir'].replace('[project_id]',str(form.s.project_id) )


      #form.pre(icon_fld)

events={
  'permissions':permissions,
}