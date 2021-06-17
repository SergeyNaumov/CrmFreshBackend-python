from fastapi import  APIRouter

from .action_plan import action_plan

router = APIRouter()
@router.get('/action_plan')
async def x():
    return {'ok':1}

@router.get('/action_plan/{format}/{id}')
def download_action_plan(format:str,id:int):
    return action_plan(format,id)
