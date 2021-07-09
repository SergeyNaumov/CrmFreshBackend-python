from lib.anna.get_ul_list import get_ul_list_ids

def events_permissions(form):
  for f in form.fields:
    f['read_only']=1

  if form.manager['type']!=1: # Для сотрудников АннА добавляем фильтр "Юридическое лицо"
    form.errors.append('Доступ запрещён')
    return
    
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

        #form.pre(m)
    
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

  qs=form.query_search


events={
  'permissions':[
      events_permissions
  ],
  'before_search':before_search
}