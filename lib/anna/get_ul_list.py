def get_ul_list_ids(form,manager_id):
    
    rez=form.db.query(
        query="select ur_lico_id from ur_lico_manager where manager_id=%s",
        values=[manager_id],
        massive=1
    )

    if not len(rez):
        rez.append('0')

    return [str(x) for x in rez]

# Получаем все смежные юрлица для юрлица
def get_ul_list_from_ur_lico_id(form,ur_lico_id):
    rez=form.db.query(
        query="""
            select
                ur_lico_id
            from
                ur_lico_manager
            where
                manager_id in (select manager_id from ur_lico_manager where ur_lico_id=%s)
        """,
        values=[ur_lico_id],
        str=1,
        massive=1
    )
    return rez
