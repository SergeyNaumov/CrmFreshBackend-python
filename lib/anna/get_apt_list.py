
# Возвращает список аптек
def get_apt_list(form,manager_id):
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

def get_apt_list_ids(form,manager_id):
    res_lst=[]
    lst=get_apt_list(form,manager_id)
    for a in lst:
        res_lst.append(str(a['id']))
    
    if not len(res_lst):
        res_lst=['0']

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
    #return [str(x) for x in rez]
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

