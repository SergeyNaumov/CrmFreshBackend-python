from lib.anna.get_ul_list import get_ul_list_ids

def events_permissions(form):
  #form.explain=1
  for f in form.fields:
    f['read_only']=1

  if form.manager['type']==3: # Для сотрудников АннА добавляем фильтр "Юридическое лицо"
    form.errors.append('Доступ запрещён')
    return
  
  if form.manager['type']==2:
    form.manager['ur_lico_ids']=get_ul_list_ids(form,form.manager['id'])
  
  if form.script == 'find_objects':
    form.remove_field('out_action')

  if form.manager['type']==1 and form.script in ('admin_table','find_objects'):
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
    
    if ov['ur_lico_id']:
      ov['ur_lico']=form.db.query(
        query="SELECT * from ur_lico where id = %s",
        values=[ov['ur_lico_id']],
        onerow=1
      )

      ov['managers']=form.db.query(
        query="""
          SELECT 
            m.id, m.login
          from
            manager m 
            join ur_lico_manager ulm ON ulm.manager_id=m.id
          WHERE ulm.ur_lico_id=%s
        """,
        values=[ov['ur_lico_id']]
      )

      for m in ov['managers']:
        m['ur_lico_list']=form.db.query(
          query="""
            select group_concat(u.header SEPARATOR " ; ") 
            FROM
              ur_lico u
              join ur_lico_manager ulm on ulm.ur_lico_id=u.id
            WHERE ulm.manager_id=%s
            GROUP BY ulm.manager_id
          """,
          onevalue=1,
          values=[m['id']]
        )

      
    
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
    
    form.title=f'''Прогнозный бонус для {ov['ur_lico']['header']}<br><small>({ov['action']['header']}/{ov['action_plan']['header']}), {ov['period']['querter']} квартал {ov['period']['year']}</small>'''


def before_search(form):
  # для менеджера Анна фильтр "Юридическое лицо" обязателен
  if form.manager['type']==1 and not ('ur_lico_id' in form.query_hash):
    form.errors.append('Фильтр "Юридическое лицо" обязателен')
  
  qs=form.query_search
  if 'priority_sort' in form.R['params']:
    if form.R['params']['priority_sort'][0]=='period_id' and form.R['params']['priority_sort'][1] in ('asc','','desc'):

      qs['ORDER']=[f"pbp.date_begin "+form.R['params']['priority_sort'][1]]
      
  #form.explain=1
  qs['SELECT_FIELDS'].append('if(pbp.date_end < curdate(),1,0) prev ')
  period_ids=[]
  
  if form.manager['type']==2 and not(form.manager['show_old_plans']): # Если это юрлицо -- и не включена возможность просмотра периода прошлых периодов
    period_ids=form.db.query(
      query='select id from prognoz_bonus_period where date_begin>=curdate() or date_end >= curdate()- interval 14 day',
      massive=1,
      str=1
    )
 # else: # берём периоды не старше чем 90*2 дней (2 квартала назад)
    # https://trello.com/c/jIJUAtC5/81-%D0%BF%D1%80%D0%BE%D0%B3%D0%BD%D0%BE%D0%B7%D0%BD%D1%8B%D0%B9-%D0%B1%D0%BE%D0%BD%D1%83%D1%81
    #period_ids=form.db.query(
    #  query='select id from prognoz_bonus_period where date_begin>=curdate()- interval 90*2 day',
    #  massive=1,
    #  str=1
    #)
  
  if len(period_ids):
    qs['WHERE'].append(f"wt.period_id IN ({ ','.join(period_ids) })")
  

  
  if form.manager['type']==2:
    qs['WHERE'].append(f"wt.ur_lico_id in ({','.join(form.manager['ur_lico_ids'])})")

events={
  'permissions':[
      events_permissions
  ],
  'before_search':before_search
}