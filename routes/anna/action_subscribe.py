from lib.engine import s
from .permissions import get_manager_data, get_anna_manager, get_ur_lico
from .get_reg_data import access_ur_lico_ok, access_apteka_ok
from lib.send_mes import send_mes
from lib.core import exists_arg



def action_subscribe_ur_lico(action_id:int, ur_lico_id: int):
    manager_data=get_manager_data()
    success=1
    errors=[]
    # Если у данного менеджера есть полномочия менять юрлицо
    ur_lico=get_ur_lico(ur_lico_id)
    action=s.db.query(
      query="select header from action where id=%s",
      values=[action_id],
      onerow=1
    )

    anna_manager=get_anna_manager()    
    if not ur_lico:
        errors.append('Юридическое лицо с таким id не найдено')
    elif not action:
        errors.append('Мероприятие с таким id не найдено')

    elif str(manager_data['type']) != '2':
        errors.append('Вы не являетесь представителем юридического лица')
    
    elif not anna_manager:
        errors.append('Вы не являетесь представителем юридического лица')

    elif ur_lico and access_ur_lico_ok(manager_data['id'], str(ur_lico_id)) :
        s.db.save(
            table='action_ur_lico_request',
            replace=1,
            data={
                'action_id':action_id,
                'ur_lico_id':ur_lico_id
            },
            debug=1,
            errors=errors
        )

        
        if exists_arg('email',anna_manager):
            

            subject=f"{anna_manager['fio']} - {s.env['host']} Подписка на мероприятие:{action['header']} от {ur_lico['header']}"
            message=f'''
                Только что представитель юридического лица <a href="https://{s.env['host']}/edit-form/ur_lico/{ur_lico['id']}">{ur_lico['header']}</a>,<br>
                {manager_data['name_f']} {manager_data['name_i']} {manager_data['name_o']}<br>
                Отправил запрос на оформление подписки на мероприятие:<br>
                {action['header']}
            '''

            send_mes(
                to=anna_manager['email'],
                subject=subject,
                message=message
            )

            #print('subject:',subject)
            #print('message:',message)

    else:
        success=0
    
    if len(errors):
        success=0    
    
    return {'success':success,'errors':errors}

def action_subscribe_apteka(action_id:int,apteka_id:int):
    manager_data=get_manager_data()
    success=1
    errors=[]
    action=s.db.query(
      query="select header from action where id=%s",
      values=[action_id],
      onerow=1
    )

    apteka=s.db.query(
        query="select id,ur_address,ur_lico_id from apteka where id=%s",
        values=[apteka_id],
        onerow=1
    )
    print('apteka:',apteka)
    ur_lico_manager=''
    ur_lico=get_ur_lico(apteka['ur_lico_id'])
    if ur_lico:
        ur_lico_manager=s.db.query(
            query='''
                select
                    m.id,m.login email,
                    concat(name_f,' ',name_i,' ',name_o) fio
                from
                    ur_lico_manager ulm
                    JOIN manager m ON m.id=ulm.manager_id
                WHERE
                    ulm.ur_lico_id=%s
            ''',
            values=[apteka['ur_lico_id']],
            onerow=1
        )




    

    print('ur_lico:',ur_lico)
    print('ur_lico_manager:',ur_lico_manager)
    
    if str(manager_data['type']) != '3':
        errors.append('Вы не являетесь представителем аптеки')
    elif not apteka:
        errors.append('Аптека с таким id не найдена')
    
    elif not ur_lico:
        errors.append('Для данной аптеки не установлено юридическое лицо, свяжитесь с разработчиком')
    elif not ur_lico_manager:
        errors.append(f'Для Вашего юридического лица ({ur_lico["header"]}) не выбран ответственный')
    elif not action:
        errors.append('Мероприятие с таким id не найдено')
    elif not access_apteka_ok(manager_data['id'], apteka_id):
        errors.append('У Вас нет праф оформлять подписку для данной аптеки')
    elif apteka :
        s.db.save(
            table='action_apteka_request',
            replace=1,
            data={
                'action_id':action_id,
                'apteka_id':apteka_id
            },
            debug=1,
            errors=errors
        )

        
        if exists_arg('email',ur_lico_manager):
            

            subject=f"{ur_lico_manager['fio']} - {s.env['host']} Подписка на мероприятие:{action['header']} от {ur_lico['header']}"
            message=f'''
                Только что представитель аптеки  <a href="https://{s.env['host']}/edit-form/apteka/{apteka_id}">{apteka['ur_address']}</a>,<br>
                {manager_data['name_f']} {manager_data['name_i']} {manager_data['name_o']}<br>
                Отправил запрос на оформление подписки на мероприятие:<br>
                {action['header']}
            '''

            send_mes(
                to=ur_lico_manager['email'],
                subject=subject,
                message=message
            )

            print('subject:',subject)
            print('message:',message)

    else:
        success=0
    
    if len(errors):
        success=0    

    return {'success':success,'errors':errors}