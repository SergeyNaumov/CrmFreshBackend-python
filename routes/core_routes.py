# 2026-09-27: migrated core_routes.py, removed global s, engine is on request.state directly

# 2026-09-27: removed from lib.engine import s (global)
from fastapi import APIRouter, Request
from lib.all_configs import read_config, project_get_permissions_for, get_permissions_for
import sys # for debug log
import time


router = APIRouter()



@router.post('/core/get-manager')
async def core_get_manager(R: dict, request: Request): # 2026-09-27: added request: Request
  s=request.state.engine # 2026-09-27: removed global s
  errors=[]; login=R['login']
  
  try:
    manager=await project_get_permissions_for(form=None, login=login) # 2026-09-27: engine is on request.state, not global
    if not manager:
      manager=await get_permissions_for(R=R) # 2026-09-27: engine is on request.state

  except Exception as e:
    errors.append(f'{e}')
    sys.stderr.write(errors)
    
  response={'errors': errors, 'log':errors, 'success':1} if not errors else {'errors':errors,'success':0} # 2026-09-27: removed global db.get_db()
  return response
