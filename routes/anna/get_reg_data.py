from lib.engine import s
from .permissions import get_manager_data
def get_reg_data():
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