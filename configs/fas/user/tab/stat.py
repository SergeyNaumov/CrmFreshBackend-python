# def stat_before_code(form,field):
# 	if inn:=form.ov.get('inn'):
# 		db=form.db
# 		# уклонений
# 		rejection_cnt=db.query(query="select count(*) from rejection where inn=%s",values=[inn],onevalue=1)
# 		contract_termination_cnt=db.query(query="select count(*) from contract_termination where inn=%s",values=[inn],onevalue=1)
# 		rnp_reestr_from_ftp_cnt=db.query(query="select count(*) from rnp_reestr_from_FTP where client_inn=%s",values=[inn],onevalue=1)

# 		field['html']=f"""
# 			Уклонений: {rejection_cnt}<br>
# 			Расторжений: {contract_termination_cnt}<br>
# 			Реестр РНП: {rnp_reestr_from_ftp_cnt}<br>
# 		"""

stat_component_folder="/files/fas-components/user_card/stat"
default_component_folder="/files/fas-components/user_card/default"



def default_component_before_code(form,field):
	field['data']={
		'form':{
			'id':form.id, 'read_only':form.read_only,
			'ov':form.ov
		}
	}

fields=[
	# {
	# 	'name':'stat',
	# 	'not_filter':1,
	# 	'type':'component',
	# 	'template':f'{stat_component_folder}/template.html',
	# 	#'methods':f'{stat_component_folder}/methods.js',
	# 	'object':f'{stat_component_folder}/object.js',
	# 	'tab':'stat'
	# },
	{
		'name':'default_component',
		'not_filter':1,
		'type':'component',
		'template':f'{default_component_folder}/template.html',
		#'methods':f'{stat_component_folder}/methods.js',
		'before_code': default_component_before_code,
		'object':f'{default_component_folder}/object.js?nc=1',
		'tab':'stat'
	},
]