def cols_before_code(form,field):
	if not(field['value']):
		field['value']=1

events={
	'cols':{
		'before_code':cols_before_code
	}

}