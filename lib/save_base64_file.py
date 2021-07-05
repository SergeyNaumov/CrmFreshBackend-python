import re, os
from base64 import decodestring
from lib.core import exists_arg, del_file_and_resizes,get_name_and_ext, random_filename
#from lib.resize import resize_all

def save_base64_file(**arg):


    if exists_arg('filedir',arg) and exists_arg('src',arg) and exists_arg('orig_filename',arg):
          
          #print('src:',arg['src'])
          # Сохраняем файл
          rez = re.search(r'^data:(.+?);base64,(.+)',arg['src'])
          

          if rez:
            # Сохраняем файл
            filename=''
            if exists_arg('filename',arg):
              filename=arg['filename']
            else:
              [name,ext]=get_name_and_ext(arg['orig_filename'])
              filename=random_filename()+'.'+ext

            fullname=arg['filedir']+'/'+filename
            mime=rez[1]
            base64=str.encode(rez[2])
            fh = open(fullname, "wb")
            fh.write(decodestring(base64))
            fh.close()
            return filename

    else:
          form=arg['form']
          field=arg['field']
          ext=arg['ext']
          to_save_field=''
          filename=arg['filename']
          


          if 'filedir' not in field or not field['filedir']:
            form.errors.append(f'для поля field["name"] не указан filedir')
            return 
          
          if not os.path.isdir(field['filedir']):
            try:
              os.mkdir(field['filedir'])
            except FileExistsError:
              errors.append(f'не удалось создать директорию {field["filedir"]}')

          fullname=field['filedir']+'/'+filename


          rez = re.search(r'^data:(.+?);base64,(.+)',arg['src'])
          if rez:
            # Сохраняем файл
            mime=rez[1]
            base64=str.encode(rez[2])
            fh = open(fullname, "wb")
            fh.write(decodestring(base64))
            fh.close()



          else:
            form.errors.append('save_base64_file: не получен src в нужном формате (data:....;base64,....)')
            return 

          # удаляем старый
          if not exists_arg('table',arg) or not exists_arg('id',arg):
            return



          old_photo=form.db.query(
            query=f'SELECT {field["name"]} from {arg["table"]} WHERE id=%s',
            values=[arg['id']],
            onevalue=1,
            errors=form.errors
          )
          #print()
          #print('OLD_PHOTO: ',old_photo)
          # удаляем старое фото и все его ресайзы

          del_file_and_resizes(
            field=field,
            value=old_photo
          )


          # сохраняем полное имя в базе или нет?
          if exists_arg('keep_orig_filename',field):
            filename+=';'+arg['orig_name']

          elif exists_arg('keep_orig_filename_in_field',field):
            form.db.query(
              query=f'UPDATE {arg["table"]} SET {field["name"]}=%s, {field["keep_orig_filename_in_field"]}=%s where id=%s',
              values=[filename,arg['orig_name'],arg['id']]
            )

          form.db.query(
            query=f'UPDATE {arg["table"]} SET {field["name"]}=%s where id=%s',
            errors=form.errors,
            values=[filename,arg['id']],
          )

  
    


def b64_split(src):
  print('SRC:',src)
