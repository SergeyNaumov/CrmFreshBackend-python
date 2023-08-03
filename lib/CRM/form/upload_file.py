from lib.resize import resize_one
from lib.core import exists_arg, get_ext, random_filename
from lib.save_base64_file import save_base64_file, b64_split

def upload_file(form):
    R=form.R
    name=exists_arg('name',R)
    field=None
    
    if name in form.fields_hash:
      field=form.fields_hash[name]
    else:
      return {'success':0,'errors':['name не указано или указано неверно']}

    if not name:
      form.errors.append('не указано name')
    
    value=exists_arg('value',R)
    if not value:
      return {'success':0,'errors':['не указано value']}


    orig_name=exists_arg('orig_name',value)
    if not orig_name:
      #form.errors.append('не указано orig_name')
      return {'success':0,'errors':['не указано orig_name']}
    else:
      ext = get_ext(orig_name)
      if not ext: 
        form.errors.append(f'не удалось определить расщирение. orig_name: {orig_name}')


    src=exists_arg('src',value)
    if not src:
      return {'success':0,'errors':['нет value.src']}

    
    if not form.success():
        return {'success':0,'errors':errors}
    
    filename_without_ext=random_filename()
    #print('filename_without_ext:',filename_without_ext)
    filename_for_out=filename_without_ext+'.'+ext
    crops=[]
    #print('FORM:',form.fields)
    if value:
      orig_name=value['orig_name']
      
      
      if 'crops' in value:
        crops=value['crops']
      
      #b64=b64_split(src)



      if src and not len(form.errors):
        save_base64_file(
          form=form,
          src=src,
          field=field,
          table=form.work_table,
          id=form.id,
          ext=ext,
          orig_name=orig_name,
          filename=filename_without_ext+'.'+ext
        )

    if form.success() and exists_arg('resize',field):
      if  exists_arg('crops',field) and len(crops):
        for r in field['resize']:
            width,height=r['size'].split("x")
            filename=r['file']
            filename=filename.replace('<%filename_without_ext%>',filename_without_ext)
            filename=filename.replace('<%ext%>',ext)
            for c in crops:
                save_base64_file(
                  form=form,
                  src=c['data'],
                  field=field,
                  filename=filename,
                  ext=ext
                )

                resize_one(
                    fr=field['filedir']+'/'+filename,
                    to=field['filedir']+'/'+filename,
                    width=width,
                    height=height,
                    grayscale=exists_arg('grayscale',field),
                    composite_file=exists_arg('composite_file',field),
                    quality=exists_arg('quality',field),
                )
      else: # ресайзим оригинальную фотографию
        for r in field['resize']:
            width,height=r['size'].split("x")
            filename=r['file']
            filename=filename.replace('<%filename_without_ext%>',filename_without_ext)
            filename=filename.replace('<%ext%>',ext)
            
            resize_one(
              fr=field['filedir']+'/'+filename_without_ext+'.'+ext,
              to=field['filedir']+'/'+filename,
              width=width,
              height=height,
              grayscale=exists_arg('grayscale',r),
              composite_file=exists_arg('composite_file',r),
              composite_gravity=exists_arg('composite_gravity',r),
              composite_resize=exists_arg('composite_resize',r),
              quality=exists_arg('quality',r),
            )






    return {
      'success':form.success(),
      'errors':form.errors,
      'value':filename_for_out
    }
