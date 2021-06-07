from lib.core import exists_arg
def process_result_list(form,R,result_list):
  # Обрабатывает результат, возвращает output
  if not result_list: result_list=[]
  output=[]
  memo_values={}
  multiconnect_values={}
  id_list=[]


  for r in result_list:
    id_fields=form.work_table_id.split(',')
    for idf in id_fields:
      if 'wt__'+idf in r:
        id_list.append(r['wt__'+idf])
      else:
        form.errors.append(f'Ошибка: поле "{idf}"" отсутствует в основной таблице но упомянуто в work_table_id')

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
            if multiconnect_arr:
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
            if str(v['v'])==str(value):
              value,values_finded=v['d'],1

          if not values_finded:
            value='не выбрано'

      if not exists_arg('make_change_in_search',field) and exists_arg('filter_code',field) and not (isinstance(field['filter_code'],str)):
        value=field['filter_code'](form=form,field=field,row=r)
        
      else:
        if field['type']=='memo':
          type='memo'
        
        elif field['type']=='multiconnect':
          type='multiconnect'
          if exists_arg(r['wt__'+form.work_table_id],multiconnect_values):
            #print('ARG:',exists_arg('wt__'+form.work_table_id,r))
            #print('multiconnect_values:',multiconnect_values)
            value=multiconnect_values[r['wt__'+form.work_table_id]]
          else: value=''

        elif field['type'].startswith('font'):
          type=field[type]

        elif field['type_orig'] in ['checkbox','switch']:
          if exists_arg('make_change_in_search',field):
            type=field['type']
          else:
            value='да' if value else 'нет'

        elif field['type_orig'] in ['filter_extend_checbox','filter_extend_switch']:
          value=('нет','да')[value]

        elif field['type_orig'] in ['select_from_table','filter_extend_select_from_table']:
          if exists_arg('make_change_in_search',field):
            type='select'
            value=r[tbk+'__'+field['value_field']]
            if not exists_arg(name,form.SEARCH_RESULT['selects']):
                form.SEARCH_RESULT['selects'][name]=field['values']
          else:
            if not('db_name' in field): field['db_name']=field['name']

            if field['db_name'].startswith('func:'):
              value = name
            elif exists_arg(tbl+'__'+field['header_field'],r) and r[tbl+'__'+field['header_field']]:
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
        elif field['type_orig'] == 'datetime':
          value=str(value)
        elif field['type_orig']=='date':
          value=str(value)
          if exists_arg('make_change_in_search',field):
            type='date'
          
      if not exists_arg('make_change_in_search',field):
        type='html'

      #print('name:',field['name'],' type:',type)

      if not value: value=''
      data.append({
          'name':name,
          'type':type,
          'value':value
      })

    # все эти заморочки для структур с составнам work_table_id,
    # например form.work_table_id='ur_lico_id,action_id'
    work_table_id_fields=form.work_table_id.split(',')
    key_list=[]
    values_list=[]
    for fld in work_table_id_fields:
      key_list.append('wt__'+fld)
      if 'wt__'+fld in r:
        values_list.append(str(r['wt__'+fld]))
      

    id_field=','.join(key_list)
    id_value=','.join(values_list)
    #print('id_field:',id_field,'id_value:',values_list)
    output.append({'key':id_value,'data':data})

    #output.append({'key':r['wt__'+form.work_table_id],'data':data})
  
  return output