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
        str=1,
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
      #print('f:',f)
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


          
          

      
        #if not f['value']:
        #  f['value']=''

      if form.action not in ['insert','update'] and (
          exists_arg('orig_type',f) in ['select_from_table','filter_extend_select_from_table']
          or
          f['type'] in ['select_from_table','filter_extend_select_from_table']
        ):
          f['value']=exists_arg(f['name'],values);
          if not exists_arg('values',f) or not len(f['values']):
            f['values']=get_values_for_select_from_table(form,f)
            
      if f['type'] == '1_to_m':

        get_1_to_m_data(form,f)

      if f['type']=='get_in_ext_url':
        get_in_ext_url(form,f)
        #values[name]=f['value']


      if name in values:
        if values[name].isnumeric():
          values[name]=str(values[name])
        f['value']=values[name]

      # if 'before_code' in f:
      #   f['before_code'](form=form,field=f)  


          

      
    form.values=values
    #print('GET_VALUES2:',values)


