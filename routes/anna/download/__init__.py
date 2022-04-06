from fastapi import  APIRouter

from .action_plan import action_plan, dbf_ready as action_plan_dbf_ready
from .cert import download_cert, html_cert

router = APIRouter()
@router.get('/action_plan/dbf-ready/{id}')
def dbf_ready(id:int):
    return action_plan_dbf_ready(id)

@router.get('/action_plan')
async def x():
    return {'ok':1}

@router.get('/certpdf/{id}')
def cert(id:int):
    return download_cert(id)

@router.get('/cert/{id}')
def cert(id:int):
    return html_cert(id)

@router.get('/action_plan/{format}/{id}')
def download_action_plan(format:str,id:int):
    return action_plan(format,id)


    