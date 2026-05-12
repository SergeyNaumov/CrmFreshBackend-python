from .lib import need_manager_fld


async def action_init_new_docpack_form(form,field):
    # выводим поле "менеджер"
    need_manager=need_manager_fld(form)
        
    
    
    manager_list=[]
    if field.get('ur_lico_list'):
        print('locale ur_lico_list')
        ur_lico_list = await field['ur_lico_list'](form,field)

    else:
        print('login: ',form.manager['login'])
        add_where = ''
        if form.manager['login'] not in ['pzm','admin'] and form.ov.get('brand_id') and form.ov.get('brand_id') == 1:
            add_where = 'where id <> 28'
        ur_lico_list=await form.db.query(query=f'select id v,firm d from ur_lico {add_where} order by firm')
    
    tarif_list=await form.db.query(
        query='select id v,header d from tarif where enabled=1 order by header'
    )
    buhgalter_card_requisits_list=await form.db.query(
        query='select id v,concat(firm," ; ИНН:", inn) d from buhgalter_card_requisits where user_id=%s',
        values=[form.id]
    )
    
    if need_manager:
        manager_list=await form.db.query(
            query='select id v,name d from manager where enabled=1 order by name',
        )
            
    
    return {
        'success':form.success(),
        'errors':form.errors,
        'ur_lico_list':ur_lico_list,
        'tarif_list':tarif_list,
        'buhgalter_card_requisits_list':buhgalter_card_requisits_list,
        # для админа и менежера платежей
        'need_manager_field':need_manager,
        'manager_list':manager_list,
        'cur_manager_id':form.manager['id']
    }    
