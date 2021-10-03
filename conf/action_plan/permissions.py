
from .get_old_values import get_old_values

def events_permissions(form):
  form.pre(form.R)
  #filter_ur_lico(form)
  #print('action:',form.action)
  #print('script:',form.script)
  if form.id:
    #form.ov=form.db.query(
    #  query='select * from action where id=%s',
    #  values=[form.id],
    #  onerow=1
    #)

    form.ov=get_old_values(form)
    #form.pre(form.ov)

    if form.ov:
      form.title=f'''Маркетинговое мероприятие {form.ov['header']}!<br><small>dkjskj</small>'''
      

  new_fields=[]
  for f in form.fields:
    f['read_only']=1
    if form.id:
      if not (f['name'] in ['date_start','date_stop']):
         new_fields.append(f)

      if  f['name'] =='date_stop':
        new_fields.append({
          'description':'Даты подписки',
          'type':'code',
          'after_html':f'<p><b>Дата подписки:</b> { form.ov["date_start"] } - { form.ov["date_stop"] }</p>',
          'name':'dates'
        })
    else:
      new_fields.append(f)




  form.fields=new_fields
  

  if form.script in ['find_objects']:

    for f in form.fields:
      if f['name']=='date_start':
        f['description']='Период подписки'
      
      if f['name']=='date_stop':
        f['description']='Подписка'

  #if form.script=='admin_table':
    #form.javascript['admin_table']=form.template(
      #'./conf/action/templates/admin_table.js',
    #)


  
  if form.script=='find_objects':
    
    # Представитель ЮЛ, кнопки подписки
    if str(form.manager['type'])=='2': 
      
      


      ur_lico_list=form.manager['ur_lico_list']
      form.manager['apteka_ids_list']=[]
      # добавляем в запрос для подписанных юрлиц
      if len(ur_lico_list): 

        ur_lico_ids=[]
        for u in ur_lico_list: ur_lico_ids.append(str(u['id']))
        

        # Получаем id-шники аптек
        form.manager['apteka_ids_list']=form.db.query(
          query='select id from apteka where ur_lico_id in ('+','.join(ur_lico_ids)+')',
          massive=1,
          str=1
        )
        #form.pre(form.manager['apteka_ids_list'])
        
        # Добавляем в поисковый запрос список подписанных юрлиц
        form.QUERY_SEARCH_TABLES.append(
          {'t':'action_ur_lico','a':'aul','l':'aul.action_id=wt.id and aul.ur_lico_id in ('+','.join(ur_lico_ids)+')','lj':1}
        )

        # 
        form.QUERY_SEARCH_TABLES.append(
                {'t':'prognoz_bonus','a':'pb','l':f'pb.action_id=wt.id AND pb.ur_lico_id in ({ ",".join(ur_lico_ids)})'}
        )

        # добавляем в запрос для юрлиц, отправивших запрос на подписку

        form.QUERY_SEARCH_TABLES.append(
          {'t':'action_ur_lico_request','a':'aul_r','l':'aul_r.action_id=wt.id and aul_r.ur_lico_id in ('+','.join(ur_lico_ids)+')','lj':1}
        )
        if not len(form.manager['apteka_ids_list']):
          form.manager['apteka_ids_list']=['0']

        # для подсчёта кол-ва подписанных аптек
        form.QUERY_SEARCH_TABLES.append(
          {'t':'action_apteka','a':'aa','l':'wt.id=aa.action_id and aa.apteka_id in ('+','.join(form.manager['apteka_ids_list'])+')','lj':1}
        )


      form.GROUP_BY='wt.id'
      #form.explain=1

      form.javascript['find_objects']=form.template(
        './conf/action/templates/find_objects_ur_lico.js',
      )


    elif str(form.manager['type'])=='3': # аптека

      form.explain=1
      form.javascript['find_objects']=form.template(
        './conf/action/templates/find_objects_apteka.js',
      )
      #form.pre(form.javascript)

      apteka_list=form.db.query(
        query='''
          SELECT
            id,concat(id," ",ur_address) name
          from 
            apteka
            
          WHERE manager_id=%s 
        ''', # WHERE manager_id=%s or manager_id>0 limit 10
        values=[form.manager['id']]
      )

      form.manager['apteka_list']=apteka_list
      if len(apteka_list):

        apteka_ids=[]
        for a in apteka_list:
          apteka_ids.append(str(a['id']))

        form.QUERY_SEARCH_TABLES.append(
          {'t':'action_apteka','a':'aa','l':'wt.id=aa.action_id and aa.apteka_id in ('+','.join(apteka_ids)+')','lj':1}
        )
        form.QUERY_SEARCH_TABLES.append(
          {'t':'action_apteka_request','a':'aar','l':'wt.id=aar.action_id and aar.apteka_id in ('+','.join(apteka_ids)+')','lj':1}
        )
        form.GROUP_BY='wt.id'
        #form.pre(apteka_ids)
        #form.explain=1

def filter_ur_lico(form):
  # в том случае, если это юридическое лицо, в подчинении у которого есть другие юрлица -- выводим фильтр для фильтрации по этим юрлицам
  if form.manager['type']==2 and form.script in ['admin_table','find_objects','edit_form']:
      form.manager['ur_lico_list']=form.db.query(
        query='''
          SELECT
            wt.id,wt.header name,
            group_concat(distinct a.id SEPARATOR "|") apt_ids
          from 
            ur_lico wt
            JOIN ur_lico_manager ulm ON wt.id=ulm.ur_lico_id
            LEFT JOIN apteka a ON a.ur_lico_id=wt.id
          WHERE ulm.manager_id=%s
          GROUP BY wt.id
        ''',
        values=[form.manager['id']]
      )
      apt_list_ids=[]

      for u in form.manager['ur_lico_list']:
        u['apt_ids']=u['apt_ids'].split('|')
        apt_list_ids=list(apt_list_ids)+list(u['apt_ids'])
      
      if not len(apt_list_ids): apt_list_ids=[]
      form.manager['apt_list_ids']=apt_list_ids

      ur_lico_ids=[]

      
      for u in form.manager['ur_lico_list']: ur_lico_ids.append(str(u['id']))
      form.manager['ur_lico_ids']=ur_lico_ids
      if not len(ur_lico_ids): ur_lico_ids=['0']

      #form.pre(form.manager['ur_lico_list'])


  
  if form.manager['type']==2:
    if form.script in ['admin_table','find_objects'] and len(form.manager['ur_lico_list'])>1:


      
      #form.explain=1
      form.fields.append(
         {
           'name':'ur_lico_id',
           'description':'Юридическое лицо',
           'type':'filter_extend_select_from_table',
           'table':'ur_lico',
           'header_field':'header',
           'value_field':'id',
           'tablename':'aul',
           'where':'id in ('+','.join(form.manager['ur_lico_ids'])+')',
           'filter_on':1,
           'not_process':1
         }
      )
     # print(f"script: {form.script}")
      #form.pre(form.fields)