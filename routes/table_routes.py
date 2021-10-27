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
    script='table'
  )
  errors=[]

  

  #for d in data_list:
  data=[]
  headers=form.headers
  return {
    'form':{
      'title':form.title,
      'log':form.log,
      'errors':form.errors,
      'headers':headers,
      'data':form.data,
      'sort':form.sort,
      'sort_desc':form.sort_desc
    },

    'success':1,

    #'data':form.links
  }

  