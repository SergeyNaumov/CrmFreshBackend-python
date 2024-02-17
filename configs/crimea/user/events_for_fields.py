from lib.core import join_ids

def snt_id_before_code(form,field):
	if form.script=='edit_form' and form.action in ('edit','update'):
		field['read_only']=1

	if not(form.admin_all_snt):
		#print('snt_ids:',form.snt_ids)
		if len(form.snt_ids):
		 	field['where']=f"id in ({join_ids(form.snt_ids)})"

events={
	'snt_id':{
		'before_code':snt_id_before_code
	}
}