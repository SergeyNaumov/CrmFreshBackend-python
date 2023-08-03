
from lib.core import exists_arg, date_to_rus

def permissions(form):

    if not form.manager['access_to_conf']:
        form.errors.append('Вам запрещён доступ к конференциям')
        return
    
    query=f"""
         SELECT 
            wt.id, wt.header, wt.start,
            wt.link,wt.conf_id,wt.access_code,wt.comment,
            if(wt.not_cert=1 or cf.id is null, null, wt.id) cert_exists
         from
            conference wt
            LEFT JOIN conference_stat cf ON wt.id=cf.conference_id and cf.manager_id=%s
        WHERE
            wt.enabled=1  GROUP by wt.id order by wt.start desc

    """ #  , link, conf_id, access_code, comment
    
    if 'limit' in form.R and form.R['limit']:
        query+=f" limit {form.R['limit']}"

    #print(form.R)

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
        values=[form.manager['id']],
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

            if d['cert_exists']:
                #d['cert_exists']=f'<a href="http://dev-crm.test/backend/anna/download/certpdf/{d["cert_exists"]}">получить</a>'
                d['cert_exists']=f'<a href="/backend/anna/download/certpdf/{d["cert_exists"]}">получить</a>'
            else:
                d['cert_exists']='-'
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
