def name(form,v):
  value=v['name']
  if not ('name_f' in v): v['name_f']=''
  if not ('name_i' in v): v['name_i']=''
  if not ('name_o' in v): v['name_i']=''

  if v['name_f'] and v['name_i'] :
    value=v['name_f']+' '+v['name_i']+' '+v['name_o']

  return [
    'name',{'value': value },

  ]

def login(form,v):
  error=''

  where=[]
  if form.id:
    where.append(f'{form.work_table_id}<>{form.id}')

  where.append(f'login=%s')
  
  exists=form.db.getrow(
    table='manager',
    where=(' and '.join(where)),
    values=[v['login']]
  )

  if exists:
    error='такой логин уже существует'


  return ['login',{'error':error}]


ajax={
  'name':name,
  'login':login
}