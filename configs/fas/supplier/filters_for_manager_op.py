from lib.core import cur_date
def prepare_filters_for_manager_op(form):
	# Подготовка фильтров для менеджера ОП

	fields_hash={}
	for f in form.fields:
		f['filter_on']=0
		fields_hash[f['name']]=f
	# включаем фильтры для менеджера
	for name in ('firm', 'region_id','inn','manager_id','contact_date'):
		f=fields_hash[name]
		f['filter_on']=1
		if name=='contact_date':
			f['value']=[cur_date(),'']
	#fields_hash[]
	#form.pre(fields_hash)