def permissions(form):
	perm=form.manager.get('permissions')
	if not( ('admin' in perm) or (form.manager['login']=='admin') ):
		form.errors.append('доступ запрещён')

events={
	'permissions':permissions
}