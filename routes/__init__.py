from fastapi import APIRouter
#from config import config
from lib.engine import s
from .core_routes import router as router_core
from .register import router as router_register
from .admin_tree_routes import router as router_admin_tree
from .get_filters_routes import router as router_get_filters
from .get_result_routes import router as router_get_result
from .edit_form_routes import router as router_edit_form
from .one_to_m_routes import router as router_one_to_m
from .memo import router as router_memo
from .password import router as router_password
from .ajax import router as router_ajax
from .autocomplete import router as router_autocomplete
from .stat_tool import router as stat_tool
from .documentation_routes import router as router_documentation
from .page_routes import router as router_page
from .video_routes import router as router_video
from .news_routes import router as router_news
from .table_routes import router as router_table
from .const_routes import router as router_const
from .docpack_routes import router as router_docpack

# messenger
from .messenger import router as router_messenger


# Роутеры, не входящие в систему
from .testing import router as router_testing
from .svcms import router as router_svcms

# Расширения
from .extend_routes import router as router_extend

router = APIRouter()
# /register /remember
router.include_router(router_register)
router.include_router(router_password)

# /login, /logout, /mainpage, /startpage 
router.include_router(router_core)




router.include_router(router_testing)
router.include_router(router_get_filters)
router.include_router(router_get_result)
router.include_router(router_admin_tree)
router.include_router(router_edit_form)
router.include_router(router_one_to_m)
router.include_router(router_memo,prefix='/memo')
router.include_router(router_const,prefix='/const')
router.include_router(router_docpack,prefix='/docpack')

router.include_router(router_messenger,prefix='/messenger')


router.include_router(router_extend)
router.include_router(router_documentation,prefix='/documentation')

router.include_router(router_page,prefix='/page')
router.include_router(router_table,prefix='/table')

router.include_router(router_video,prefix='/VideoList')
router.include_router(router_news,prefix='/NewsList')

router.include_router(router_autocomplete,prefix='/autocomplete')
router.include_router(stat_tool,prefix='/stat-tool')

router.include_router(router_ajax) # /ajax

router.include_router(router_svcms,prefix='/svcms')




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






