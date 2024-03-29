from lib.all_configs import read_config
import shutil, os, re
#import os
#import re
def check_path(path,errors):
    if not (path.startswith('/')):
        errors.append('Wrong parametr path!')

def get_file_list(**arg):
    error=''
    res_dirs=[]
    res_files=[]
    res=[]
    if not len(arg):
        return
    form=arg['form']
    path=arg['path']
    
    path_directory=form.manager['files_dir']+path

    # если нет директории -- создаём её
    if not os.path.isdir(form.manager['files_dir']+path):
      dirname=form.manager['files_dir']
      if path != '/':
        dirname+=path

      if os.path.isfile(dirname):
        error=f'Ошибка wysiwyg: {dirname} -- это файл (а должна быть директория), обратитесь к разработчику'
        return res,error
      else:
        os.makedirs(form.manager['files_dir']+path, exist_ok=True)
        #os.mkdirs(form.manager['files_dir']+path)


    #print('path_directory:',path_directory)
    _list=sorted(os.listdir(path_directory))

    for l in _list:
        
        if(os.path.isdir(path_directory+'/'+l)):
            res_dirs.append({'name':l,'type':'dir'})
        else:
            res_files.append({'name':l,'type':''})
    #return [list(res_dirs),list(res_files)]
    for f in res_dirs: res.append(f)
    for f in res_files: res.append(f)
    #['file1.png','file2.png','file3.png']
    return res,error

def wysiwyg_process(**arg):
  #print('wysiwyg_process - реализовать')
  config=arg['config']
  field_name=arg['field_name']
  errors=[]
  R={}

  if 'R' in arg:
    R=arg['R']
  
  action=''
  if 'action' in R:
    action=R['action']
  
  if 'action' in arg:
    action=arg['action']
  path=''
  
  if 'path' in R:
    path=R['path']
  elif 'path' in arg:
    path=arg['path']
  
  id=''
  if 'id' in arg:
    id=arg['id']
  if 'id' in R:
    id=R['id']
  if 'config' in R:
    config=R['config']
  form=read_config(
    action=action,
    config=config,
    id=id,
    #values=values,
    script='wysiwyg'
  )
  check_path(path,errors)
  #print('action:',action,' errors:',errors,'path: ',path)
  if not len(errors):
    if action == 'file_list':
        file_list,error=get_file_list(path=path,errors=errors,form=form)
        #print('file_list:',file_list)
        if error:
          errors.append(error)
        
        return {
            'success':form.success(),
            'errors':errors,
            'file_list':file_list,
            'files_dir_web':form.manager['files_dir_web']
        }

    elif action=='create_folder':
        new_folder_name=R['new_folder_name']
        if re.match(r'^[a-zA-Z0-9\.\-_]+$',new_folder_name):
            try:
                print('files_dir:',form.manager['files_dir'])
                print('path:',path)
                print('new_folder_name:',new_folder_name)

                os.mkdir(form.manager['files_dir']+path+'/'+new_folder_name)
            except FileExistsError:
                errors.append('уже существует файл или папка с таким именем')
        else:
            errors.append('недопустимые символы в названии папки')
        
        return {
            'success':(not len(errors)),
            'errors':errors,
        }


    elif action=='delete':
        name=''
        if 'name' in R and R['name']:
            name=R['name']
            if re.match(r'\/',name):
                errors.append('ошибка, странный параметр name')
            else:
                obj_path=form.manager['files_dir']+path+name

                if os.path.isdir(obj_path):
                    os.rmdir(obj_path)
                elif os.path.exists(obj_path):
                    os.remove(obj_path)

                file_list,error=get_file_list(path=path,errors=errors,form=form)
                if error:
                  errors.append(error)
                return {
                    'success':(1,0)[len(errors)],
                    'errors':errors,
                    'file_list':file_list,
                    'files_dir_web':form.manager['files_dir_web']
                }
        else:
            errors.append('не указан параметр name')

    elif action=='upload':
        file=arg['file']
        
        
        full_path=f"{form.manager['files_dir']}/{file.filename}"
        if arg['path']:
            P= path[:0] + path[(0+1):] # удаляем начальный слэш
            full_path=f"{form.manager['files_dir']}/{P}{file.filename}"
        print('upload_to:',full_path)
        with open(full_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_list,error=get_file_list(path=path,errors=errors,form=form)
        if error:
          errors.append(error)
        return {
            'success':(1,0)[len(errors)],
            'errors':errors,
            'file_list':file_list,
        }
    else:
        errors.append('action не указан, либо не известен')

  return 
  {'success':(0,1)[len(errors)],'errors':errors}
