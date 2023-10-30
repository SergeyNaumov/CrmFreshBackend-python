def prepare_filters_for_find_inn_doubles(form,inn):
	form.search_on_load=1
	fields_hash={}
	for f in form.fields:
		f['filter_on']=0
		fields_hash[f['name']]=f

	# включаем фильтры для поиска по ИНН:
	for name in ('firm', 'region_id','inn','manager_id','memo', 'contact_date'):
		f=fields_hash[name]
		f['filter_on']=1
	f=fields_hash['inn']['value']=inn