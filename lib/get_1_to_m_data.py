from lib.core import exists_arg
from lib.CRM.form.get_values_for_select_from_table import get_values_for_select_from_table
#from lib.CRM.form.run_event import run_event
import re

def normalize_value_row(form,field,d):
  for cf in field['fields']:
      c_name=cf['name']
      filedir=''
      if exists_arg('filedir',cf):
        filedir=cf['filedir']
        fdir=re.sub(r'^\.\/','/',cf['filedir'])
      d_cname=exists_arg(c_name,d) or ''
      
      if cf['type'] == 'file' and exists_arg(c_name,d):
          
        if d_cname:
          filename=''
          filesplit = d_cname.split(';')
          if len(filesplit)==2:
            filename=filesplit[1]
          else:
            filename=d_cname
          

          if filedir and filename:  # для превью на фронте
            print('filedir: ',filedir)
            resize_for_preview=None
            if exists_arg('preview',cf) and exists_arg('resize',cf) and len(cf['resize'])>0:
              for r in cf['resize']:
                 if r['size']==cf['preview']:
                    resize_for_preview=r
              
              if resize_for_preview:
                name,ext=filename.split('.')
                tmp_file=r['file'].replace('<%filename_without_ext%>',name).replace('<%ext%>',ext)
                d['preview_img']=fdir+'/'+tmp_file  

            else:
              d['preview_img']=fdir+'/'+filename             
               
          d[c_name+'_filename']=filename
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
        #print('D:',d)
        
        normalize_value_row(form,f,d)
        f['values'].append(d)
  else:
    f['values']=[]


      
      











