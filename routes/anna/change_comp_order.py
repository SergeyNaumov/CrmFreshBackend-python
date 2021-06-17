from lib.engine import s
from lib.form_control import check_rules, is_email, is_phone
from .permissions import get_ur_lico, get_anna_manager
from lib.core import exists_arg
from lib.send_mes import send_mes

def change_comp_order(R):
    errors=[]
    success=1
    rules=[
       [ (R['comp_id'] and str(R['comp_id']).isdigit()) ,'Не указан comp_id. обратитесь к разработчику'],
       #[ (R['phone']),'Телефон не указан'],
       [ is_phone(R['phone']),'Телефон указан не корректно' ],
       [ (R['email_for_notify']),'Email для оповещений не указан'],
       [ is_email(R['email_for_notify']),'Email для оповещений указан не корректно, укажите валидный email' ],
       [ (R['header']),'Заполните наименование компании'],
       [ (  not(R['inn']) or len(R['inn'])==10 or len(R['inn'])==12 ),'ИНН должен быть 10 или 12 цифр'],
       
       
    ]
    check_rules(rules,errors)
    #print('R:',R['comp_id'])
    ur_lico=get_ur_lico(R['comp_id'])
    if not ur_lico:
        errors.append('Не удалось найти такое юридическое лицо в базе')

    if not len(errors):
        R['manager_id']=s.manager['id']
        s.db.save(
            table="change_comp_order",
            data=R,
            errors=errors
        )
        
        anna_manager=get_anna_manager()
        if anna_manager and exists_arg('email',anna_manager):
            send_mes(
                to=anna_manager['email'],
                subject=f"Заявка на изменение данных с {s.env['host']}",
                message=f"""
                    Наименование компании: {R['header']}<br>
                    ИНН: {R['inn']}<br>
                    Email для оповещений: {R['email_for_notify']}
                """
            )

    if len(errors):
        success=0

    return {'success':success,'errors':errors}