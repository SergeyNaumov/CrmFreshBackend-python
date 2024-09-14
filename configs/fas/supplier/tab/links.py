async def links_before_code(form,field):
    
    if not(form.action == 'edit' and form.id):
        return


    field['after_html']=f'<div><a href="/edit_form/buhgalter_card/{form.id}" target="_blank">Реквизиты компании</a></div>'
    
fields=[
    {
            'tab':'links',
            'name':'links',
            'type':'code',
            'before_code':links_before_code            
    },
]
