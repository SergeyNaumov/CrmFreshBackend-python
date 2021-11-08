from lib.core import get_child_field,exists_arg
from lib.get_1_to_m_data import get_1_to_m_data
def update_field(form,field,arg):
  R=form.R
  child_field_name=exists_arg('child_field_name',arg)

  if child_field_name:
    child_field=get_child_field(field,exists_arg('child_field_name',arg))
    print('child_field:',child_field)

    if not child_field:
      form.errors.append(f'Не найден элемент {arg["child_field_name"]} в элементе {arg["field_name"]}')
  else:
    form.errors.append('не указан параметр child_field_name. обратитесь к разработчику')

  if form.success():
    value=R['value']
    id=R['cur_id']

    regexp_rules=exists_arg('regexp_rules',child_field)
    if regexp_rules and len(regexp_rules):
        j=0
        while j < len(regexp_rules):
          regexp=regexp_rules[j]
          j+=2
      

  if form.success():
    form.db.query(
      query=f"""
        UPDATE
          {field["table"]}
        SET
          {child_field["name"]}=%s
        WHERE {field["table_id"]}=%s""",
      values=[value,id]

    )
    get_1_to_m_data(form,field)

  return {
    'success':1,
    'errors':form.errors,
    'values':field['values']
  }

