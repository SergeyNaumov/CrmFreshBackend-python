from fastapi import APIRouter, Request

from .left_menu_admin import left_menu_admin
from .project_sitemap import router as router_project_sitemap
from .project_struct import router as router_project_struct
from .project_export import router as router_project_export
from .project_clone import router as router_project_clone
from .domain import router as router_domain
from .page_constructor import router as router_page_constructor


router = APIRouter()
router.include_router(router_project_sitemap)
router.include_router(router_project_struct)
router.include_router(router_project_export)
router.include_router(router_project_clone)
router.include_router(router_domain)
router.include_router(router_page_constructor, prefix='/page-constructor')


@router.get('/left-menu-admin')
async def controller_left_menu_admin(request: Request):
  return await left_menu_admin(request)
