def links_before_code(form,field):
    
    if not(form.action == 'edit' and form.id):
        return

    field['after_html']=f'<div><a href="/edit_form/user/{form.id}?action=create_ofp_card" target="_blank">Создать карту ОФП</a></div>'

    # вывод карт ОФП в блоке ссылок
    ofp=form.db.query(
        query=f"select teamwork_ofp_id id,count(*) cnt from teamwork_ofp where user_id={form.id} limit 1",
        debug=1,
        onerow=1
    )
    #form.pre({'ofp':ofp})
    if ofp and ofp['cnt']:
        if ofp['cnt']>1:
            field['after_html']+=f'<div><a href="/admin_table/teamwork_ofp?user_id={form.id}" target="_blank">Показать все карты ({ofp["cnt"]})</a></div>'
        else:
            field['after_html']+=f'<div><a href="/edit_form/teamwork_ofp/{ofp["id"]}" target="_blank">Перейти в карту ОФП</a></div>'

    field['after_html']+=f'<div><a href="/edit_form/buhgalter_card/{form.id}" target="_blank">Карточка бухгалтера</a></div>'
    
fields=[
    {
            'tab':'links',
            'name':'links',
            'type':'code',
            'before_code':links_before_code            
    },
]