from lib.core import exists_arg

# Сохранение ЧПУ (таблица in_ext_url) для поля типа in_ext_url
async def save_in_ext_url(form,field,value):
  if not(field.get('in_url')):
    return

  in_url=field['in_url'].replace('<%id%>',str(form.id))
  if not in_url:
    return

  where=f'in_url="{in_url}"'
  data={
    'in_url':in_url,
    'ext_url':value
  }

  if exists_arg('foreign_key',field) and exists_arg('foreign_key_value',field):
    where+=f' AND {field["foreign_key"]}={field["foreign_key_value"]}'
    data[field['foreign_key']]=field['foreign_key_value']

  exists=await form.db.query(
    query=f'select * from in_ext_url where {where}',
    onerow=1
  )

  if exists and exists['ext_url']!=value and value:
    await form.db.save(
      table='in_ext_url',
      update=1,
      where=where,
      data=data,
      errors=form.errors
    )
  elif not(exists) and value:
    await form.db.save(
      table='in_ext_url',
      data=data,
      errors=form.errors
    )
