async def events_permission(form):
    perm=form.manager['permissions']
    #form.pre()
    if perm['manager_group_edit']:
        form.read_only=0
        form.not_create=0
        form.make_delete=1


events={
  'permissions':events_permission,
  #'before_delete':before_delete,
  #'before_code':events_before_code
}