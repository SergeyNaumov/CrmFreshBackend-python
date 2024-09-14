def prepare_filters_for_find_inn_doubles(form,inn):
    if inn:
        print('inn:',inn)
        form.search_on_load=1
        form.title+=f' (поиск по ИНН {inn})'
        fields_hash={}

        for f in form.fields:
            f['filter_on']=0
            fields_hash[f['name']]=f

        f=fields_hash['inn']['value']=inn

    # включаем фильтры для поиска по ИНН:
    for name in ('name', 'email', 'inn','phone'):
       f=fields_hash[name]
       f['filter_on']=1

    f=fields_hash['inn']['value']=inn