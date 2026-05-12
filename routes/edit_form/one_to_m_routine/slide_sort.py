from lib.core import exists_arg
async def slide_sort(form,field):
    sort_hash=exists_arg('sort_hash',form.R)

    if not exists_arg('sort',field):
      form.errors.append('сортировка запрещена')
    
    if not sort_hash:
      form.errors.append('отсутствует sort_hash')

    if form.success():
      sort_field=exists_arg('sort_field',field) or 'sort'
      when_list=''
      for id in sort_hash.keys():
        id=str(id)
        sort_hash[id]=str(sort_hash[id])
        if id.isnumeric() and sort_hash[id].isnumeric():
          when_list+=f"""WHEN {field["table_id"]}={id} THEN "{sort_hash[id]}"\n"""

      query=f"""
        UPDATE {field['table']}
          SET {sort_field}=(
            CASE
              {when_list}
            END
          )
        WHERE {field['foreign_key']}={form.id}
      """

      await form.db.query(
        query=query,
        errors=form.errors
      )
      await form.run_event('after_slide_sort')

    return {'success':form.success(),'errors':form.errors}