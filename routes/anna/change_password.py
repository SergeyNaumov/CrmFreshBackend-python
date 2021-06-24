from lib.engine import s
from .permissions import get_manager_data,password_ok, get_anna_manager, get_ur_lico
from .get_reg_data import get_ur_lico_list_for_account
from lib.send_mes import send_mes
from lib.form_control import is_email # , is_phone, check_rules, 
from lib.core import exists_arg

# update manager set password=sha2('123',256)

def change_password(R:dict):
    error=''
    success=1
    p1=R['password1']
    p2=R['password2']
    #print('R2:',R)
    # Убрать false
    if False and not password_ok(R['password']) :
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

        # Отправляем сообщение об изменениях пароля самому аккаунту
        manager=get_manager_data()
        #print('manager:',manager)
        if is_email(R['login']):
            send_mes(
                to=R['login'],
                subject='Изменение пароля в системе АннА',
                message=f"""
                    <p>Вы получили это письмо, потому что произошла смена пароля в учетной записи, новые данные для входа:</p>
                    Логин: {manager['login']}<br>
                    Новый пароль: {p1}
                """
            )
        #print('manager:',manager)
        # Если это не менеджер АннА -- отправляем менеджеру АннА
        if str(manager['type'])!="1" and exists_arg('ma_email',manager):
            #anna_manager=get_anna_manager()
            subject=""
            message=""
            
            if manager['type']==2:
                ur_lico_list=manager['ur_lico_list']

                
                subject=f"Представитель юридического лица изменил пароль"
                message=f"{manager['ma_name_f']} {manager['ma_name_i']} {manager['ma_name_o']} - Только что {manager['name_f']} {manager['name_i']} {manager['name_i']} ({manager['login']}), представитель"
                if len(ur_lico_list)>1:
                    message+=" юридических лиц:<br>\n"
                else:
                    message+=" юридического лица:<br>\n"

                for u in ur_lico_list:
                    u['id']=str(u['id'])
                    message=message+f"""<a href="https://{s.env['host']}/edit-form/ur_lico/{ u['id'] }">{u['header']}</a><br>\n"""
                
                message+=f"изменил(а) свой пароль на <b>{p1}</b>"


            #print('TYPE:',manager['type'],str(manager['type'])=="3")
            if manager['type']==3:
                
                apteka=manager['apteka']
                

                if apteka:

                    subject=f"Представитель аптеки: {apteka['ur_address']} изменил пароль"
                    message=f"""
                        Только что {manager['name_f']} {manager['name_i']} {manager['name_i']} ({manager['login']}), представитель аптеки:
                        <a href="https://{s.env['host']}/edit-form/apteka/{ apteka['id'] }">{apteka['ur_address']}</a>
                    """
                    message+=f"<br>изменил(а) свой пароль на <b>{p1}</b>"

                    # Письмо представителю юридического лица
                    ur_lico=manager['ur_lico']
                    
                    if is_email(ur_lico['email_for_notify']):
                        send_mes(
                            to=ur_lico['email_for_notify'],
                            subject=subject,
                            message=message
                        )
            
            # Письмо менеджеру АннА о смене пароля
            send_mes(
                to=manager['ma_email'],
                subject=subject,
                message=message
            )

            # Если это аптека, тогда юридическому лицу тоже отправляем уведомление
            if str(manager['type'])=="3":
                message=""



    return {'success':success,'error':error}
