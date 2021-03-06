from lib.core import exists_arg
def process_result_list(form,R,result_list):
  # Обрабатывает результат, возвращает output
  if not result_list: result_list=[]
  output=[]
  memo_values={}
  multiconnect_values={}
  id_list=[]

  for r in result_list: id_list.append(r['wt__'+form.work_table_id])

  if len(id_list):
      for q in R['query']:
        name,values=q
        field=form.fields_hash[name]
        if field['type'] == 'multiconnect':
            multiconnect_arr=form.db.query(
              query="""
                SELECT
                    rst.{field['relation_save_table_id_worktable']} id,
                    group_concat(rt.{field['relation_table_header']} SEPARATOR ',') header
                FROM
                    {field['relation_save_table']} rst
                    join {field['relation_table']} rt ON (rt.{field['relation_table_id'] =rst.{field['relation_save_table_id_relation']})
                WHERE
                    rst.{field['relation_save_table_id_worktable']} IN ( {','.join(id_list)} )
                GROUP BY rst.{field['relation_save_table_id_worktable']
              """
            )
            for ma in multiconnect_arr: multiconnect_values[ma['id']]=ma['header']
  for r in result_list:
    
    data=[]
    for q in R['query']:
      name=q[0]

      field=form.fields_hash[name]
      type='html' #field['type']
      tbl = exists_arg('tablename',field) or 'wt'
      db_name=exists_arg('db_name',field) or name
      value=exists_arg(tbl+'__'+db_name,r)
      #print('r=>',r)
      #print(name,'=>',value)
      if not exists_arg('type_orig',type):
        field['type_orig']=field['type']

      if field['type_orig'] in ['filter_extend_select_values', 'select_values']:
          values_finded=0
          for v in field['values']:
            if v['v']==value:
              value,values_finded=v['d'],1

          if not values_finded:
            value='не выбрано'

      if not exists_arg('make_change_in_search',field) and exists_arg('filter_code',field) and not (isinstance(field['filter_code'],str)):
        value=field['filter_code'](str=str,value=value)
      else:
        if field['type']=='memo':
          type='memo'
        
        elif field['type']=='multiconnect':
          type='multiconnect'
          if exists_arg('wt__'+form.work_table_id,r):
            value=multiconnect_values[r['wt__'+form.work_table_id]]
          else: value=''

        elif field['type'].startswith('font'):
          type=field[type]

        elif field['type_orig'] in ['checkbox','switch']:
          if exists_arg('make_change_in_search',field):
            type=field['type']
          else:
            value=('нет','да')[value]

        elif field['type_orig'] in ['filter_extend_checbox','filter_extend_switch']:
          value=('нет','да')[value]

        elif field['type_orig'] in ['select_from_table','filter_extend_select_from_table']:
          if exists_arg('make_change_in_search',field):
            type='select'
            value=r[tbk+'__'+field['value_field']]
            if not exists_arg(name,form.SEARCH_RESULT['selects']):
                form.SEARCH_RESULT['selects'][name]=field['values']
          else:
            if field['db_name'].startswith('func:'):
              value = name
            elif r[tbl+'__'+field['header_field']]:
              value=r[tbl+'__'+field['header_field']]
            else:
              value=''
        elif field['type_orig'] in ['filter_extend_select_values','select_values']:
          if exists_arg('make_change_in_search',field):
            type='select'
            value=exists_arg(tbl+'__'+db_name,r)

            if not exists_arg(name,form.SEARCH_RESULT['selects']):
              form.SEARCH_RESULT['selects'][name]=field.values

        elif field['type_orig'] in ['text','textarea','filter_extend_text']:
          t='text' # или textarea ?
          type='text'
          value=exists_arg(tbl+'__'+db_name,r)

        elif field['type_orig'] == 'password':
          value='[пароль зашифрован]'

        elif field['type_orig']=='in_ext_url':
          value=exists_arg('in_ext_url__ext_url',r)

        elif field['type_orig']=='date' and exists_arg('make_change_in_search',field):
          type='date'
          #if exists_arg('make_change_in_search',field):

      if not value: value=''
      data.append({
          'name':name,
          'type':type,
          'value':value
      })
      
    output.append({'key':r['wt__'+form.work_table_id],'data':data})
  
  return output