def permissions(form):
	manager=form.manager
	perm=manager.get('permissions')
	#form.pre(perm)
	form.snt_ids=[]
	form.admin_all_snt=False
	form.ov=False
	print('PERMISSIONS:: ',form.id)
	if perm.get('admin_all_snt') or perm.get('owner_all_snt'):
		# Если это администратор всех СНТ
		form.admin_all_snt=True
	else:

		form.snt_ids=form.db.query(
			query="select id from snt where owner_id=%s",
			values=[manager['id']],
			massive=1
		)

		if len(form.snt_ids):
			form.add_where=f"wt.snt_id in ({join_ids(form.snt_ids)})"
		else:
			form.errors.append('У Вас нет прав доступа ни к одному СНТ')

	if form.id:
		form.ov=form.db.query(
			query=f"select * from {form.work_table} where id={form.id}",
			onerow=1
		)
		print('ov:',form.ov)
		if form.ov:
			if snt_id:=form.ov.get('snt_id'):
				form.manager['files_dir']=f'./files/snt_{snt_id}'
				form.manager['files_dir_web']=f'/files/snt_{snt_id}'

			if not(form.admin_all_snt) and not(form.ov['snt_id'] in form.snt_ids):
				form.errors.append('У Вас нет прав доступа к этому СНТ')

		else:
			form.errors.append('Новость не найдена не найден!')

events={
	'permissions':permissions
}