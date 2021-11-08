from fastapi import APIRouter #, File, UploadFile, Form, Depends
from lib.all_configs import read_config



router = APIRouter()


# , file: bytes = File(...), fileb: UploadFile = File(...)
#, 
# Загрузка файла в wysiwyg
@router.get('/{config}')
async def wysiwyg_upload(config:str,limit: int = 0): # 
  R={}
  if limit:
    R['limit']=limit

  form=read_config(
    action='',
    config=config,
    R=R,
    #id=id,
    #values=values,
    script='table'
  )
  errors=[]

  

  #print('R:',form.R)
  
  data=[]
  headers=form.headers
  return {
    'form':{
      'config':form.config,
      'title':form.title,
      'log':form.log,
      'errors':form.errors,
      'headers':headers,
      'data':form.data,
      'sort':form.sort,
      'links':form.links,
      'sort_desc':form.sort_desc
    },

    'success':1,

    #'data':form.links
  }

  