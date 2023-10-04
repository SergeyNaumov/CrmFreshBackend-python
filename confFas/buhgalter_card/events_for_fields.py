def links_before_code(form,field):
  if form.ov:
    field['after_html']=f'''<a href="/edit_form/user/{form.id}" target="_blank">Карта ОП: {form.ov['firm']}</a>'''


def firm_c_before_code(form,field):
  #form.pre(form.ov)
  if form.ov: field['after_html']=form.ov['firm']

def manager_id_c_before_code(form,field):
  if form.ov: 
    field['after_html']=f"{form.ov['m__name']}<br><small>Группа: {form.ov['m__name']}</small>"

# def firm_c_before_code(form,field):
#   if form.ov: field['after_html']=form.ov['mg__header']

def requisits_after_save(form,field,data=None):

    #exists_main=form.db.query(
    #    query=f"select main from {field['table']} where {field['foreign_key']}=%s",
    #    values=[form.id],
    #    onevalue=1
    #)
    print('field:',field)
    print('VALUES:',field['values'])

    
    data=field['values']
          #print('cur_item:',cur_item)
    if data and len(data)==1:
          d=data[0]
          if d['main']==1:
              form.db.query(
                  query=f"UPDATE {field['table']} SET main=0 where {field['foreign_key']}={form.id} and id<>{d['id']}",
                  values=[],
                  debug=1
              )



events={
  'links':{
    'before_code':links_before_code
  },
  'firm_c':{
    'before_code':firm_c_before_code
  },
  'manager_id_c':{
    'before_code': manager_id_c_before_code
  },
  'requisits':{
    'after_save_code':requisits_after_save
  }
}