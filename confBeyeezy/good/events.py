def permissions(form):
	perm=form.manager['permissions']
	if perm.get('admin'):
		form.make_delete=True

events={

	'permissions':permissions
}