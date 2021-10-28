
from lib.core import exists_arg, date_to_rus

def permissions(form):

    if not form.manager['access_to_conf']:
        form.errors.append('Вам запрещён доступ к конференциям')
        return
    query=f"""
         SELECT 
            id, header, start,
            link,conf_id,access_code,comment
         from
            conference
        WHERE
            enabled=1 order by start desc
    """ #  , link, conf_id, access_code, comment

    if form.manager['type']==1:
        form.links=[
            {
                'type':'url',
                'link':'/admin_table/conference',
                'description':'Редактирование конференций'
            },
        ]

    form.data=form.db.query(
        query=query,
        log=form.log,
        errors=form.errors,
        arrays=1
    )


    #print('data:',form.data)
    for d in form.data:
        d['start']=date_to_rus(d['start'])
        if d['header']:
            #Формируем объект-dialog
            d['header']={
                'header':d['header'],
                'type':'url',
                'url':f"/page/conference/{d['id']}",
                
            }
            # d['header']={
            #     'header':d['header'],
            #     'type':'dialog',
            #     'dialog_html':form.template('./conf/conference_table/templates/dialog.html',d=d),
            #     #'url':f"/table/{form.config}/ajax-dialog/{d['id']}"
            # }
            for for_del in ('id','link','conf_id','access_code','comment'):
                del d[for_del]
            #f"""<a href="" target="_blank">{d['header']}</a>"""
        # if d['link']:
        #     d['link']=f"""<a href="{d['link']}" target="_blank">{d['link']}</a>"""
        

events={
    'permissions':[permissions]
}
