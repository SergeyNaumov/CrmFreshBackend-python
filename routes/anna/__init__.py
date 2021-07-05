#from fastapi import FastAPI, APIRouter
from fastapi import APIRouter
from lib.engine import s
from lib.send_mes import send_mes
from lib.form_control import check_rules, is_email, is_phone
from lib.core import exists_arg
from .permissions import *
from .reg_apteka_account import reg_apteka_account, change_apteka_account
from .change_comp_order import change_comp_order, change_on_notify
from .change_apteka_order import change_apteka_order
from .get_reg_data import get_reg_data, access_ur_lico_ok
from .left_menu import left_menu
from .action_subscribe import *
from .change_reg_data import change_reg_data
from .change_password import change_password

from .download import router as download
from .bonus import router as bonus

router = APIRouter()

# скачивание xls и dbf
router.include_router(download,prefix='/download')

# Загрузка формы из бонуса
router.include_router(bonus,prefix='/bonus')

#@router.get('/download/action_plan')
#def x():
#    return {'ok':1}

@router.get('/left-menu')
def controller_left_menu():
    return left_menu()


@router.post('/check-account-login')
def check_account_login(R:dict):
    errors=[]
    if not exists_arg('id',R): R['id']='0'
    if(exists_arg('login',R)):
        if exists_manager_login(R['login'],R['id']):
            errors.append('Такой логин уже существует')
    else:
        errors.append('Неверный запрос')

    if len(errors):
        return {"success":0,"errors":errors}
    return {"success":1,"errors":[]}



# Регистрация менеджера-представителя аптеки
@router.post('/reg-apteka-account')
def router_reg_apteka_account(R:dict):
    return reg_apteka_account(R)

# Изменение данных менеджера-представителя аптеки
@router.post('/change-apteka-account')
def router_change_apteka_account(R:dict):
    return change_apteka_account(R)


# Опции для аптеки
@router.post('/change-set-apteka')
async def change_set(R: dict):
    if exists_arg('apteka_id',R) and 'value' in R and exists_arg('number',R): 
        field_name='set'+str(R['number'])

        exists=s.db.query(
            query="SELECT apteka_id from apteka_settings where apteka_id=%s limit 1",
            values=[R['apteka_id']],
            onevalue=1
        )
        if exists:
            s.db.query(
                query=f"UPDATE apteka_settings SET {field_name}=%s where apteka_id=%s""",
                debug=1,
                values=[R['value'],R['apteka_id']]
            )
        else:
            s.db.save(
                table='apteka_settings',
                data={
                    'apteka_id': R['apteka_id'],
                    field_name: R['value']
                }
            )
        return {'success':1}
    else:
        return {'success':0}
    


# Главная страница АннА, получение гегистрационных данных
@router.get('/get-reg-data') 
async def route_get_reg_data():
    return get_reg_data()


# Проверка пароля
@router.post('/check-password')
async def check_password(R: dict):
    success=1
    error=''
    
    # Пароль не подошёл
    if not password_ok(R['password']):
        success=0
        error='введённый пароль не подошёл'

    return {
        'success':success,
        'error':error
    }

@router.post('/change-password')
async def change_password_controller(R:dict):
    return change_password(R)

# Изменени рег. данных менеджера
@router.post('/change-reg-data')
async def change_reg_data_controller(R:dict):
    return change_reg_data(R)


# Заявка на изменение данных юрлица
@router.post('/change-comp-order')
async def route_change_comp_order(R:dict):
    return change_comp_order(R)

# ставим / снимаем галку у юрлица "уведомлять о подписке аптек"
@router.get('/change-on-notify/{ur_lico_id}/{v}')
async def route_change_on_notify(ur_lico_id:int,v:int):
    return change_on_notify(ur_lico_id,v)

@router.post('/get-account-data')
async def get_account_data(R:dict):
    if R['id']:
        data=s.db.query(
            query="select login,name_f,name_i,name_o,phone from manager where id=%s",
            values=[R['id']],
            onerow=1
        )
        if data :
            return {"success":1,"data":data}
        
    return {"success":0,"errors":"что-то пошло не так"}


# Заявка от юрлица для подписки на акцию
@router.get('/subscribe-action/{action_id}/ur_lico/{ur_lico_id}')
async def request(action_id:int, ur_lico_id:int):
    return action_subscribe_ur_lico(action_id,ur_lico_id)



# Заявка от аптеки для подписки на акцию
@router.get('/subscribe-action/{action_id}/apteka/{apteka_id}')
async def request(action_id:int, apteka_id:int):
    return action_subscribe_apteka(action_id,apteka_id)

# Заявка на изменение данных аптеки
@router.post('/change-apteka-order')
async def route_change_apteka_order(R:dict):
    change_apteka_order(R)