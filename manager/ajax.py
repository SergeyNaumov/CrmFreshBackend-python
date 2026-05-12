async def name(form,v):
  value=v['name']
  if not ('name_f' in v): v['name_f']=''
  if not ('name_i' in v): v['name_i']=''
  if not ('name_o' in v): v['name_i']=''

  if v['name_f'] and v['name_i'] :
    value=v['name_f']+' '+v['name_i']+' '+v['name_o']

  return [
    'name',{'value': value },

  ]

async def login(form,v):
  error=''

  where=[]
  if form.id:
    where.append(f'{form.work_table_id}<>{form.id}')

  where.append(f'login=%s')
  
  exists=await form.db.getrow(
    table='manager',
    where=(' and '.join(where)),
    debug=1,
    values=[v['login']]
  )

  if exists:
    error='такой логин уже существует'


  return ['login',{'error':error}]


async def phone(form, v):
  error = ''
  where = []
  if form.id:
    where.append(f'{form.work_table_id}<>{form.id}')

  where.append(f'phone=%s')

  if v['phone']:
    exists = await form.db.getrow(
      table='manager',
      where=(' and '.join(where)),
      values=[v['phone']]
    )
    if exists:
      error = 'такой номер телефона уже существует'

  return ['phone', {'error': error}]

ajax={
  'name':name,
  'login':login,
  'phone':phone
}