from .permissions import events_permissions, filter_ur_lico

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


  #form.pre(form.query_search)
  #form.pre(query_apt_count)
  form.query_search['WHERE'].append('wt.date_stop>=curdate()')
  if str(form.manager['type'])=='2':
    if len(form.manager['ur_lico_list']):
      qs['SELECT_FIELDS'].append('group_concat(distinct aul.ur_lico_id SEPARATOR "|") subscribed_ur_lico_id')
      qs['SELECT_FIELDS'].append('group_concat( distinct aa.apteka_id SEPARATOR "|" ) subscribed_apteka_id')
      
      qs['SELECT_FIELDS'].append('group_concat(distinct aul_r.ur_lico_id SEPARATOR "|") requested_ur_lico_id')
      qs['SELECT_FIELDS'].append('group_concat(distinct aa.apteka_id SEPARATOR "|" ) apteka_id_list')
      


  if str(form.manager['type'])=='3': # для представителя аптеки
    if len(form.manager['apteka_list']):
      qs['SELECT_FIELDS'].append('group_concat(distinct aa.apteka_id SEPARATOR "|" ) subscribed_apteka_id')
      qs['SELECT_FIELDS'].append('group_concat(distinct aar.apteka_id SEPARATOR "|" ) requested_apteka_id')
  
  
  if 'date_start' in on_filters_hash and on_filters_hash['date_start']:
    qs['WHERE'].append(
      f'''wt.date_start>="{on_filters_hash['date_start']}-01"'''
    )

  if 'date_stop' in on_filters_hash and on_filters_hash['date_stop']:
    qs['WHERE'].append(
      f'''wt.date_stop<="{on_filters_hash['date_stop']}-31"'''
    )

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
  

events={
  'permissions':[
      events_permissions
      #filter_ur_lico
  ],
  'before_search':[
      before_search
  ]
}