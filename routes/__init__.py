from fastapi import APIRouter
#from config import config
from lib.engine import s
from .core_routes import router as router_core

from .admin_tree_routes import router as router_admin_tree
from .get_filters_routes import router as router_get_filters
from .get_result_routes import router as router_get_result
from .edit_form_routes import router as router_edit_form
from .one_to_m_routes import router as router_one_to_m
from .testing import router as router_testing

# Расширения
from .extend_routes import router as router_extend

router = APIRouter()

router.include_router(router_core)
router.include_router(router_testing)
router.include_router(router_get_filters)
router.include_router(router_get_result)
router.include_router(router_admin_tree)
router.include_router(router_edit_form)
router.include_router(router_one_to_m)
router.include_router(router_extend)



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






