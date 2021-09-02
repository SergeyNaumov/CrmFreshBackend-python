from lib.core import exists_arg, get_func, from_datetime_get_date
import re
import shlex
def get_search_where(form,query):
  WHERE,headers=[],[]
  VALUES=[]

  form.SEARCH_RESULT['query_fields']=[]
  #print('get_search_where - доделать')
  if not len(query):
    if isinstance(form.default_find_filter,str):
      form.default_find_filter=[form.default_find_filter.split(',')]

    for name in form.default_find_filter:
        if name in form.fields_hash:
          f=form.fields_hash[name]
          form.SEARCH_RESULT['query_fields'].append(f)
          query.append([name,''])
  for f in form.fields:
    form.fields_hash[f['name']]=f
    
  for q in query:
      name,values=q
      
      if not name in form.fields_hash:
        continue
      
      f=form.fields_hash[name]

      form.query_hash[name]=values

      form.SEARCH_RESULT['query_fields'].append(f)
      description=exists_arg('description',f) or ''
      
      header={
        'h':description,
        'n':name,
        'make_sort': not(form.not_order)
      }

      if len(form.priority_sort) and form.priority_sort[0] == name:
        header['sorted']=form.priority_sort[1]

      form.SEARCH_RESULT['headers'].append(header)

      if exists_arg('not_process',f):
          continue



      db_name=exists_arg('db_name',f) or name
      table=exists_arg('tablename',f) or 'wt'
      #if f['type'] == 'multiconnect':

      if f['type'] not in ['1_to_m','memo'] and not exists_arg('not_order',f):
          o,operable_fld='',''
          #print('F:',f)
          if f['type'] in ['date','datetime','filter_extend_date','filter_extend_datetime']:
              operable_fld=table+'.'+db_name
              o=operable_fld+" desc"


          elif f['type'] in ['select_from_table','filter_extend_select_from_table']:
              func=get_func(f)
              if func:
                operable_fld=func
              else:
                operable_fld=table+'.'+f['header_field']
              o=operable_fld

          elif f['type']=='in_ext_url':
              operable_fld='in_ext_url.ext_url'
              o=operable_fld

          else:
              func=get_func(f)
              if func :
                operable_fld=func
              else:
                operable_fld=table+'.'+db_name

              o=operable_fld

          if len(form.priority_sort):
              if form.priority_sort[0] == name:
                  desc_value=('','desc')[form.priority_sort[1] == 'desc']
                  form.query_search['ORDER'].append(operable_fld+' '+desc_value)
          # else:
          #     form.query_search['ORDER'].append(o)

      if not values or (isinstance(values,list) and not len(values)):
          continue

      if exists_arg('filter_type',f)=='range':

        min,max=values
        if min:
          WHERE.append('('+db_name+' >= %s)')
          VALUES.append(min)

        if max:
          WHERE.append('('+db_name+' <= %s)')
          VALUES.append(max)

      elif f['type'] in ('text','textarea','email','filter_extend_text'):

        v=values
        if v:
          # form.db.connect.escape_string(v)
          v='%'+str(v)+'%'
          #v="'"+v+"'"
          func=get_func(f)
          if func:
            WHERE.append('('+dn_name+' LIKE %s)')
          else:
            WHERE.append('('+table+'.'+db_name+' LIKE %s)')
          VALUES.append(v)
          #print('WHERE:',WHERE)

      elif (f['type'] in ['date','datetime','filter_extend_date','filter_extend_datetime'] and not(exists_arg('filter_type',f))) or exists_arg('filter_type',f)=='range' :

          min,max=values
          min_date=from_datetime_get_date(min)
          
          if min_date:
            min_date=min_date+' 00:00:00'
            WHERE.append('('+table+'.'+db_name+'>=%s)')
            VALUES.append(min_date)

          max_date=from_datetime_get_date(max)
          if max_date:
            max_date=max_date+' 23:59:59'
            WHERE.append('('+table+'.'+db_name+'<=%s)')
            VALUES.append(max_date)          

      elif f['type']=='memo':
        v=values[0]
        date_low=from_datetime_get_date(v['registered_low'])

        if date_low:
            date_low=date_low+' 00:00:00'
            WHERE.append(f['memo_table_alias']+'.'+f['memo_table_registered']+' >= %s')
            VALUES.append(date_low)
        
        date_hi=from_datetime_get_date(v['registered_hi'])
        if date_hi:
            date_hi=date_hi+' 23:59:59'
            WHERE.append(f['memo_table_alias']+'.'+f['memo_table_registered']+' <= %s')
            VALUES.append(date_hi)

        m=exists_arg('message',v)
        if m:
          m='%'+m+'%' #escape!
          WHERE.append('('+f['memo_table_alias']+'.'+f['memo_table_comment']+' LIKE %s)')
          VALUES.append(m)
        
        user_id = exists_arg('user_id',v)
        if user_id:

          WHERE.append('('+f['memo_table_alias']+'.'+f['memo_table_auth_id']+' IN ('+','.join(user_id)+') )')
      elif f['type'] in ['checkbox','filter_extend_checkbox']:
        if type(values) is list:
          map_rezult=[]
          for v in values:
            if (type(v) is int) or (type(values) is str):
              if type(v) is int: v=str(v)
              if v.isnumeric():
                map_rezult.append(v)
          
          if len(map_rezult):
            if f['type']=='filter_extend_checkbox':
              WHERE.append(' ('+table+'.'+db_name+' IN ('+','.join(map_rezult)+'))')
            else:
              WHERE.append(' (wt.'+db_name+' IN ('+','.join(map_rezult)+'))')

      elif f['type'] in ['select_from_table','filter_extend_select_from_table','filter_extend_select_values','select_values']:
        if type(values) is int or type(values)=='str':
          values=[values]
        if type(values) is list:
          map_rezult=[]
          for v in values:
            if type(v) is int: v=str(v)
            if v.isnumeric():
              map_rezult.append(v)

          if len(map_rezult):
            if f['type']=='filter_extend_select_from_table':
              

              WHERE.append(' ('+table+'.'+db_name+' IN ('+','.join(map_rezult)+'))')
            else:
              
              WHERE.append(' (wt.'+db_name+' IN ('+','.join(map_rezult)+'))')

      elif f['type'] == 'multiconnect':
        if not exists_arg('tablename',f):
          form.errors.append('не указано tablename для '+f['name'])
        else:
          # my @values = grep /^\d+$/, @{$values};
          if len(values):
            WHERE.append('('+f['tablename']+'.'+f['relation_table_id']+' IN ('+','.join(values)+')')
      elif f['type']=='file':
          if values==1: # файл существует
            WHERE.append(f'''(wt.{f['name']}<>"") ''')
          elif values==2: # файл отсутствует
            WHERE.append(f'''(wt.{f['name']}="") ''')


          

      else:
        map_rezult=[]
        for v in values:
          if v and type(v)=='str':
            if v.isnumeric():
              map_rezult.append(v)

        if len(map_rezult):
          WHERE.append(' ('+table+'.'+db_name+' IN ('+','.join(map_rezult)+'))')
  #print('WHERE:',WHERE)
  form.query_search['WHERE']=WHERE
  form.query_search['VALUES']=VALUES
