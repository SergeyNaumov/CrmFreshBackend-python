# Привязка приложения к СР
from lib.core import exists_arg, date_to_rus, join_ids

async def action_link_sr(form,field,R):
    db=form.db
    errors=[]

    app_id=R.get('app_id') ; sr_id=R.get('sr_id')

    if not(app_id):
        errors.append('не передан параметр app_id')

    if not(sr_id):
        errors.append('не передан параметр sr_id')

    if not(len(errors)):
        app = await db.query(
            query="""
                SELECT
                    a.*, s.type
                FROM
                    dogovor_app a
                    JOIN service s ON s.id=a.service_id
                WHERE
                    a.id=%s
            """,
            values=[R['app_id']],
            onerow=1
        )
        if app:

            t=app['type']
            if t==1:
                query=f"""
                    SELECT
                        wt.teamwork_ofp_id id,
                        concat(if(wt.regnumber, wt.regnumber,'-'),' от ', DATE_FORMAT(wt.born,%s) )  v,
                        date(wt.born) from_date
                    FROM
                        teamwork_ofp wt
                    WHERE
                        teamwork_ofp_id=%s
                """
            elif t==2:
                query=f"""
                    SELECT
                    FROM
                        user_fin wt
                    WHERE
                        wt.id=%s
                """
            if query:
                item=await db.query(
                    query=query,values=['%e.%m.%Y',sr_id],onerow=1
                )
                if item:
                    sr_link=''
                    if t==1:
                        sr_link=f"/edit_form/teamwork_ofp/{sr_id}"
                    elif t==2:
                        sr_link=f"/edit_form/user_fin/{sr_id}"

                    await db.query(
                        query="UPDATE dogovor_app SET card_id=%s WHERE id=%s",
                        values=[sr_id,app['id']]
                    )
                    return {
                        'success':True,
                        'sr_name':item['v'],
                        'sr_link':sr_link,
                        'card_id':sr_id
                    }
                else:
                    errors.append(f"не найдено СР с id={sr_id}")
            else:
                errors.append('неизвестный тип услуги у СР')
        else:
            errors.append('не найдено приложение к договору')


    return {'success':False,'errors':errors}