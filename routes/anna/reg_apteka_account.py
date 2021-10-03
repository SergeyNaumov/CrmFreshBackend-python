from lib.engine import s
from lib.form_control import check_rules, is_email, is_phone
from .permissions import get_ur_lico, exists_manager_login
from lib.core import exists_arg
from lib.send_mes import send_mes

def reg_apteka_account(R):
    errors=[]
    success=1
    rules=[
       [ (R['apteka_id'] and str(R['apteka_id']).isdigit()) ,'Не указан ID аптеки. обратитесь к разработчику'],
       [ (R['login']),'Логин не указан'],
       [ is_email(R['login']),'Логин должен являться валидным Email-ом' ],
       [ not exists_manager_login(R['login']),'Данный логин уже существует' ],
       
       [ (R['name_f']),'Укажите фамилию'],
       [ (R['name_i']),'Укажите имя'],
       [ (R['name_o']),'Укажите отчество'],
       [ (R['phone']),'Телефон не указан'],
       [ is_phone(R['phone']),'Телефон указан не корректно' ],
    ]
    check_rules(rules,errors)
    
    
    if not len(errors):
        # Если всё ок -- создаём менеджера
        R['type']=3 # тип учётной записи -- Представитель аптеки
        R['email']=R['login']

        apt_manager_id=s.db.save(
            table="manager",
            debug=1,
            data=R,
            errors=errors
        )
        if apt_manager_id:
          s.db.query(
            query="UPDATE manager set password=sha2(%s,256) WHERE id=%s",
            values=[R['password'], apt_manager_id],
            #debug=1,
            errors=errors
          )

          s.db.query(
            query="UPDATE apteka set manager_id=%s where id=%s",
            values=[apt_manager_id,R['apteka_id']],
            #debug=1,
            errors=errors
          )
        
        
    send_mes(
        to=R['login'],
        subject='Для Вас создан аккаунт в системе АннА',
        message=f"""
            Уважаемый(ая) {R['name_f']}  {R['name_i']} {R['name_o']}!<br>
            Только что для Вас был создан аккаунт для входа в систему АннА:<br>
            Логин: {R['login']}<br>
            Пароль: {R['password']}
        """
    )

    if len(errors):
        success=0
    return {'success':success,'errors':errors}

def change_apteka_account(R):
    errors=[]
    success=1
    rules=[
       [ (R['manager_id'] and str(R['manager_id']).isdigit()) ,'Не указан ID менеджера. обратитесь к разработчику'],
       [ (R['login']),'Логин не указан'],
       [ is_email(R['login']),'Логин должен являться валидным Email-ом' ],
       [ not exists_manager_login(R['login'],R['manager_id']),'Данный логин уже существует' ],
       
       [ (R['name_f']),'Укажите фамилию'],
       [ (R['name_i']),'Укажите имя'],
       [ (R['name_o']),'Укажите отчество'],
       [ (R['phone']),'Телефон не указан'],
       [ is_phone(R['phone']),'Телефон указан не корректно' ],
    ]
    check_rules(rules,errors)
    if not exists_arg('password',R):
      R['password']=''

    if not len(errors):
        # Если всё ок -- обновляем


        R['email']=R['login']
        values=[R['login'], R['name_f'], R['name_i'], R['name_i'], R['email'],R['phone']]
        
        
        
        update_query=f'''
              UPDATE manager set
                login=%s, name_f=%s, name_i=%s, name_o=%s,email=%s,phone=%s
        '''

        if R['password']:
          update_query=update_query+', password=sha2(%s,256)'
          values.append(R['password'])

        where=' where id=%s'
        values.append(R['manager_id'])

        s.db.query(
            query=update_query+where,
            values=values,
            errors=errors,
            debug=1
        )


        if R['password']:
          send_mes(
              to=R['login'],
              subject='Изменение данных аккаунта в системе АннА',
              message=f"""
                  Уважаемый(ая) {R['name_f']}  {R['name_f']} {R['name_f']}!<br>
                  Только что были изменены регистрационные данные в системе АннА:<br>
                  Логин: {R['login']}<br>
                  Пароль: {R['password']}
              """
          )

    if len(errors):
        success=0
    return {'success':success,'errors':errors}