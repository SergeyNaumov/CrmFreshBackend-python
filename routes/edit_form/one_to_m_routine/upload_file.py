from lib.core import get_child_field, exists_arg, get_ext, random_filename
from lib.get_1_to_m_data import get_1_to_m_data
from lib.resize import resize_one
import shutil,os

def upload_file(form,field,arg):
  child_field_name=arg['child_field_name']
  child_field=get_child_field(field,child_field_name)
  if not child_field:
    form.errors.append(f'не найдено поле {child_field_name} в {field["name"]} обратитесь к разработчику')
  

  #if form.success():

  


  # сохраняем файл
  if form.success():
    attach=arg['attach']
    orig_filename=attach.filename

    # сохраняем файл
    if not os.path.exists(child_field['filedir']):
      os.mkdir(child_field['filedir'])



    ext=get_ext(orig_filename)
    filename_without_ext=random_filename()
    filename=filename_without_ext+'.'+ext
    
    full_name=child_field['filedir']+'/'+filename
    with open(full_name, "wb") as buffer:
         shutil.copyfileobj(attach.file, buffer)

    db_value=filename
    if exists_arg('keep_orig_filename',child_field):
      db_value+=";"+orig_filename
    
    # resize:
    if exists_arg('resize',child_field):
      for r in child_field['resize']:
        width,height=r['size'].split("x")
        resize_filename=r['file']
        resize_filename=resize_filename.replace('<%filename_without_ext%>',filename_without_ext)
        resize_filename=resize_filename.replace('<%ext%>',ext)
        resize_one(
          fr=child_field['filedir']+'/'+filename_without_ext+'.'+ext,
          to=child_field['filedir']+'/'+resize_filename,
          width=width,
          height=height,
          grayscale=exfts_arg('grayscale',r),
          composite_file=exists_arg('composite_file',r),
          composite_gravity=exists_arg('composite_gravity',r),
          composite_resize=exists_arg('composite_resize',r),
          quality=exists_arg('quality',r),
        )

    
    if arg['one_to_m_id']:

        oldfile=form.db.query(
          query=f'SELECT {child_field["name"]} from {field["table"]} WHERE {field["foreign_key"]}=%s and {field["table_id"]}=%s',
          values=[form.id,arg["one_to_m_id"] ],
          onevalue=1,
          errors=form.errors
        )

        # удаляем старый файл
        if form.success() and oldfile:


          oldfile_arr=oldfile.split(':')
          if len(oldfile_arr)==2:
            oldfile=oldfile_arr[1]
          
          if os.path.exists(child_field['filedir']+'/'+oldfile):
            os.remove(child_field['filedir']+'/'+oldfile)




        form.db.save(
          table=field['table'],
          update=1,
          where=f'{field["foreign_key"]}={form.id} and {field["table_id"]}={arg["one_to_m_id"]}',
          
          data={
            child_field['name']: db_value
          }
        )
        # Сделать ресайз!

        get_1_to_m_data(form,field)
        return {
          'success':form.success(),
          'errors':form.errors,

          'values':field['values']
        }

    else: # multi

        db_value=filename
        if exists_arg('keep_orig_filename',child_field):
          db_value+=";"+orig_filename
        
        id = form.db.save(
          table=field['table'],
          data={
            field['foreign_key']:form.id,
            child_field_name:db_value
          }
        )

        value={
          field['foreign_key']:form.id,
          field['table_id']:id,
          child_field['name']:filename,
          child_field['name']+'_filename':filename,
        }



        return {
          'success':form.success(),
          'errors':form.errors,
          'values':[value]
          # 'file_info': [{
          #   'name':filename,
          #   'orig_name':orig_filename,
          #   'full_name':full_name
          #   }]
        }





  


