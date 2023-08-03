def header_before_code(form,field):

    if form.script in ('find_objects','admin_table'):

        field={
            'name':'id',
            'description':'Название',
            'type':'select_from_table',
            'table':'action',
            'header_field':'header',
            'value_field':'id',
            'where':'date_stop>=curdate()',
            'filter_code':header_filter_code,
            'read_only':1,
            'filter_on':1,
        # При выводе фильтров и при поиска превращаем данное текстовое поле в autocomplete
        #'before_code':header_before_code
        }

        # field['values']=form.db.query(
        #     query='select id v,header d from action where date_stop>=curdate()'
        # )

        return field

def header_filter_code(form,field,row):
  return f'<a href="/edit-form/action/{row["wt__id"]}" target="_blank">{row["wt__header"]}</a>'
        
