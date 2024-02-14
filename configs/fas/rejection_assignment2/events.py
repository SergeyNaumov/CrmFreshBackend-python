def permissions(form):
  if form.manager['login'] in ('akulov','anna','admin'):
        form.read_only=False
        form.make_delete=True


events={
  'permissions':permissions
}