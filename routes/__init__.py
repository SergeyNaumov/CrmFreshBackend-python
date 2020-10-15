from fastapi import APIRouter
#from config import config
from lib.engine import s

from .core_routes import router as router_core
from .admin_table import router as router_admin_table
from .testing import router as router_testing

router = APIRouter()


router.include_router(router_core)
router.include_router(router_testing)

router.include_router(router_admin_table)

@router.get("/")
async def mainpage():
  permissions=s.db.query(
         query='SELECT login from manager',
         massive=1
  )

  return {
    'permissions':permissions
  }






