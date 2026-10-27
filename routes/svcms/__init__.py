#from fastapi import FastAPI, APIRouter
from fastapi import APIRouter, Request
#from lib.send_mes import send_mes
#from lib.form_control import check_rules, is_email, is_phone
#from lib.core import exists_arg

from .left_menu import left_menu
from .startpage import router as router_startpage
from .data_transfer import router as router_data_transfer
from .api_keys import router as router_api




router = APIRouter()



#@router.get('/download/action_plan')
#def x():
#    return {'ok':1}

@router.get('/left-menu')
async def controller_left_menu(request: Request):
    return await left_menu(request)

# Стартовая страница клиентской админки (карточка хостинга/домена + заявки)
router.include_router(router_startpage)

# Импорт/экспорт данных проекта (/svcms/data/...)
router.include_router(router_data_transfer)

# API и интеграции: ключ, настройки, статистика (/svcms/api/...)
router.include_router(router_api)



