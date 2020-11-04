from lib.core import get_name_and_ext, exists_arg
def edit_form_process_fields(form):
  for f in form.edit_form_fields:
    if f['type']=='password':
      if 'enctypt_method' in f: del( f['enctypt_method'])
      if 'method_send' in f:
        for m in f['method_send']:
          del m['code']
    elif f['type']=='file' and exists_arg('value',f) and 'resize' in f:
      v=f['value']
      filename_without_ext, ext = get_name_and_ext(v)
      if ext:
        for r in f['resize']:
          file=r['file']
          file=file.replace('<%filename_without_ext%>',filename_without_ext)
          file=file.replace('<%ext%>',ext)
          r['loaded']=f['filedir']+'/'+file
          r['loaded']=re.sub(r'^\.\/','/',r['loaded'])
          
      
