from fastapi import APIRouter, Request #, File, UploadFile, Form, Depends
from lib.all_configs import read_config
from lib.svcmsmanager import api_doc, ds_api



router = APIRouter()


# , file: bytes = File(...), fileb: UploadFile = File(...)
#, 
# Документация по конфигу (таблица документации, дерево разделов).
@router.get('/{config}')
async def documentation(config:str,request: Request):

  # Документация API управления контентом DS-сайта генерируется кодом
  # (lib/svcmsmanager/api_doc.py), конфига в БД у неё нет. Ссылку открывает
  # кнопка «Документация» на странице «API и интеграции» (/vue/ds-api).
  if config == 'ds_api':
    manager=getattr(request.state,'manager',None) or {}
    host=manager.get('host') or ''
    tree=api_doc.doc_tree(ds_api.base_url(host) or 'https://<домен>/api/v1')
    return {
      'title':tree['title'],
      'log':[],
      'errors':[],
      'success':1,
      'list':tree['list'],
      'links':tree['links'],
    }

  form = await read_config(
    request=request,
    action='',
    config=config,
    #id=id,
    #values=values,
    script='documentation'
  )
  errors=form.errors

  data_list=await form.db.query(
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
