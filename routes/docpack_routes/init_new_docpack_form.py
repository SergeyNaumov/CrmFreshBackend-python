from .lib import need_manager_fld


def action_init_new_docpack_form(form,field):
    # выводим поле "менеджер"
    need_manager=need_manager_fld(form)
        
    
    
    manager_list=[]
        
    if field.get('ur_lico_list'):
        ur_lico_list=field['ur_lico_list'](form,field)

    else:
        ur_lico_list=form.db.query(query='select id v,firm d from ur_lico order by firm')
    
    tarif_list=form.db.query(
        query='select id v,header d from tarif where enabled=1 order by header'
    )
    
    if need_manager:
        manager_list=form.db.query(
            query='select id v,name d from manager where enabled=1 order by name',
        )
            
    
    return {
        'success':form.success(),
        'errors':form.errors,
        'ur_lico_list':ur_lico_list,
        'tarif_list':tarif_list,
        
        # для админа и менежера платежей
        'need_manager_field':need_manager,
        'manager_list':manager_list,
        'cur_manager_id':form.manager['id']
    }    
