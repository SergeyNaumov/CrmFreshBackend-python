def get_ul_list_ids(form,manager_id):
    
    rez=form.db.query(
        query="select ur_lico_id from ur_lico_manager where manager_id=%s",
        values=[manager_id],
        massive=1
    )

    if not len(rez):
        rez.append('0')

    return [str(x) for x in rez]

