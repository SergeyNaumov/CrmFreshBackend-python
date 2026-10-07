import os
from lib.resize import resize_one, convert_to_webp, out_ext_for, is_raster_ext
from lib.core import exists_arg, get_ext, random_filename
from lib.save_base64_file import save_base64_file, b64_split
from pathlib import Path

async def upload_file(form):
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
      # Создаём filedir если его нет
      Path(field['filedir']).mkdir(parents=True, exist_ok=True)
      orig_name=value['orig_name']
      
      
      if 'crops' in value:
        crops=value['crops']
      
      #b64=b64_split(src)



      if src and not len(form.errors):
        await save_base64_file(
          form=form,
          src=src,
          field=field,
          table=form.work_table,
          id=form.id,
          ext=ext,
          orig_name=orig_name,
          filename=filename_without_ext+'.'+ext
        )

      # to_webp: конвертируем основной файл в webp и обновляем имя в БД
      if form.success() and exists_arg('to_webp',field) and is_raster_ext(ext) and ext.lower()!='webp':
        old_path=field['filedir']+'/'+filename_without_ext+'.'+ext
        new_path=field['filedir']+'/'+filename_without_ext+'.webp'
        if convert_to_webp(old_path, new_path, quality=exists_arg('base_quality',field) or 85):
          if os.path.isfile(old_path):
            os.remove(old_path)
          ext='webp'
          filename_for_out=filename_without_ext+'.webp'
          db_value=filename_for_out
          if exists_arg('keep_orig_filename',field):
            db_value=filename_for_out+';'+orig_name
          await form.db.query(
            query=f'UPDATE {form.work_table} SET {field["name"]}=%s WHERE {form.work_table_id}=%s',
            errors=form.errors,
            values=[db_value, form.id],
          )

    if form.success() and exists_arg('resize',field):
      out_ext=out_ext_for(field, ext)
      if  exists_arg('crops',field) and len(crops):
        # Ручная обрезка: кроп i соответствует resize[i] (порядок задаёт
        # фронт, file.vue init()). Кроп — dataURL canvas, сохраняем его как
        # миниатюру и доводим до точного размера. save_base64_file зовём с
        # filedir/orig_filename -> ветка «только на диск», без UPDATE БД.
        for i,r in enumerate(field['resize']):
            width,height=str(r['size']).split("x")
            filename=r['file']
            filename=filename.replace('<%filename_without_ext%>',filename_without_ext)
            filename=filename.replace('<%ext%>',out_ext)
            crop_data=crops[i].get('data') if i < len(crops) else None
            if crop_data:
              await save_base64_file(
                form=form,
                src=crop_data,
                field=field,
                filedir=field['filedir'],
                orig_filename=filename,
                filename=filename,
                ext=out_ext
              )
              src_file=field['filedir']+'/'+filename
            else: # кроп не подтверждён — ресайзим оригинал
              src_file=field['filedir']+'/'+filename_without_ext+'.'+ext

            resize_one(
                fr=src_file,
                to=field['filedir']+'/'+filename,
                width=width,
                height=height,
                grayscale=exists_arg('grayscale',r),
                composite_file=exists_arg('composite_file',r),
                composite_gravity=exists_arg('composite_gravity',r),
                composite_resize=exists_arg('composite_resize',r),
                quality=exists_arg('quality',r),
                to_webp=exists_arg('to_webp',field),
            )
      else: # ресайзим оригинальную фотографию
        for r in field['resize']:
            width,height=r['size'].split("x")
            filename=r['file']
            filename=filename.replace('<%filename_without_ext%>',filename_without_ext)
            filename=filename.replace('<%ext%>',out_ext)
            
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
              to_webp=exists_arg('to_webp',field),
            )






    return {
      'success':form.success(),
      'errors':form.errors,
      'value':filename_for_out
    }
