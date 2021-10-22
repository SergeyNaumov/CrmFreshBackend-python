from lib.core import  date_to_rus
from lib.anna.get_ul_list import get_ul_list_ids, get_ul_list_from_ur_lico_id
from lib.anna.get_cur_period import get_cur_period
from lib.anna.get_apt_list import get_apt_list_ids, get_all_ids_for_aptcomp
def permissions(form):
  params={}
  
  form.manager['ur_lico_ids']=[]
  form.manager['apt_list_ids']=[]

  if 'cgi_params' in form.R:
    params=form.R['cgi_params']
    # Если это менеджер АннА, и есть параметр ur_lico_id
    if 'ur_lico_id' in params and form.manager['type']==1:
      
      form.manager['ur_lico_ids']=get_ul_list_from_ur_lico_id(form,params['ur_lico_id'])



  if form.script=='edit_form' and form.id and 'cgi_params' in form.R and 'manager_id' in form.R['cgi_params']:
    manager_id=form.R['cgi_params']['manager_id']

    form.manager['ur_lico_ids']=get_ul_list_ids(form,manager_id)
    form.manager['apt_list_ids']=get_apt_list_ids(form,manager_id)

  if form.manager['type']==2:
    form.manager['ur_lico_ids']=get_ul_list_ids(form,form.manager['id'])
    form.manager['apt_list_ids']=get_apt_list_ids(form)
    
  if form.manager['type']==3:
    form.manager['apt_list_ids']=get_apt_list_ids(form)

    form.manager['apteka_settings']={
     'set1':0,'set2':0
    }
    
    if len(form.manager['apt_list_ids']):
      apteka_id=form.manager['apt_list_ids'][0]
      form.manager['apteka_settings']=form.db.query(
        query='select set1,set2 from apteka_settings where apteka_id=%s',
        values=[apteka_id],
        onerow=1
      )
      
    

    # form.manager['apteka_settings']={
    #   'set1':1,'set2':1
    # }
    #form.pre(form.manager['apteka_settings'])
    if form.manager['apteka_settings']['set2']:
      form.manager['apt_list_ids']=get_all_ids_for_aptcomp(form,apteka_id)

   
  


  if form.script=='edit_form' and form.id and form.action =='edit':
    form.ov=form.db.query(
        query="""
            select
                ap.*, a.date_start, a.date_stop
            from
                action_plan ap
                LEFT join action a ON a.id=ap.action_id
            where ap.id=%s""",
        values=[form.id],
        onerow=1
    )
    #form.pre(form.ov)
    if form.ov:
      form.ov['period']={'id':''}
      form.ov['total_good_price']=form.db.query(
        query='select sum(price) from action_plan_good apg join good g on g.id=apg.good_id where apg.action_plan_id=%s',
        values=[form.id],
        onevalue=1
      )
      form.ov['open_summary']=0
      if ('open_summary' in params) and params['open_summary']=='1': # если этот параметр включен, тогда блок "Сводные данные по всем юридическим лицам" выводим открытым
        form.ov['open_summary']=1
        #form.pre(form.ov)

      if 'prev' in params and len(params['prev'].split('-'))==2: #prev=2021-2  период указывается явно
        period_arr=params['prev'].split('-')
        #print('period_arr:',int(period_arr[0]), int(period_arr[1]))
        form.ov['period']=form.db.query(
          query="select * from prognoz_bonus_period where year=%s and querter=%s",values=[int(period_arr[0]), int(period_arr[1])],
          onerow=1,
          debug=1
        )
        #print('period:',form.ov['period'])
        #get_cur_period(form)
      elif 'prev' in params and int(params['prev']):
        form.ov['period']=get_cur_period(form,1)
      else:
        form.ov['period']=get_cur_period(form)
    
    if form.ov:
      form.title=f'''Маркетинговое мероприятие {form.ov['header']}'''
      # смотрим сколько разных процентных ставой для товаров
      form.ov['goods_cnt_percent']=form.db.query(
        query='''
          SELECT
            count(*)
          from (
            SELECT
              *
            FROM 
              action_plan_good apg
              join good g on apg.good_id=g.id
            WHERE
              apg.action_plan_id=%s
            GROUP BY g.percent
          ) x
          
        ''',
        values=[form.id],
        onevalue=1
      )

    else:
      form.errors.append('Ссылка устарела')

    
  

events={
  'permissions':[
    permissions
  ],
  'before_search':[

  ]
}