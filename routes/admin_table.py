from lib.core import cur_year,cur_date, success
from fastapi import FastAPI, APIRouter
from config import config
from lib.CRM.filters import get_filters
from lib.engine import s


router = APIRouter()

@router.get('/get-filters/{config}')
async def get_filters_controller(config: str):
  return get_filters(
    config=config,
    script='admin_table',
    #R=R
  )

