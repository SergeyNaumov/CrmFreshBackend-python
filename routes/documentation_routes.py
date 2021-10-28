from fastapi import APIRouter #, File, UploadFile, Form, Depends
from lib.all_configs import read_config



router = APIRouter()


# , file: bytes = File(...), fileb: UploadFile = File(...)
#, 
# Загрузка файла в wysiwyg
@router.get('/{config}')
async def wysiwyg_upload(config:str): # 

  form=read_config(
    action='',
    config=config,
    #id=id,
    #values=values,
    script='documentation'
  )
  errors=form.errors

  data_list=form.db.query(
    query=f'select * from {form.work_table} order by sort' ,
    #debug=1,
    #table=config,
    #order='sort',
    #where='parent_id is null',

    errors=errors,
    tree_use=1
  )

  #for d in data_list:

  return {
    'title':form.title,
    'log':form.log,
    'errors':form.errors,
    'success':1,
    'list':data_list,
    'links':form.links
  }

  