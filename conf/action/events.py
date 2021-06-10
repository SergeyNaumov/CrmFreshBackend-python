from .permissions import events_permissions, filter_ur_lico



def before_search(form):
  
  # Для представителя юридического лица выводим информацию подписанных юридических лицах, а также о тех,
  # которые отправили запросы на подписку
  #form.explain=1
  form.query_search['WHERE'].append('wt.date_stop>=curdate()')
  if str(form.manager['type'])=='2':
    if len(form.manager['ur_lico_list']):
      form.query_search['SELECT_FIELDS'].append('group_concat(distinct aul.ur_lico_id SEPARATOR "|") subscribed_ur_lico_id')
      form.query_search['SELECT_FIELDS'].append('group_concat(distinct aul_r.ur_lico_id SEPARATOR "|") requested_ur_lico_id')
      form.query_search['SELECT_FIELDS'].append('group_concat(distinct aa.apteka_id SEPARATOR "|" ) apteka_id_list')
  

  if str(form.manager['type'])=='3': # для представителя аптеки
    if len(form.manager['apteka_list']):
      form.query_search['SELECT_FIELDS'].append('group_concat(distinct aa.apteka_id SEPARATOR "|" ) subscribed_apteka_id')
      form.query_search['SELECT_FIELDS'].append('group_concat(distinct aar.apteka_id SEPARATOR "|" ) requested_apteka_id')
      
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