from lib.core import exists_arg
def before_search(form):
  
  # Для представителя юридического лица выводим информацию подписанных юридических лицах, а также о тех,
  # которые отправили запросы на подписку
  #form.explain=1
  qs=form.query_search
  on_filters_hash=qs['on_filters_hash']
  tables=' '.join(qs['TABLES'])
  where=' AND '.join(qs['WHERE'])
  if where:
    where=' WHERE '+where


  #form.pre(form.R)
  if not ('id' in qs['on_filters_hash']):
    form.errors.append('Фильтр "Название" обязателен')

  qs['WHERE'].append('wt.date_stop>=curdate()')
  if form.manager['type']==2:

    if len(form.manager['ur_lico_list']):
      qs['SELECT_FIELDS'].append('group_concat(distinct aul.ur_lico_id SEPARATOR "|") subscribed_ur_lico_id')
      qs['SELECT_FIELDS'].append('group_concat( distinct aa.apteka_id SEPARATOR "|" ) subscribed_apteka_id')
      
      qs['SELECT_FIELDS'].append('group_concat(distinct aul_r.ur_lico_id SEPARATOR "|") requested_ur_lico_id')
      qs['SELECT_FIELDS'].append('group_concat(distinct aa.apteka_id SEPARATOR "|" ) apteka_id_list')
  
      #form.pre(form.manager['ur_lico_ids'])
      #form.explain=1
      if 'only_subscribe' in on_filters_hash:
          if(1 in on_filters_hash['only_subscribe'] and not (0 in on_filters_hash['only_subscribe'])):
              # Ищем только подписанные
              #form.pre('where:'+where)
              #qs['WHERE'].append(f'''aul.ur_lico_id IN ({','.join(form.manager['ur_lico_ids'])})''')
              qs['WHERE'].append(f'''aul.ur_lico_id is not null''')
      
          elif(0 in on_filters_hash['only_subscribe'] and not (1 in on_filters_hash['only_subscribe'])):
              # только неподписанные
              qs['WHERE'].append(f'''aul.ur_lico_id is null''')

      
      



  if form.manager['type']==3: # для представителя аптеки
    
    if len(form.manager['apteka_list']):
      qs['SELECT_FIELDS'].append('group_concat(distinct aa.apteka_id SEPARATOR "|" ) subscribed_apteka_id')
      qs['SELECT_FIELDS'].append('group_concat(distinct aar.apteka_id SEPARATOR "|" ) requested_apteka_id')
  
    if 'only_subscribe' in on_filters_hash:

        if(1 in on_filters_hash['only_subscribe'] and not (0 in on_filters_hash['only_subscribe'])):
            # Ищем только подписанные
            #form.pre('where:'+where)
            #qs['WHERE'].append(f'''aul.ur_lico_id IN ({','.join(form.manager['ur_lico_ids'])})''')
            qs['WHERE'].append(f'''aa.apteka_id is not null''')
    
        elif(0 in on_filters_hash['only_subscribe'] and not (1 in on_filters_hash['only_subscribe'])):
            # только неподписанные
            qs['WHERE'].append(f'''aa.apteka_id is null''')

  
  if 'date_subscribe' in on_filters_hash:
    date_subscribe=on_filters_hash['date_subscribe']
    #form.pre(date_subscribe)
    if date_subscribe[0]:
      qs['WHERE'].append(
       f'''wt.date_start>="{date_subscribe[0]}-01"'''
     )
    if date_subscribe[1]:
      qs['WHERE'].append(
       f'''wt.date_stop<="{date_subscribe[1]}-31"'''
     )
  # if 'date_start' in on_filters_hash and on_filters_hash['date_start']:
  #   qs['WHERE'].append(
  #     f'''wt.date_start>="{on_filters_hash['date_start']}-01"'''
  #   )

  # if 'date_stop' in on_filters_hash and on_filters_hash['date_stop']:
  #   qs['WHERE'].append(
  #     f'''wt.date_stop<="{on_filters_hash['date_stop']}-31"'''
  #   )
  
  #form.pre(form.query_search)

  if exists_arg('date_start',on_filters_hash) and exists_arg('date_stop',on_filters_hash) and on_filters_hash['date_stop']<on_filters_hash['date_start']:
    form.errors.append('неправильно задан период')
    
  #if 'date_stop' in on_filters_hash and on_filters_hash['date_stop']:
  #  qs['WHERE'].append(f'wt.date_stop>="{on_filters_hash['date_stop']}-01" and wt.date_stop<="{on_filters_hash['date_stop']}-31" ')

  #form.pre(qs)
  #if 'date_start' in qs and
    #subscribed_ur_lico_id
    # Добавляем в поисковый запрос список подписанных юрлиц
    # form.QUERY_SEARCH_TABLES.append(
    #   {'t':'action_ur_lico','a':'aul','l':'aul.action_id=wt.id','lj':1}
    # )
    #form.pre(form.query_search)

  #form.out_before_search.append('<h2 class="subheadling mb-2">История начисления бонусов</h2>')
  
