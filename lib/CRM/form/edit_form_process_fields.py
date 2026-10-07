from lib.core import get_name_and_ext, exists_arg
from lib.resize import out_ext_for
import re
import os
async def edit_form_process_fields(form):

  for f in form.fields:
    # для новой формы очищаем поля
    #if form.action=='new' and exists_arg('value',f):
    #  f['value']=''
      
    if f['type']=='password':
      if 'enctypt_method' in f: del( f['enctypt_method'])
      if 'method_send' in f:
        for m in f['method_send']:
          del m['code']
    
    elif f['type']=='file' and exists_arg('value',f) and 'resize' in f:
      v=f['value']
      filename_without_ext, ext = get_name_and_ext(v)
      if ext:
        out_ext=out_ext_for(f, ext)
        for r in f['resize']:
          file=r['file']
          file=file.replace('<%filename_without_ext%>',filename_without_ext)
          file=file.replace('<%ext%>',out_ext)
          # Сырой путь './files/...' — для проверки существования (cwd = корень).
          raw=f['filedir']+'/'+file
          # Если миниатюры на диске нет (старые загрузки до появления resize)
          # — не подставляем битый путь, чтобы фронт откатился на оригинал.
          if os.path.isfile(raw):
            r['loaded']=re.sub(r'^\.\/','/',raw)
          else:
            r['loaded']=''
    
    elif f['type']=='code' and exists_arg('code',f):
      f['code'](form,f)
      
