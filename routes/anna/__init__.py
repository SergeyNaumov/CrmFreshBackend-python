from fastapi import FastAPI, APIRouter
from lib.engine import s
from lib.send_mes import send_mes
from lib.form_control import check_rules, is_email, is_phone
from lib.core import exists_arg
from .permissions import *
from .reg_apteka_account import reg_apteka_account, change_apteka_account
from .change_comp_order import change_comp_order
from .change_apteka_order import change_apteka_order
from .get_reg_data import get_reg_data

router = APIRouter()

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
async def change_password(R:dict):
    error=''
    success=1
    p1=R['password1']
    p2=R['password2']

    if not password_ok(R['password']):
        error='Ваш текущий пароль не принят системой, попробуйте ещё раз'
    else:
        if len(p1)<6:
            error='указанный пароль слишком короткий'

        else:
            if not(p1) or not(p2) or p1 != p2 or len(p1)<6:
                error='пароли не совпадают'


    if error:
        success=0
    else: # все проверки пройдены, меняем пароль
        s.db.query(
            query='UPDATE manager set password=sha2(%s,256) where id=%s',
            values=[p1,s.manager['id']]
        )

        # Отправляем сообщение об изменениях пароля сотруднику
        manager=get_manager_data()
        if is_email(R['login']):
            send_mes(
                to=R['login'],
                subject='Изменение пароля в системе Анна',
                message=f"""
                    Логин: {manager['login']}<br>
                    Новый пароль: {p1}
                """
            )


    return {'success':success,'error':error}

# Изменени рег. данных менеджера
@router.post('/change-reg-data')
async def change_reg_data(R:dict):
    
    success=1
    
    rules=[
       [ (R['phone']),'Телефон не указан'],
       [ is_phone(R['phone']),'Телефон указан не корректно' ],
       [ (R['login']),'Логин не указан'],
       [ is_email(R['login']),'Логин указан не корректно, укажите валидный email' ],
       [ (R['name_f']),'Фамилия не указана'],
       [ (R['name_i']),'Имя не указано'],
       [ (R['name_o']),'Отчество не указано'],
       
       [ not exist_login(R['login']), 'Такой Логин уже существует в нашей системе. Пожалуйста укажите другой, или воспользуетесь <a href="/remember">формой восстановления пароля</a>']
    ]
    errors=[]
    check_rules(rules,errors)
    if len(errors):
        success=0
    else:
        s.db.query(
            query="UPDATE manager set login=%s, email=%s, phone=%s, name=%s, name_f=%s, name_i=%s, name_o=%s WHERE id=%s",
            values=[
                R['login'],R['login'],
                R['phone'],
                R['name_f']+' '+R['name_i']+' '+R['name_o'], # Обновляем поле "полное имя"
                R['name_f'],
                R['name_i'],
                R['name_o'],
                s.manager['id']
            ]
        )
    return {'success':success,'errors':errors}

# Заявка на изменение данных юрлица
@router.post('/change-comp-order')
async def route_change_comp_order(R:dict):
    return change_comp_order(R)

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

# Заявка на изменение данных аптеки
@router.post('/change-apteka-order')
async def route_change_apteka_order(R:dict):
    change_apteka_order(R)