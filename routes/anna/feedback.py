from lib.engine import s
from lib.form_control import check_rules, is_email, is_phone
#from .permissions import get_ur_lico, get_anna_manager,get_manager_data
from lib.core import exists_arg
from lib.send_mes import send_mes
from lib.engine import s

def feedback(R):
    errors=[]
    success=True
    if not(exists_arg('question', R)) or not(R['question']):
        success=False
        errors.append('Укажите свой вопрос')
    
    #print('manager:',s.manager)
    m=s.manager
    email=m['email']
    phone=m['phone']
    if not(email): email=m['login']
    if not(phone): phone='-'

    message=f'''
        ФИО: {m["name"]}<br>
        Почта: {email}<br>
        Телефон: {phone}<br>
    '''
    if m['type']==2:
        ur_lico=s.db.query(
            query="select group_concat(ul.header SEPARATOR ', ') from ur_lico_manager ulm join ur_lico ul ON ul.id=ulm.ur_lico_id where ulm.manager_id=%s",
            values=[m['id']],
            onevalue=1
        )
        message+=f'''Юр.Лицо: {ur_lico}<br>'''
    if m['type']==3:
        apteka=s.db.query(
            query='''select concat(a.ur_address,' (',ul.header,')')  from apteka a join ur_lico ul on ul.id=a.ur_lico_id where a.manager_id=%s''',
            values=[m['id']],
            onevalue=1
        )
        if apteka: message+=f'''Аптека: {apteka}<br>'''
    if m['type']==4:
        pharm=s.db.query(
            query='''
                select 
                    concat(m.name,' / ',a.ur_address,' / ',ul.header) 
                from 
                manager_pharmacist mph
                join manager m ON m.id=mph.id
                join apteka a ON a.id=mph.apteka_id
                join ur_lico ul on ul.id=a.ur_lico_id where mph.id=453%s''',
            values=[m['id']],
            onevalue=1
        )
        if pharm: message+=f'''Фармацевт: {pharm}<br>'''

    message+=f'''Текст вопроса: {R['question']}'''
    #print('email:',email, m['email'],m['login'])
    #print(message)
    s.db.save(
        table='feedback',
        data={
            'question':R['question'],
            'manager_id':m['id']
        }
    )
    send_mes(
        to='webadmin@digitalstrateg.ru',
        subject=f'''Заявка "связь с Альянсом Фарм. Ассоциаций" {s.env['host']}''',
        message=message
    )
    return {
        'success':success,
        'errors':errors}
    



