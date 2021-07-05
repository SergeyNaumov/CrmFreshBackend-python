from lib.anna.get_apt_list import get_apt_list_ids
from lib.anna.get_ul_list import get_ul_list_ids
def events_permissions(form):
  

  # Для менеджера Анна делаем возможность фильтровать по юридическому лицу
  if form.manager['type']==1:
    form.fields.append(
      {
        'name':'ur_lico_id',
        'description':'Юридическое лицо',
        'tablename':'ul',
        'table':'ur_lico',
        'multiple':1,
        'type':'select_from_table',
        'header_field':'header',
        'value_field':'id',
        'filter_on':1
      }
    )
    form.QUERY_SEARCH_TABLES.append({'table':'ur_lico','alias':'ul','link':'ul.id=wt.ur_lico_id','left_join':1})

  elif form.manager['type']==2:
    form.manager['ul_ids']=get_ul_list_ids(form,form.manager['id'])
    # Если у данного аккаунта менее 2-х юрлиц -- скрываем фильтры ИНН и наименование
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
        'table':'ur_lico',
        'header_field':'header',
        'value_field':'id',
        'name':'ur_lico_id',
        'where':f"id in ({','.join(form.manager['ul_ids'])})"
      })

  # 


  if form.manager['type']==3:
    form.errors.append('доступ запрещён!')
  
  for f in form.fields:
    f['read_only']=1


def before_search(form):
  


  if form.manager['type']==2:
    apt_list_ids=get_apt_list_ids(form,form.manager['id'])
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