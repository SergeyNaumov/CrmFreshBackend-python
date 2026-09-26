from lib.core import cur_date
def registered_before_code(form,field):
	if form.action=='new':
		field['value']=cur_date()

def enabled_before_code(form,field):
	if form.action=='new':
		field['value']=1

def type_before_code(form,field):
	if form.action=='new':
		field['value']=1

def photo_filter_code(form,field,row):

	if photo:=row.get('wt__photo'):
		return f'<img style="width: 100px" src="{field["filedir"].replace("./","/")}/{photo}">'
	return ''

events={
	'registered':{
		'before_code':registered_before_code
	},
	'enabled':{
		'before_code':enabled_before_code
	},
	'type':{
		'before_code':type_before_code
	},
	'photo':{
		'filter_code':photo_filter_code
	}
}