
from lib.core import exists_arg, date_to_rus

def permissions(form):

    if not form.manager['access_to_conf']:
        form.errors.append('Вам запрещён доступ к конференциям')
        return
    
    query=f"""
         SELECT 
            wt.id, wt.header, wt.start,
            wt.link,wt.conf_id,wt.access_code,wt.comment
         from
            conference wt
            LEFT JOIN conference_stat cf ON wt.id=cf.conference_id and cf.manager_id={form.manager['id']}
            LEFT JOIN video_lessions vl ON vl.conference_id=wt.id
            LEFT JOIN video_lessions_stat_open vlso ON vlso.video_id=vl.id and vlso.manager_id={form.manager['id']}
        WHERE
            wt.enabled=1 and wt.not_cert=0 and (cf.id is not null or vlso.sec_opened >=600  ) GROUP by wt.id order by wt.start desc

    """ #  , link, conf_id, access_code, comment
    
    if 'limit' in form.R and form.R['limit']:
        query+=f" limit {form.R['limit']}"

    #print(form.R)


    
    form.data=form.db.query(
        query=query,
        values=[],
        log=form.log,
        errors=form.errors,
        arrays=1
    )


    #form.data=[]
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

            d['cert_exists']=f'<a href="/backend/anna/download/certpdf/{d["id"]}">получить</a>'
            
            for for_del in ('id','link','conf_id','access_code','comment'):
                del d[for_del]
            #f"""<a href="" target="_blank">{d['header']}</a>"""
        # if d['link']:
        #     d['link']=f"""<a href="{d['link']}" target="_blank">{d['link']}</a>"""
        

events={
    'permissions':[permissions]
}
