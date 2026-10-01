async def permissions(form):
    form.root_directory='./'

form={
  #'root_directory':'./',
  'events':{
    'permissions':permissions
  }
}