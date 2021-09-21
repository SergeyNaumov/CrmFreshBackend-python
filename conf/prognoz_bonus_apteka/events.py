from lib.anna.get_apt_list import get_apt_list_ids, get_all_ids_for_aptcomp

def events_permissions(form):
  
  for f in form.fields:
    f['read_only']=1

  if form.manager['type']==2: # Для сотрудников АннА добавляем фильтр "Юридическое лицо"
    form.errors.append('Доступ запрещён')
    return
  
  if form.manager['type']==3:
    
    if form.script=='admin_table': # для аптеки скрываем фильтр "аптека", чтобы не маячил, но включаем его искусственно в before_search
      form.remove_field('apteka_id')

    form.manager['apteka_settings']={
      'set1':1,'set2':1
    }
    form.manager['apt_list_ids']=get_apt_list_ids(form)
    
    if len(form.manager['apt_list_ids']):
      apteka_id=form.manager['apt_list_ids'][0]
      apteka_settings=form.db.query(
        query='select set1,set2 from apteka_settings where apteka_id=%s',
        values=[apteka_id],
        onerow=1
      )
      if apteka_settings: form.manager['apteka_settings']=apteka_settings



    if form.manager['apteka_settings']['set2']:
      form.manager['apt_list_ids']=get_apt_list_ids(form)
      #print('apt_list_ids:',form.manager['apt_list_ids'])
    

  if form.manager['type']==1:
    form.fields.append(
      {
        'description':'Менеджер АннА',
        'name':'manager_id',
        'type':'filter_extend_select_from_table',
        'db_name':'id',
        'table':'manager',
        'filter_on':1,
        'where':'type=1',
        'header_field':'name',
        'value_field':'id',
        'tablename':'m'
      }
    )
  if form.script=='edit_form' and form.id:

    

    ov=form.db.query(
      query=f"""
        SELECT
          wt.*
        from 
          {form.work_table} wt
        WHERE
          wt.id=%s
      """,
      values=[form.id],
      onerow=1
    )

    if ov['action_id']:
      ov['action']=form.db.query(
        query="SELECT * from action where id = %s",
        values=[ov['action_id']],
        onerow=1
      )

    ov['action_plan']={}
    if ov['action_plan_id']:
      ov['action_plan']=form.db.query(
        query="SELECT * from action_plan where id = %s",
        values=[ov['action_plan_id']],
        onerow=1
      )
    
    if ov['apteka_id']:
      ov['apteka']=form.db.query(
        query="SELECT id,inn,ur_lico_id,ur_address header from apteka where id = %s",
        values=[ov['apteka_id']],
        onerow=1
      )

      ov['manager']=form.db.query(
        query="""
          SELECT 
            m.id, m.login
          from
            manager m 
          WHERE id=%s
        """,
        #onerow=1,
        values=[ov['apteka_id']]
      )

      # for m in ov['managers']:
      #   m['ur_lico_list']=form.db.query(
      #     query="""
      #       select group_concat(u.header SEPARATOR " ; ") 
      #       FROM
      #         ur_lico u
      #         join ur_lico_manager ulm on ulm.ur_lico_id=u.id
      #       WHERE ulm.manager_id=%s
      #       GROUP BY ulm.manager_id
      #     """,
      #     onevalue=1,
      #     values=[m['id']]
      #   )

      
    
    if ov['period_id']:
      ov['period']=form.db.query(
        query="""
          SELECT 
            *,
            (curdate()>date_end) prev, 
            (to_days(date_end)-to_days(date_begin)) querter_total_days,  
            (to_days(curdate()) - to_days(date_begin) )+1 querter_begin_days
          FROM prognoz_bonus_period where id = %s
        """,
        values=[ov['period_id']],
        onerow=1
      )

    # cgi_params={}
    
    # if 'cgi_params' in form.R:
    #   cgi_params=form.R['cgi_params']
    #   if cgi_params['manager_id']:
    #form.pre(ov['period'])
    form.ov=ov
    
    form.title=f'''Прогнозный бонус для {ov['apteka']['header']}<br><small>({ov['action']['header']}/{ov['action_plan']['header']}), {ov['period']['querter']} квартал {ov['period']['year']}</small>'''


def before_search(form):

  qs=form.query_search
  if form.manager['type']==3:

    #qs['on_filters_hash']['apteka_id']=[]
    #form.R['query'].append(["action_id",[]])
    #form.pre(qs)

    
    #qs['WHERE'].append(f"wt.apteka_id in ({','.join(form.manager['apt_list_ids'])})")
    qs['WHERE'].append(f"u.manager_id = {form.manager['id']}")

events={
  'permissions':[
      events_permissions
  ],
  'before_search':before_search
}