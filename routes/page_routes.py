from fastapi import APIRouter #, File, UploadFile, Form, Depends
from lib.all_configs import read_config



router = APIRouter()


# , file: bytes = File(...), fileb: UploadFile = File(...)
#, 
# Загрузка файла в wysiwyg
@router.get('/{config}/{id}')
async def process_page(config:str,id:int,referer:str): # 
  form=read_config(
    action='',
    config=config,
    id=id,
    referer=referer,
    #values=values,
    script='page'
  )
  errors=form.errors

  #for d in data_list:

  return {
    'form':{
      
      'title':form.title,
      'blocks':form.blocks,
      'log':form.log,
      'errors':form.errors,

    },
    'javascript':form.javascript['page'],
    'success':1,

  }

  