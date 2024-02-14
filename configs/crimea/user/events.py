from lib.core import join_ids

def permissions(form):
	manager=form.manager
	perm=manager.get('permissions')
	#form.pre(perm)
	form.snt_ids=[]
	form.admin_all_snt=False
	form.ov=False

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
		if form.ov:
			print('ov:',form.ov, form.snt_ids)
			if not(form.admin_all_snt) and not(form.ov['snt_id'] in form.snt_ids):
				form.errors.append('У Вас нет прав доступа к этому СНТ')

		else:
			form.errors.append('Член СНТ не найден!')

	#form.pre(form.snt_ids)

# def after_insert(form):
# 	if not(form.admin_all_snt) and len(form.snt_ids) == 1:
# 		# это председатель одного единственного СНТ
# 		form.db.query(
# 			query=f"UPDATE {form.work_table} set snt_id={form.snt_ids[0]} where id={form.id}"
# 		)


def before_save(form):
	snt_id=form.new_values.get('snt_id')
	form.pre(form.new_values)
	if not(snt_id) or snt_id=='0':
		form.errors.append('укажите СНТ')

events={
	'permissions':permissions,
	#'after_save': after_insert
	'before_save':before_save
}