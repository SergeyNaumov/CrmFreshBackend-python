from lib.core import exists_arg 
def set_default_attributes(form):
  pass
  # Может быть оно конечно и нужно, но не для memo точно, поэтому пока закомментировал:
  
  if not form.read_only:
    for field in form.fields:

      if ('make_delete' not in field) and ( not exists_arg('read_only',field) ):
        field['make_delete']=1
  