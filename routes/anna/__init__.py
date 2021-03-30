from fastapi import FastAPI, APIRouter
from lib.engine import s
from lib.send_mes import send_mes
from lib.form_control import check_rules, is_email, is_phone

router = APIRouter()

def exist_login(login):
  # Проверяем заявку
  return s.db.getrow(
    table='order_reg_company',
    where='id<>%s and  login = %s',
    values=[s.manager['id'], login],
    onerow=1
  )

def password_ok(p):
    return s.db.query(
        query="select count(*) from manager where id=%s and password=sha2(%s,256)",
        values=[s.manager['id'],p],
        onevalue=1
    )
def get_manager_data():
    return s.db.getrow(
          table="manager",
          select_fields='id,login,name_f,name_i,name_o,name,phone,type',
          where='id=%s',
          values=[s.manager['id']],
    )

@router.get('/get-reg-data')
async def get_reg_data():
    response={
        'success':1,
        'comp_list':[],
        'apt_list':[]
    }
    manager=get_manager_data()
    response['manager']=manager
    # Менеджер Анна
    if manager['type']==1:
        response['comp_list'] = s.db.get(
            table='comp',
            where="anna_manager_id = %s",
            values=[s.manager['id']]
        )

    # Представитель юридического лица
    if manager['type']==2:
        response['comp_list']=s.db.get(
            table='comp',
            select_fields='id,header,inn,phone,email,email_for_notify,0 more',
            where='manager_id = %s',
            values=[s.manager['id']]
        )

    # Представитель аптеки
    if manager['type']==3:
        response['apt_list']=s.db.get(
            table='apteka',
            where='manager_id = %s',
            values=[s.manager['id']]
        )
    return response

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
    errors=check_rules(rules)
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
async def change_comp_order(R:dict):
    errors=[]
    success=1
    rules=[
       [ (R['comp_id'] and str(R['comp_id']).isdigit()) ,'Не указан comp_id. обратитесь к разработчику'],
       [ (R['phone']),'Телефон не указан'],
       [ is_phone(R['phone']),'Телефон указан не корректно' ],
       [ (R['email']),'Email не указан'],

       [ is_email(R['email']),'Email указан не корректно, укажите валидный email' ],
       [ (R['header']),'Заполните наименование компании'],
       [ (  not(R['inn']) or len(R['inn'])==10 or len(R['inn'])==12 ),'ИНН должен быть 10 или 12 цифр'],
       
       
    ]
    errors=check_rules
    return {'success':success,'errors':errors}