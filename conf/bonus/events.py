from lib.anna.get_ul_list import get_ul_list_ids

def events_permissions(form):
  for f in form.fields:
    f['read_only']=1

  if form.manager['type']==1: # Для сотрудников АннА добавляем фильтр "Юридическое лицо"
    form.QUERY_SEARCH_TABLES.append(
      {'t':'ur_lico','a':'u','l':'wt.partner_id=u.id','lj':1}
    )
    form.fields.append(
      {
        'description':'Юридическое лицо',
        'type':'select_from_table',
        'name': 'partner_id',
        'table':'ur_lico',
        'header_field':'header',
        'value_field':'id',
        'tablename':'u',
        'filter_on':1,
        'autocomplete':1
      }
    )

    # Принудительно выводим в результатах
#    if form.script=='find_objects':

    #  form.R['query'].append(['summ',''])
      #form.R
    #form.pre([form.script, form.R])

def before_search(form):

  qs=form.query_search
  #form.pre(qs)
  
  #form.pre()
  if not len(qs['ORDER']):
    qs['ORDER']=['date_create desc']
  #form.pre(qs)
  # имитируем включенный фильтр суммы:
  #qs['on_filters_hash']['summ']=[]

  if form.manager['type']==2:
    #form.explain=1
    ur_lico_ids=get_ul_list_ids(form,form.manager['id'])
    form.query_search['WHERE'].append(f"partner_id in ({','.join(ur_lico_ids)})")

  
  query_summ=f'''
    SELECT
      sum(summ)
    FROM
      {" ".join(qs['TABLES'])}
  '''
  values=[]

  if len(qs['WHERE']):
    query_summ+=' WHERE '+' AND '.join(qs['WHERE'])
    values=qs['VALUES']

  total_bonus=form.db.query(
    query=query_summ,
    onevalue=1,
    values=values
  )

  # form.out_before_search.append(f'''
  #   <h2 class="subheadling mb-2">История начисления бонусов</h2>
  #   <p>Вы можете подписать акт через ЭДО. Для этого вам необходимо ознакомиться с <a href="/files/const/template_edo.doc">шаблоном для подключения ЭДО</a></p>
  #   <p>Заработанный бонус за всё время: {total_bonus} руб</p>

  # ''')

events={
  'permissions':[
      events_permissions
  ],
  'before_search':before_search
}