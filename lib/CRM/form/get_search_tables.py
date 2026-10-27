from lib.core import exists_arg, get_func
import re

#def adding_select_fields()

def adding_select_fields_in_desc(form,db_field,t):
  fld_on_query=t['alias']+'.'+db_field['Field']+' '+t['alias']+'__'+db_field['Field']
  if not exists_arg('select_fields', t):
    form.query_search['SELECT_FIELDS'].append(fld_on_query)
  #if  t['alias']=='mg':
    
  if exists_arg('select_fields', t) and (db_field['Field'] in t['select_fields']):
    form.query_search['SELECT_FIELDS'].append(fld_on_query)

    


  

async def get_search_tables(form,query):
  TABLES=[]
  if not len(form.QUERY_SEARCH_TABLES):
    form.QUERY_SEARCH_TABLES=[
      {'t':form.work_table,'a':'wt'}
    ]

  # Поле ЧПУ (type=in_ext_url) участвует и в списке, и в фильтрах: подмешиваем
  # LEFT JOIN in_ext_url, чтобы отдать колонку in_ext_url__ext_url
  # (process_result_list) и дать фильтр по ext_url (get_search_where).
  if not any((t.get('a') or t.get('alias'))=='in_ext_url'
             for t in form.QUERY_SEARCH_TABLES):
    chpu_field=next((f for f in (form.fields or [])
                     if f.get('type')=='in_ext_url' and f.get('in_url')),None)
    if chpu_field:
      # '<%id%>' в шаблоне заменяем на wt.id через CONCAT (без литерала '%':
      # строка запроса потом проходит через python-форматирование).
      pre,_,post=str(chpu_field['in_url']).partition('<%id%>')
      pre=pre.replace("'","''").replace('%','%%')
      post=post.replace("'","''").replace('%','%%')
      if post:
        in_url_expr="CONCAT('%s', wt.id, '%s')" % (pre,post)
      else:
        in_url_expr="CONCAT('%s', wt.id)" % pre
      form.QUERY_SEARCH_TABLES.append({
        't':'in_ext_url','a':'in_ext_url','lj':1,
        'l':("in_ext_url.project_id=wt.project_id AND "
             "in_ext_url.in_url="+in_url_expr),
        'select_fields':['ext_url'],
      })

  aliases_on={'wt':1}
  for t in form.QUERY_SEARCH_TABLES:
    t_str=''
    need_add_table=1
    if not exists_arg('table',t) and exists_arg('t',t):
      t['table']=t['t']
    
    if not exists_arg('alias',t)  and exists_arg('a',t):
      t['alias']=t['a']

    if not exists_arg('left_join',t) and exists_arg('lj',t):
      t['left_join']=t['lj']

    if not exists_arg('link',t)  and exists_arg('l',t):
      t['link']=t['l']

    if exists_arg('link',t):
      if exists_arg('left_join',t):
        t_str = t_str + ' LEFT '
      
      t_str = ''.join([t_str,' JOIN ',t['table'],' as ',t['alias'],' ON (',t['link'],')'])

      if exists_arg('for_fields',t) :
        need_add_table = 0

        for fld_name in t['for_fields']:
          
          if fld_name in form.query_search['on_filters_hash']:
            need_add_table = 1
            break

    else:
      tbl=str(t['table']).lstrip()
      # work_table может быть подзапросом "(select ...)": вокруг него
      # обратные кавычки SQL невалидны, оборачиваем в derived table с алиасом
      if tbl.startswith('('):
        t_str=f'{tbl} as {t["alias"]}'
      elif re.match(r'^select\b', tbl, re.I):
        t_str=f'({tbl}) as {t["alias"]}'
      else:
        t_str='`'+t['table']+'` `'+t['alias']+'`'

    if need_add_table:
      TABLES.append(t_str)
      
      if not exists_arg('not_add_in_select_fields', t):
        desc = await form.db.desc(
          table = t['table'],
          errors = form.log
        )
        if desc:
            for db_field in desc.values():
              #adding_select_fields(form,db_field,t)
              adding_select_fields_in_desc(form,db_field,t)

  for f in form.fields:
    func=get_func(f)
    if func: form.query_search['SELECT_FIELDS'].append(func+' '+f['name'])
    elif exists_arg('expr',f):
      # Виртуальное поле: значение — SQL-выражение (напр. подзапрос к галерее),
      # а не колонка. Алиас как у обычной колонки: <tablename>__<name>.
      tbl=exists_arg('tablename',f) or 'wt'
      form.query_search['SELECT_FIELDS'].append(f"({f['expr']}) {tbl}__{f['name']}")
    
  form.query_search['TABLES']=TABLES