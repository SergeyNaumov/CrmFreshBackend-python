def get_values(form,field):
  if form.id:
    select_fields=field["relation_save_table_id_relation"]
    #print(field);
    #if form.read_only or ('read_only' in field and field['read_only']):
    #  select_fields+=', 1 read_only '
    #print('select_fields:',select_fields)
    res=form.db.query(
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
      errors=form.id
    )
    
    return res
  else:
    return []

def save(form,field,new_values):
  old_values=get_values(form,field)
  old_values_hash={}
  print('NEW_VALUES:',new_values)
  for ov in old_values:
    old_values_hash[ov]=1
  
  values_joined=','.join(new_values)
  add_where=''
  if values_joined:
    add_where=f' AND {field["relation_save_table_id_relation"]} not in ({values_joined})'
  
  form.db.query(
    query=f"""
      DELETE
      FROM
        {field['relation_save_table']}
      WHERE
        {field['relation_save_table_id_worktable']}=%s {add_where}
    """,
    errors=form.errors,
    values=[form.id]
  )

  # сохраняем то, чего ещё нет
  for v in new_values:
    if not v in old_values_hash:
      form.db.save(
        table=field['relation_save_table'],
        ignore=1,
        #debug=1,
        data={
          field['relation_save_table_id_worktable']:form.id,
          field['relation_save_table_id_relation']:v
        }
      )
