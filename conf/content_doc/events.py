def permissions(form):
    
    if form.manager['type']==2:
        form.work_table='content_doc_ur_lico'
        form.title='Руководство (для юридических лиц)'
    elif form.manager['type']==3:
        form.work_table='content_doc_apteka'
        form.title='Руководство (для аптек)'

    if form.manager['type']==1:
        form.links=[
            {
                'type':'url',
                'link':'/admin_tree/content_doc',
                'description':'Редактирование руководства менеджеров'
            },
            {
                'type':'url',
                'link':'/admin_tree/content_doc_ur_lico',
                'description':'Редактирование руководства юрлиц'
            },
            {
                'type':'url',
                'link':'/admin_tree/content_doc_apteka',
                'description':'Редактирование руководства аптек'
            }

        ]
    

def events_before_code(form):
    pass

def before_delete(form):
    pass

events={
  'permissions': permissions,
  'before_delete':before_delete,
  'before_code':events_before_code
}