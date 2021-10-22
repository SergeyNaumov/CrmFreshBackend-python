from lib.engine import s
from .permissions import get_manager_data
from lib.core import exists_arg, date_to_rus

def get_reg_data():
    response={
        'success':1,
        'comp_list':[],
        'apt_list':[],
    }
    errors=[]
    manager=get_manager_data(s.manager['id'],errors)
    if not manager:
        errors.append('Главная страница АннА, ошибка авторизации, обратитесь к разработчику')
    if not len(errors):
        response['manager']=manager
        # Менеджер Анна
        
        if manager['type'] == 1:
            manager['ur_lico_list']=s.db.query(
                query='''
                    SELECT
                        *
                    FROM
                        ur_lico
                    WHERE
                        anna_manager_id=%s
                ''',
                values=[manager['id']]
            )
        # Представитель юридического лица
        if manager['type'] == 2:
            response['comp_list']=s.db.query(
                query="""
                    SELECT
                        wt.*, 0 more, concat(m.name_f,' ',m.name_i,' ',m.name_o)  ma_fio, m.email ma_email,
                        m.phone ma_phone, subscribe
                    FROM
                        ur_lico_manager ulm
                        join ur_lico wt ON wt.id=ulm.ur_lico_id
                        left join manager m ON wt.anna_manager_id=m.id
                    WHERE
                        ulm.manager_id=%s

                """,
                errors=errors,
                values=[s.manager['id']]
            )
            
            


            apteka_ids=[]
            for c in response['comp_list']:

                c['apteka_list']=s.db.query(
                    query="""
                        SELECT
                            wt.id,wt.ur_address,0 more,
                            wt.email, wt.inn, wt.header, wt.phone,
                            m.id m_id,
                            m.login m_login,
                            m.name_f m_name_f, m.name_i m_name_i, m.name_o m_name_o,
                            m.phone m_phone,
                            apt_set.apteka_id apt_set_id, apt_set.set1, apt_set.set2,

                            0 saved_s1, 0 saved_s2,
                            0 edit_form 
                        from 
                            apteka wt
                            LEFT JOIN manager m ON m.id=wt.manager_id
                            LEFT JOIN apteka_settings apt_set ON apt_set.apteka_id=wt.id
                            
                        where wt.ur_lico_id=%s
                    """,
                    values=[c['id']] 
                )

                c['orders_change_apteka']=[]


                apteka_ids_in_comp=[]
                for a in c['apteka_list']:
                    apteka_ids.append(str(a['id']))
                    apteka_ids_in_comp.append(str(a['id']))

                    if not a['apt_set_id']:
                        s.db.save(
                            table="apteka_settings",
                            data={
                                'apteka_id':a['id'],'set1':1,'set2':1
                            }
                        )
                        a['set1']=1
                        a['set2']=1

                c['subscribe_actions']=[] # список акций, на которые подписаны аптеки

                if len(apteka_ids_in_comp):
                    c['orders_change_apteka']=s.db.query(
                        query=f'''
                            SELECT
                                a.ur_address, o.id, o.registered
                            FROM
                                apteka a
                                join order_change_account o ON a.manager_id=o.manager_id
                            WHERE a.id IN ({','.join(apteka_ids_in_comp)}) order by registered desc
                            LIMIT 10 

                        '''
                    )
                    for o in c['orders_change_apteka']:
                        o['registered']=date_to_rus(str(o['registered']))


                    # Список акций, на которые подписаны аптеки юрлица
                    c['subscribe_actions']=s.db.query(
                        query=f'''
                            select
                                a.id, a.header, a.date_start, a.date_stop
                            from
                                action a
                                join action_apteka aa ON aa.action_id=a.id
                            WHERE
                                a.date_stop>=curdate() and aa.apteka_id in ( {','.join(apteka_ids_in_comp) } )
                            group by a.id order by a.header 
                        '''

                    )

                    
                #print('orders:',response['orders_change_apteka'])
            # Представитель аптеки
        if manager['type'] == 3:
            


            response['apt_list']=s.db.query(
                query='''
                    SELECT
                        a.*, 0 more, ul.header ul_header, ul.phone ul_phone
                    FROM
                        apteka a
                        LEFT JOIN ur_lico ul on ul.id=a.ur_lico_id
                    WHERE a.manager_id=%s
                ''',
                values=[s.manager['id']]
            )

            # s.db.get(
            #     table='apteka',
            #     select_fields='*, 0 more',
            #     where='manager_id = %s',
            #     values=[s.manager['id']],
            #     errors=errors
            # )
    response['errors']=errors
    if len(errors): response['success']=0
    return response

# Проверяем, имеем ли мы доступ к аптеке
def access_apteka_ok(manager_id,apteka_id):
    return s.db.query(
        query='select id from apteka where manager_id=%s and id=%s',
        onevalue=1,
        values=[manager_id,apteka_id]
    )
def access_ur_lico_ok(manager_id,ur_lico_id):
    return s.db.query(
        query='''
            select 
                ur_lico_id
            from
                ur_lico_manager
                
            where
                ur_lico_id=%s and manager_id=%s
        ''',
        values=[ur_lico_id,manager_id],
        #debug=1,
        onevalue=1
    )
def get_ur_lico_list_for_account(manager_id):
    return s.db.query(
        query="""
            SELECT
                ul.id, ul.header
            from
                ur_lico_manager ulm
                join ur_lico ul ON ulm.ur_lico_id=ul.id
            WHERE ulm.manager_id=%s
        """,
        values=[manager_id],
    )



# def apteka_ids_dict(reg_data):
#     pass

# def ur_lico_ids_dict(reg_data)
#     print reg_data