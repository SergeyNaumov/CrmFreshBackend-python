from lib.core import exists_arg
from lib.all_configs import read_config
from lib.CRM.form.multiconnect import get_values


def get_tag_id(form,header):
    return form.db.query(
      query=f'SELECT {field["relation_table_id"]} FROM {field["relation_table"]} WHERE {field["relation_table_header"]}=%s',
      values=[R['header']],
      debug=1,
      onevalue=1,
      errors=form.errors
    )

def check_defaults(form,field):

  defaults={
    'relation_table_id':'id',
    'relation_save_table_header':'header',
    'relation_tree_order':'header',
    'relation_save_table_id_worktable':form.work_table+'_id',
    'relation_save_table_id_relation':field['relation_table']+'_id'
  }
  
  for k in defaults.keys():
    if not k in field: field[k]=defaults[k]



def get(form,field):
  where=exists_arg('relation_table_where',field)
  if not where: where=''
  select_fields=''
  if exists_arg('tree_use',field):
    #if where: where+=' AND '
    #where+='parent_id is null'
    select_fields=f'{field["relation_table_id"]} id, {field["relation_save_table_header"]} header, parent_id'

    # В элементе v-treeview нет возможности задизейблить весь элемент, поэтому для каждой галочки добавляем read_only:
    if form.read_only or exists_arg('read_only',field):
      select_fields+=',1 read_only'
  else:
    select_fields=f'{field["relation_table_id"]} id, {field["relation_table_header"]} header'

  _list=[]
  
  if 'query' in field and field['query']:
    #print('USE QUERY')
    _list=form.db.query(
      query=field['query']
    )
  else:
    
    _list=form.db.get(
      select_fields=select_fields,
      table=field["relation_table"],
      where=where,
      #debug=1,
      order=exists_arg('relation_tree_order',field),
      tree_use=exists_arg('tree_use',field),
      errors=form.errors
    )
  value=get_values(form,field)
  #print(_list)
  return _list,value

def multiconnect_process(**arg):
  R={}
  action=''
  id=''
  field_name=''

  if 'R' in arg: R=arg['R']
  if 'action' in R: action=R['action']
  if 'id' in R: id=R['id']
  if 'field_name' in arg: field_name=arg['field_name']
  
  #print('R:',R)
  form=read_config(
    script='multiconnect',
    config=arg['config'],
    action=action,
    id=id
  )

  if field_name in form.fields_hash:
    field=form.fields_hash[field_name]
    check_defaults(form,field);
  else:
    form.errors.append(f'multiconnect: поле с именем {field_name} не найдено')

  if action == 'add_tag' and 'header' in R:
      tag_id=None
      if not R['header']:
        form.errors.append('новый тэг не указан')
      if form.success():
        tag_id=get_tag_id(form,R['header'])

      if not tag_id and form.success():
        tag_id=form.db.save(
          table=field["relation_table"],
          data={
            field['relation_table_header']:R['header']
          }
        )
      return {
        'success':form.success(),
        'tag_id':tag_id,
        'errors':form.errors,
        'log':form.log
      }
  elif action == 'autocomplete':
      _list=form.db.query(
          query=f'SELECT {field["relation_table_id"]} v, {field["relation_table_header"]} d FROM {field["relation_table"]} WHERE {field["relation_table_header"]} like %s',
          values=['%'+R["header"]+'%'],
          errors=form.errors
      )
      exists_tag=get_tag_id(form,R["header"])
      return {
        'success':form.success,
        'list':_list,
        'exists_arg':exists_tag,
        'errors':form.errors,
        'log':form.log
      }
  elif action == 'get':
    (_list,value) = get(form,field)
    return {
        'success':form.success(),
        'list':_list,
        'value':value,
        'errors':form.errors,
        'log':form.log
    }

  return {'success':'ready'}