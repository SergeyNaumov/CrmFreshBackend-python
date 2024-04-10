from lib.core import is_wt_field, exists_arg, tree_to_list
from lib.get_1_to_m_data import get_1_to_m_data
from .get_values_for_select_from_table import get_values_for_select_from_table


def get_in_ext_url(form,f):
  print('get_in_ext_url не готова')

def func_get_values(form):

    values={}
    if(hasattr(form,'values')):
      values=form.values
    

    if form.id:
      values=form.db.getrow(
        table=form.work_table,
        where=f'{form.work_table_id}=%s',
        values=[form.id],
        log=form.log
      )
      if not values:
        form.errors.append(f'Запись {form.id} не найдена')
        return
      for v in values:
        # Декодирую bites (такое счастье было в трейде)
        if(type(values[v]) is bytes):
          values[v]=values[v].decode('utf-8')
        # перевожу в строку (чтобы не гадать с типами для select-ов)
        if values[v] or values[v]==0:
          values[v]=str(values[v])
        else: values[v]=''

      if not values:
          form.errors.append(f'В инструменте {form.title} запись с id: {form.id} не найдена. Редактирование невозможно')
          return

      for f in form.fields:
        if f['type']=='password':
          del values[f['name']]

    tables_1_to_1={}
    for f in form.fields:
      if not( 'name' in f ):
        break

      if form.action=='new':
        f['value']=''
      if 'name' in f: name=f['name']
      
      
      if is_wt_field(f):
        #if name=='checkbox':
          #print('not name checkbox:', (not name in values) )
          #print('not value checkbox:', (not values[name]) )
        # if name in values:
        
        if not name in values or (not (values[name]) and values[name]!=0 and values[name]!='0'):
            values[name]=''
        else:
          values[name]=str(values[name])
          if f['type']=='datetime' and values[name]=='0000-00-00 00:00:00':
            values[name]=''    
      
      set_from_nv=True
      if form.script=='edit_form' and (form.action in ('new')) and ('value' in f ):
        #print('f:',f)
        set_from_nv=False
      
      #form.pre(f"{name}: {set_from_nv} ; value in f: {('value' in f)}")
      if form.action not in ['insert','update'] and (
          exists_arg('orig_type',f) in ['select_from_table','filter_extend_select_from_table']
          or
          f['type'] in ['select_from_table','filter_extend_select_from_table']
        ):

          if set_from_nv:  f['value']=exists_arg(f['name'],values);
          if not exists_arg('values',f) or not len(f['values']):
            f['values']=get_values_for_select_from_table(form,f)
            
      if f['type'] == '1_to_m':
        get_1_to_m_data(form,f)


      # Если это 1_to_1
      if f['type'].startswith('1_to_1_'):
        T=f['type'].replace('1_to_1_','')

        if not('db_name' in f):
          f['db_name']=f.get('name')

        # Проверки
        if not( f.get('save_table') ):
          form.errors.append(f"в поле {f.get('description')} - {f.get('name')} отсутствует атрибут save_table")
          break

        if not( f.get('foreign_key') ):
          form.errors.append(f"в поле {f.get('description')} - {f.get('name')} отсутствует атрибут foreign_key")
          break

        table=f.get('save_table')
        if form.id:
          if not(table in tables_1_to_1):
            tables_1_to_1[table]={
              'foreign_key': f['foreign_key'],
              'values':form.db.query(
                query=f"select * from {f.get('save_table')} WHERE {f.get('foreign_key')}={form.id}",
                onerow=1
              )
            }

          cur_values=tables_1_to_1[table]['values']
          if cur_values and f['db_name'] in cur_values:
            f['value']=cur_values[f['db_name']]
        else:
          f['value']=''


      if f['type']=='get_in_ext_url':
        get_in_ext_url(form,f)
        #values[name]=f['value']


      if name in values:
          if values[name].isnumeric():
            values[name]=str(values[name])
          if set_from_nv and not(form.script == 'admin_table' and ('value' in f)):
            f['value']=values[name]         
      
    #form.pre(f"v2: {form.fields[5]['value']}")
    form.values=values


# Получаем значения для select_from_table, 1_to_m
def func_get_fields_values(form):
  form.set_orig_types()
  for f in form.fields:
    if f['type'] == '1_to_m':
      get_1_to_m_data(form,f)

    elif f['type']=='get_in_ext_url':
      get_in_ext_url(form,f)
    elif exists_arg('orig_type',f) in ['select_from_table','filter_extend_select_from_table']:

      f['values']=get_values_for_select_from_table(form,f)
      
