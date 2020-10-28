from lib.core import is_wt_field, exists_arg
def get_values_for_select_from_table(form,f):
  print('get_values_for_select_from_table не готово')
  values=[]
  return values

def get_1_to_m_data(form,f):
  print('get_1_to_m_data не готова')

def get_in_ext_url(form,f):
  print('get_in_ext_url не готова')

def func_get_values(form):
    values={}

    if form.id:
      values=form.db.query(
        query=f'SELECT * from {form.work_table} WHERE {form.work_table_id}=%s',
        values=[form.id],
        onerow=1,
        debug=1,
        log=form.log
      )
      #print('GET_VALUES:',values)
      if not values:
          form.errors.append(f'В инструменте {form.title} запись с id: {form.id} не найдена. Редактирование невозможно')
          return

      for f in form.fields:
        if f['type']=='password':
          del values[f['name']]



    for f in form.fields:

      #if f['type'] in ['date','datetime','text','textarea']:



      name=f['name']
      #print(f)
      if is_wt_field(f):
        #if name=='checkbox':
          #print('not name checkbox:', (not name in values) )
          #print('not value checkbox:', (not values[name]) )
        # if name in values:
        #   print('before:',name,':',values[name])
        if not name in values or (not (values[name]) and values[name]!=0 and values[name]!='0'):
            values[name]=''
        else:
          values[name]=str(values[name])
          if f['type']=='datetime' and values[name]=='0000-00-00 00:00:00':
            values[name]=''

        # if name in values:
        #   print('after:',name,':',values[name])
      # else:
      #   print('not_wt_field:',f)
          
          

      
        #if not f['value']:
        #  f['value']=''

      if form.action not in ['insert','update'] and exists_arg('orig_type',f)=='select_from_table':
         f[values]=get_values_for_select_from_table(form,f)
      # #print('f:',f)
      if f['type'] == '1_to_m':
        get_1_to_m_data(form,f)

      if f['type']=='get_in_ext_url':
        get_in_ext_url(form,f)
        #values[name]=f['value']



      if name in values:
        if values[name].isnumeric():
          values[name]=str(values[name])
        f['value']=values[name]
      #else:
      #  print(f['name'],' - not numeric:', values[name])

      #values[name]=f['value']
      
    form.values=values
    #print('GET_VALUES2:',values)


