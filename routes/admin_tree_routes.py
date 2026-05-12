from fastapi import FastAPI, APIRouter, Request

from .admin_tree.admin_tree_run import admin_tree_run

  


router = APIRouter()
# Главная
@router.get('/admin-tree/{config}')
async def admin_tree(config: str, request:Request):
  return await admin_tree_run(
    config=config,
    request=request,
    R={}
  )

@router.post('/admin-tree/{config}')
async def admin_tree(config: str,R:dict, request:Request):
  result = await admin_tree_run(
    config=config,
    request=request,
    R=R
  )
  print('after await')
  return result
  