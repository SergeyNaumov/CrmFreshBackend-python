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

events={
  'links':{
    'before_code':links_before_code
  },
  'firm_c':{
    'before_code':firm_c_before_code
  },
  'manager_id_c':{
    'before_code': manager_id_c_before_code
  }
}