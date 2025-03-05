from lib.anna.get_apt_list import get_apt_list_ids
from lib.anna.get_ul_list import get_ul_list_ids
def events_permissions(form):
  
  if form.script=='admin_table':
   form.remove_field('phone');
   form.remove_field('manager_phone');
  # Для менеджера Анна делаем возможность фильтровать по юридическому лицу
  if form.manager['type']==1:
    form.read_only=0
    form.not_edit=0
    form.fields.append(
      {
        'name':'ur_lico_id',
        'description':'Юридическое лицо',
        'tablename':'ul',
        'table':'ur_lico',
        'multiple':1,
        'table':'ur_lico',
        'type':'select_from_table',
        'header_field':'header',
        'value_field':'id',
        'filter_on':1,
        #'filter_code':ur_lico_id_filter_code
      }
    )
    # Для менеджеров даём возможность привязывать к аптекам учётку
    # if form.script=='edit_form' and form.id: 
    #   ov=form.db.query(query="select * from apteka where id=%s",values=[form.id],onerow=1)
    #   if ov:
    #     form.pre(ov)
    #     form.fields.append({
    #        'description':'Учётная запись',
    #        'type':'select_from_table',
    #        'table':'manager',
    #        'where':'type=3',
    #        'name':'manager_id',
    #        'order':'email',
    #        'header_field':'concat(login," (",name,")")',
    #        'value_field':'id'
    #     })

    form.QUERY_SEARCH_TABLES.append({'table':'ur_lico','alias':'ul','link':'ul.id=wt.ur_lico_id','left_join':1})
    

  elif form.manager['type']==2:
    form.manager['ul_ids']=get_ul_list_ids(form,form.manager['id'])
    # Если у данного аккаунта менее 2-х юрлиц -- скрываем фильтры ИНН и наименование
    form.manager['apt_list_ids']=get_apt_list_ids(form,form.manager['id'])
    if len(form.manager['ul_ids']) < 2:
      new_fields=[]
      for f in form.fields:
        if f['name'] not in ('inn','header'):
          new_fields.append(f)
      form.fields=new_fields
    else:
      form.fields.append({
        'description':'Юридическое лицо',
        'type':'select_from_table',
        'tablename':'ul',
        'table':'ur_lico',
        'header_field':'header',
        'value_field':'id',
        'name':'ur_lico_id',
        'where':f"id in ({','.join(form.manager['ul_ids'])})",
        #'filter_code':ur_lico_id_filter_code
      })
      form.QUERY_SEARCH_TABLES.append({'table':'ur_lico','alias':'ul','link':'ul.id=wt.ur_lico_id','left_join':1})

  # 


  if form.manager['type']==3:
    form.errors.append('доступ запрещён!')
  
  for f in form.fields:
    if f['name'] != 'manager_id': f['read_only']=1


def before_search(form):
  


  if form.manager['type']==2:
    apt_list_ids=form.manager['apt_list_ids']
    if not len(apt_list_ids):
      apt_list_ids=['0']

    form.query_search['WHERE'].append('wt.id in ('+','.join(apt_list_ids)+')')
    #form.pre(form.query_search['WHERE'])
    


events={
  'permissions':[
      events_permissions
  ],
  'before_search':[
      before_search
  ]
}

# def ur_lico_id_filter_code(form,field,row):
#   form.pre(row)