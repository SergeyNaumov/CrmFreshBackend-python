from fastapi import FastAPI, APIRouter

from .admin_tree.admin_tree_run import admin_tree_run

  


router = APIRouter()
# Главная
@router.get('/admin-tree/{config}')
async def admin_tree(config: str):
  return await admin_tree_run(
    config=config,
    R={}
  )

@router.post('/admin-tree/{config}')
async def admin_tree(config: str,R:dict):
  result = await admin_tree_run(
    config=config,
    R=R
  )
  print('after await')
  return result
  