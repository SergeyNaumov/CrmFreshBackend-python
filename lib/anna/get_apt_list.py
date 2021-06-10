
# Возвращает список аптек
def get_apt_list(form,manager_id):
    return form.db.query(
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