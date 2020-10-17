from fastapi import APIRouter
#from config import config
from lib.engine import s
from .core_routes import router as router_core


from .get_filters_routes import router as router_get_filters
from .get_result_routes import router as router_get_result


from .testing import router as router_testing

router = APIRouter()

router.include_router(router_core)
router.include_router(router_testing)
router.include_router(router_get_filters)
router.include_router(router_get_result)
#router.include_router(router_admin_table)

@router.get("/")
async def mainpage():
  permissions=s.db.query(
         query='SELECT login from manager',
         massive=1
  )

  return {
    'permissions':permissions
  }






