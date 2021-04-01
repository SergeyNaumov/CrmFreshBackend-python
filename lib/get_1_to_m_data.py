from lib.core import exists_arg
from lib.CRM.form.get_values_for_select_from_table import get_values_for_select_from_table
#from lib.CRM.form.run_event import run_event
import re

def normalize_value_row(form,field,d):
  for cf in field['fields']:
      c_name=cf['name']
      if exists_arg('filedir',cf):
        fdir=re.sub(r'^\.\/','/',cf['filedir'])
      d_cname=exists_arg(c_name,d) or ''
      
      if cf['type'] == 'file' and exists_arg(c_name,d):
        
        if d_cname:
          filesplit = d_cname.split(';')
          if len(filesplit)==2:
            d[c_name+'_filename']=filesplit[1]
          else:
            d[c_name+'_filename']=d_cname

      if exists_arg('slide_code',cf):
        d[c_name]=form.run_event('slide_code',{'field':cf,'data':d})







def get_1_to_m_data(form,f):
  #print('f:',f)
  if not exists_arg('fields',f): f['fields']=[]

  for cf in f['fields']:
      if cf['type'] == 'select_from_table':
          cf['values']=get_values_for_select_from_table(form,cf)

  headers=[]
  for c in f['fields']:
      
      if exists_arg('not_out_in_slide',c):
          continue

      headers.append(
        {
          'name':c['name'],
          'description': exists_arg('description',c),
          'type':c['type'],
          'change_in_slide':exists_arg('change_in_slide',c)
        }
      )

  f['headers']=headers
  f['values']=[]
  if form.id:
      where=exists_arg('where',f) or ''
      order = exists_arg('order',f) or ''
      
      if where: where+=' AND '
      where+=f['foreign_key']+'='+str(form.id)
      
      
      if exists_arg('sort',f): order=exists_arg('sort_field',f) or 'sort'
      

      #query=f'SELECT * from {f["table"]} {where} {order'
      data=form.db.get(
        table=f["table"],
        where=where,
        order=order,
        errors=form.errors,
        
        log=form.log,
      )

      #print('ONETOM_DATA:',data)
      
      #element_fields={}
      for d in data:
        normalize_value_row(form,f,d)
        f['values'].append(d)
  else:
    f['values']=[]


      
      











