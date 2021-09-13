
# Возвращает список аптек
def get_apt_list(form,manager_id):
    manager=form.db.get(table='manager',where='id=%s',values=[manager_id],onerow=1)
    if manager['type']==3:
        r=form.db.query(
                query='''
                    SELECT
                        wt.*, 0 more, concat(m.name_f,' ',m.name_i,' ',m.name_o)  ma_fio, m.email ma_email,
                        m.phone ma_phone
                    FROM
                        ur_lico_manager ulm
                        join apteka wt ON wt.ur_lico_id=ulm.ur_lico_id
                        left join manager m ON wt.anna_manager_id=m.id
                    WHERE
                        wt.manager_id=%s
                ''',
                values=[manager_id],
                onerow=1,
                errors=form.errors
        )
        if(r): return [r]
        return []
        
    else:
        return form.db.query(
            query="""
                SELECT
                    wt.*, 0 more, concat(m.name_f,' ',m.name_i,' ',m.name_o)  ma_fio, m.email ma_email,
                    m.phone ma_phone
                FROM
                    ur_lico_manager ulm
                    join apteka wt ON wt.ur_lico_id=ulm.ur_lico_id
                    left join manager m ON wt.anna_manager_id=m.id
                WHERE
                    ulm.manager_id=%s

            """,
            errors=form.errors,
            values=[manager_id]
        )

def get_apt_list_ids(form,manager_id=0):
    if not manager_id:
        manager_id=form.manager['id']
    res_lst=[]
    lst=[]
    

    lst=get_apt_list(form,manager_id)
    for a in lst:
        
        res_lst.append(str(a['id']))
    

    

    return res_lst

def get_apt_managers_ids(form,manager_id):
    ids=get_apt_list_ids(form,manager_id)
    rez=form.db.query(
        query=f'''
        select
            manager_id 
        from
            apteka
        where id in ({",".join(ids)}) and manager_id is not null group by manager_id 
        ''',
        #debug=1,
        massive=1
    )
    if len(rez)==0:
        rez.append('0')
    return rez

def apt_list_id_for_apt(form,manager_id):
    rez=[]
    apteka_id=form.db.query(
      query='select id from apteka where manager_id=%s',
      values=[manager_id],
      onevalue=1
    )
    if apteka_id:
        rez.append(str(apteka_id))
    return rez


def get_all_ids_for_aptcomp(form,apteka_id):
    # получит все id-шники аптек в рамках этого же юрлица
    res=form.db.query(
        query='''
            SELECT
                a2.id
            from
                apteka a1
                join apteka a2 ON a2.ur_lico_id=a1.ur_lico_id
            WHERE a1.id=%s
        ''',
        massive=1,
        values=[apteka_id]
    )

    res2=[]
    for r in res:
        res2.append(str(r))
    #form.pre(res2)
    return res2
