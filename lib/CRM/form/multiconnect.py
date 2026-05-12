async def get_values(form,field):
  if form.id:

    if field.get('subtype')=='table':
      select_fields=f'{field["relation_save_table_id_relation"]} as id'
      if not('fields' in field):
        form.errors=f'Не указано fields для multiconnect с subtype=table {field["name"]}'
        return []

      for f in field['fields']:
        select_fields+=f", {f['name']}"

        return await form.db.query(
          query=f"""
            SELECT
              {select_fields}
            FROM
              {field["relation_save_table"]}
            WHERE
              {field["relation_save_table_id_worktable"]}=%s
          """,

          values=[form.id],
          errors=form.errors
        )
    else:
      select_fields=field["relation_save_table_id_relation"]

      res = await form.db.query(
        query=f"""
          SELECT
            {select_fields}
          FROM
            {field["relation_save_table"]}
          WHERE
            {field["relation_save_table_id_worktable"]}=%s
        """,
        massive=1,
        values=[form.id],
        errors=form.errors
      )
    return res
  else:
    return []



async def save(form,field,new_values):
  old_values = await get_values(form,field)
  old_values_hash={} ; db=form.db
  if field.get('subtype')=='table':

      ids=[str(x['id']) for x in new_values]

      if len(ids):
        values_joined=','.join(ids)
        add_where=''
        if values_joined:
          add_where=f' AND {field["relation_save_table_id_relation"]} not in ({values_joined})'

        await db.query(
          query=f"DELETE FROM {field['relation_save_table']} WHERE {field['relation_save_table_id_worktable']}=%s {add_where}",
          values=[form.id],
        )

        exists_ids=[x for x in await db.query(
          query=f"""
            SELECT
              {field["relation_save_table_id_relation"]}
            FROM
              {field['relation_save_table']}
            WHERE
              {field['relation_save_table_id_worktable']}=%s
              AND {field["relation_save_table_id_relation"]} in ({values_joined})
          """,
          values=[form.id],
          massive=1
        )]
        for item in new_values:
          update=0
          where=''
          if item['id'] in exists_ids:
            update=1
            where=f"{field['relation_save_table_id_worktable']}={form.id} and {field['relation_save_table_id_relation']}={item['id']}"


          data={
            field['relation_save_table_id_worktable']:form.id,
            field['relation_save_table_id_relation']:item['id']
          }

          for f in field['fields']:
            data[f['name']]=item[f['name']]

          if len(data):
            await db.save(
              table=field['relation_save_table'],
              update=update,
              data=data,
              #debug=1,
              errors=form.errors,
              where=where,
            )



  else:
      new_values=[str(x) for x in new_values]
      for ov in old_values:
        old_values_hash[ov]=1

      values_joined=','.join(new_values)
      add_where=''
      if values_joined:
        add_where=f' AND {field["relation_save_table_id_relation"]} not in ({values_joined})'



      await db.query(
        query=f"""
          DELETE
          FROM
            {field['relation_save_table']}
          WHERE
            {field['relation_save_table_id_worktable']}=%s {add_where}
        """,
        debug=1,
        errors=form.errors,
        values=[form.id]
      )

      # сохраняем то, чего ещё нет
      for v in new_values:
        if not v in old_values_hash:
          await db.save(
            table=field['relation_save_table'],
            ignore=1,
            #debug=1,
            data={
              field['relation_save_table_id_worktable']:form.id,
              field['relation_save_table_id_relation']:v
            }
          )

  if not len(form.errors):
    await form.run_event('after_save_multiconnect')
