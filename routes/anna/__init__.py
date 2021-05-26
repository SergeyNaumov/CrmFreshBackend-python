from fastapi import FastAPI, APIRouter
from lib.engine import s
from lib.send_mes import send_mes
from lib.form_control import check_rules, is_email, is_phone
from lib.core import exists_arg

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
def get_manager_data(errors=[]):
    return s.db.query(
        query="""
            SELECT
                wt.id,wt.login,wt.name_f,wt.name_i,wt.name_o,wt.name,wt.phone,wt.type,
                ma.id ma_id, ma.name_f ma_name_f,  ma.name_i ma_name_i, ma.name_o ma_name_o, ma.email ma_email, ma.phone ma_phone
            FROM 
                manager wt
                LEFT JOIN manager ma ON wt.anna_manager_id=ma.id
            WHERE wt.id=%s
        """,
        values=[s.manager['id']],
        onerow=1

    )

    # s.db.getrow(
    #       table="manager",
    #       select_fields='id,login,name_f,name_i,name_o,name,phone,type',
    #       where='id=%s',
    #       errors=errors,
    #       values=[s.manager['id']],
    # )
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
    



@router.get('/get-reg-data')
async def get_reg_data():
    response={
        'success':1,
        'comp_list':[],
        'apt_list':[],
    }
    errors=[]
    manager=get_manager_data(errors)

    if not len(errors):
        response['manager']=manager
        # Менеджер Анна
        if str(manager['type'])=="1":
            response['comp_list'] = s.db.get(
                table='comp',
                where="anna_manager_id = %s",
                values=[s.manager['id']]
            )

        # Представитель юридического лица
        if str(manager['type'])=="2":
            response['comp_list']=s.db.query(
                query="""
                    SELECT
                        wt.*, 0 more, concat(m.name_f,' ',m.name_i,' ',m.name_o)  ma_fio, m.email ma_email,
                        m.phone ma_phone
                    FROM
                        ur_lico_manager ulm
                        join ur_lico wt ON wt.id=ulm.ur_lico_id
                        left join manager m ON wt.anna_manager_id=m.id
                    WHERE
                        ulm.manager_id=%s

                """,
                values=[s.manager['id']]
            )
            for c in response['comp_list']:

                c['apteka_list']=s.db.query(
                    query="""
                        SELECT
                            wt.id,wt.ur_address,0 more,
                            wt.email, wt.inn, wt.header, wt.phone,
                            concat(m.name_f,' ',m.name_i,' ',m.name_o)  m_fio, m.email m_email,
                            m.phone m_phone,
                            apt_set.apteka_id apt_set_id, apt_set.set1, apt_set.set2,
                            1 saved_s1, 1 saved_s2
                        from 
                            apteka wt
                            LEFT JOIN manager m ON m.id=wt.manager_id
                            LEFT JOIN apteka_settings apt_set ON apt_set.apteka_id=wt.id
                        where wt.ur_lico_id=%s
                    """,
                    values=[c['id']]
                )
                for a in c['apteka_list']:
                    if not a['apt_set_id']:
                        s.db.save(
                            table="apteka_settings",
                            data={
                                'apteka_id':a['id'],'set1':1,'set2':1
                            }
                        )
                        a['set1']=1
                        a['set2']=1
            # s.db.get(
            #     table='comp',
            #     select_fields='*, 0 more',
            #     where='manager_id = %s',
            #     values=[s.manager['id']],
            #     errors=errors
            # )

        # Представитель аптеки
        if str(manager['type'])=="3":
            
            response['apt_list']=s.db.get(
                table='apteka',
                select_fields='*, 0 more',
                where='manager_id = %s',
                values=[s.manager['id']],
                errors=errors
            )
    response['errors']=errors
    if len(errors): response['success']=0
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
    check_rules(rules,errors)

    if not len(errors):
        R['manager_id']=s.manager['id']
        s.db.save(
            table="change_comp_order",
            data=R,
            errors=errors
        )

    if len(errors):
        success=0

    return {'success':success,'errors':errors}

# Заявка на изменение данных аптеки
@router.post('/change-apteka-order')
async def change_comp_order(R:dict):
    errors=[]
    success=1
    rules=[
       [ (exists_arg('apteka_id',R) and str(R['apteka_id']).isdigit()) ,'Не указан comp_id. обратитесь к разработчику'],
       [ (R['phone']),'Телефон не указан'],
       [ is_phone(R['phone']),'Телефон указан не корректно' ],
       [ (R['email']),'Email не указан'],
       [ is_email(R['email']),'Email указан не корректно, укажите валидный email' ],
       [ (R['header']),'Заполните наименование компании'],
       [ (  not(R['inn']) or len(R['inn'])==10 or len(R['inn'])==12 ),'ИНН должен быть 10 или 12 цифр'],
       
       
    ]
    check_rules(rules,errors)

    if not len(errors):
        R['manager_id']=s.manager['id']
        s.db.save(
            table="change_apteka_order",
            data=R,
            errors=errors
        )

    if len(errors):
        success=0

    return {'success':success,'errors':errors}