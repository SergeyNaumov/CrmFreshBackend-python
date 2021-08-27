from lib.engine import s
from .permissions import get_manager_data, exist_login, get_ur_lico
from lib.form_control import check_rules, is_email, is_phone
from lib.send_mes import send_mes
from lib.core import exists_arg

def change_reg_data(R:dict):
    success=1
    manager=get_manager_data()
   # print('manager:',manager)
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
          s.db.save(
            table="order_change_account",
            data={
                'login': R['login'],
                'phone': R['phone'],
                'name_f':R['name_f'],
                'name_i':R['name_i'],
                'name_o':R['name_o'],
                'manager_id':s.manager['id']
            },
            
          )

          # Если рег. данные меняет аптека, тогда сразу сохраням их
          if manager['type']==3:
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

    name_role="представитель "


    
    subject=f"Изменение регистрационных данных - {manager['login']}"
    # отправляем представителю юрлица


    if manager['type']==2:
        ur_lico_list=manager['ur_lico_list']

        if len(ur_lico_list)>1:
            name_role+=" юридических лиц:<br>"

        for u in ur_lico_list:
            u['id']=str(u['id'])
            name_role+=f"""<a href="https://{s.env['host']}/edit-form/ur_lico/{ u['id'] }">{u['header']}</a><br>\n"""

    apteka=None
    if manager['type']==3:
        name_role+=" аптеки "
        apteka=manager['apteka']
        if apteka:
            name_role+=f"""<a href="https://{s.env['host']}/edit-form/apteka/{ apteka['id'] }">{apteka['ur_address']}</a>"""

    
    message=f"""
    {manager['name_f']} {manager['name_i']} {manager['name_o']}, {name_role}<br>
    Изменение регистрационных данных:<br>
    <b>Логин:</b> {R['login']}<br>
    <b>Телефон:</b> {R['phone']}<br>
    <b>Фамилия:</b> {R['name_f']}<br>
    <b>Имя:</b> {R['name_i']}<br>
    <b>Отчество:</b> {R['name_o']}<br>
    """

    

    if apteka: # если это представитель аптеки -- отправляем в юрлицо
        #print('apteka:',apteka)
        # Письмо представителю юридического лица
        ur_lico=manager['ur_lico']
        
        if exists_arg('email_for_notify',ur_lico) and is_email(ur_lico['email_for_notify']):
            print('send_to (ur_lico):',ur_lico['email_for_notify'])
            send_mes(
                to=ur_lico['email_for_notify'],
                subject=subject,
                message=message
            )


    else:
        message_manager_anna=f"""
            {manager['ma_name_f']} {manager['ma_name_i']} {manager['ma_name_o']} -<br>
            {message}
        """
    # Письмо менеджеру АннА
    
    if manager['type'] in [2,3] and is_email(manager['ma_email']):
        # если рег. данные меняет юр.лицо
        if manager['type']==2: # гер
            send_mes(
                to=manager['ma_email'],
                subject=f"Изменение регистрационных данных ",
                message=message_manager_anna
            )
        
        # Если рег. данные меняет аптека
        if manager['type']==3:
            send_mes(
                to=manager['ma_email'],
                subject=f"{manager['ma_name_f']} {manager['ma_name_i']} {manager['ma_name_o']} - изменение регистрационных данных для аптеки",
                message=f"""
                    <b>{ur_lico['header']}</b><br>
                    {message}
                """
            )

        print('send_to (anna manager):',manager['ma_email'])

    if is_email(manager['login']):
        send_mes(
            to=manager['login'],
            subject=subject,
            message=message
        )
        print('send_to (account):',manager['login'])

    
    return {'success':success,'errors':errors}
