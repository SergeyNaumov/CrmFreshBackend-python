from lib.engine import s
from lib.core import exists_arg, date_to_rus
from .get_old_values import get_old_values
#from lib.anna.get_apt_list import get_apt_list_ids
def events_permissions(form):
  #form.pre('zzz')
  filter_ur_lico(form)
  form.ur_lico_subscribe=None
  
  if form.manager['type']==3:
    apteka_id=form.db.query(
      query=f"select id from apteka where manager_id={form.manager['id']}",onevalue=1
    )
    
    apteka_settings={
      'id':apteka_id,
      'set1':0,'set2':0
    }
    if apteka_id:
      apteka_settings=form.db.query(
       query=f'select apteka_id id, set1,set2 from apteka_settings where apteka_id=%s',
       values=[apteka_id],
       onerow=1
      )


    form.manager['apteka_settings']=apteka_settings

   #form.manager['apteka_list']=get_apt_list_ids(form,form.manager['id'])
    #form.pre(form.manager['apteka_list'])

  # Фильтр для юрлиц
  if form.script in ['admin_table', 'find_objects'] and form.manager['type'] in (2,3):
    #form.QUERY_SEARCH_TABLES.append(
    #  {'t':'action_ur_lico','a':'aul','l':'wt.id=aul.action_id','lj':1}
    #)
    #form.explain=1
    form.fields.append(
      {
          'name':'date_subscribe',
          'description':'Даты подписки',
          'type':'yearmon',
          'filter_on':1,
          'filter_type':'range',
          'not_process':1,
          'filter_code':date_subscribe_filter_code
      }
    )
    
    # form.fields.append(
    #     {
    #       'description':'Подписанные мероприятия',#'только те маркетинговые мероприятия, на которые я подписан',
    #       'type':'checkbox',
    #       'name':'only_subscribe',
    #       'not_process':1,
    #       'filter_code':filter_code_subscribe,
    #       'filter_on':1
    #     }
    # )

  if form.id:

    #form.ov=form.db.query(
    #  query='select * from action where id=%s',
    #  values=[form.id],
    #  onerow=1
    #)

    form.ov=get_old_values(form)

    if not form.ov: return
    #form.pre(form.ov)

    if form.ov:
      form.title='Маркетинговое мероприятие '+form.ov['header']

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
    if form.manager['type']==2: 
      
      


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

      form.javascript['find_objects']="//find_objects_ur_lico.js\n"+form.template(
        './conf/action/templates/find_objects_ur_lico.js',
      )


    elif form.manager['type']==3: # аптека

      
      form.javascript['find_objects']="//find_objects_apteka.js\n"+form.template(
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
           #'filter_on':1,
           'not_process':1
         }
      )
     # print(f"script: {form.script}")
      #form.pre(form.fields)


def filter_code_subscribe(form,field,row):
  pass
  #form.pre(row)


def date_subscribe_filter_code(form,field,row):
  



  if form.manager['type']==2: # Юридическое лицо
    #form.pre(row)
    # получаем списки подписанных и отправивших запрос на акцию юрлиц
    if not exists_arg('subscribed_ur_lico_id',row): row['subscribed_ur_lico_id']=''
    if not exists_arg('subscribed_apteka_id',row): row['subscribed_apteka_id']=''

    if not exists_arg('requested_ur_lico_id',row): row['requested_ur_lico_id']=''
    
    row['subscribed_apteka_id']=row['subscribed_apteka_id'].split('|')
    row['subscribed_ur_lico_id']=row['subscribed_ur_lico_id'].split('|')
    row['requested_ur_lico_id']=row['requested_ur_lico_id'].split('|')
    #form.pre(row['subscribed_apteka_id'])
    #ur_lico_subscribe='[{"id":"1","name":"ЗАО лекарствснаб","v":"0"},{"id":"2","name":"ФЕРЕЙН","v":"1"},{"id":"3","name":"ООО Ихтиандр","v":"2"}]'
    ur_lico_subscribe=[]
    

    for u in form.manager['ur_lico_list']:
      
      need_append=False
      
      if not exists_arg('ur_lico_id',form.query_hash):
        need_append=True
      elif exists_arg('ur_lico_id',form.query_hash) and len(form.query_hash['ur_lico_id']):
        # В том случае, когда мы фильтруем по юрлицам -- выводим информацию о подписке только по тем юрлицам, по которым ищем
        if u['id'] in form.query_hash['ur_lico_id']:
          need_append=True
        else:
          need_append=False
      v=0
      if str(u['id']) in row['subscribed_ur_lico_id']: v=2 # подписанных
      elif str(u['id']) in row['requested_ur_lico_id']: v=1 # отправил запрос на подписку
      else: v=0
      
      if need_append:
        # u['apt_ids'] -- id-шники аптек для конкретного юрлица
        #form.pre({
        #  'u_apt_ids':u['apt_ids'],
        #  'subscribed_apteka_id':row['subscribed_apteka_id'],
        #  'cnt_apt':len(list(set(u['apt_ids']) & set(row['subscribed_apteka_id'])))
        #})
        ur_lico_subscribe.append({
          'id':u['id'],
          'action_id':row['wt__id'],
          'v':str(v),
          'name':u['name'],
          'apt_cnt':len(list(set(u['apt_ids']) & set(row['subscribed_apteka_id'])))
        })

    #form.pre(['subscribe',ur_lico_subscribe])
    # Количество подписанных аптек
    apteka_subscribe=0
    ur_lico_subscribe=s.to_json(ur_lico_subscribe)
    
    if (row['apteka_id_list']):
      apteka_subscribe=len(row['apteka_id_list'].split('|'))
    return f'''
      {date_to_rus(row['wt__date_start']) } - { date_to_rus(row['wt__date_stop'])}
      <div id="anna_subscr{row["wt__id"]}" class="subscibe_buttons">{ur_lico_subscribe}|{apteka_subscribe}</div>'''


  elif form.manager['type']==3: # Аптека
    # subscribe_status: 0 - не подписна ; 1 - отправлен запрос на участие ; 2- подписана
    if not exists_arg('subscribed_apteka_id',row): row['subscribed_apteka_id']=''
    row['subscribed_apteka_id']=row['subscribed_apteka_id'].split('|')
    if not exists_arg('requested_apteka_id',row): row['requested_apteka_id']=''
    row['requested_apteka_id']=row['requested_apteka_id'].split('|')

    apteka_subscribe=[]

    for a in form.manager['apteka_list']:
      v=0
      if str(a['id']) in row['subscribed_apteka_id']: v=2
      if str(a['id']) in row['requested_apteka_id']: v=1
      apteka_subscribe.append({'id':a['id'],'v':str(v),'name':a['name']})
    apteka_subscribe=s.to_json(apteka_subscribe)


    return f'''{date_to_rus(row['wt__date_start']) } - { date_to_rus(row['wt__date_stop'])}
      <div id="anna_subscr{row["wt__id"]}" class="subscibe_buttons">{apteka_subscribe}</div>'''

    #form.pre(apteka_subscribe)

    #form.pre(row)
    subscribe_status=0
    return subscribe_status
    # else:
  return ''