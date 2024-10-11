from lib.core import exists_arg, date_to_rus, join_ids
from pprint import pprint

async def process_list(db, t, _list):
    ids=[0]
    items_dict={}
    for l in _list:
        l['from_date']=date_to_rus(l['from_date'])
        ids.append(l['id'])
        items_dict[l['id']]=l

    comments=[]
    if t==1:
        comments=await db.query(
            query=f"""
                select
                    wt.teamwork_ofp_id id, wt.comment, max(wt.registered) reg
                from
                    teamwork_ofp_memo wt
                    join (
                        select
                            teamwork_ofp_id, max(id) id
                        from
                            teamwork_ofp_memo
                        WHERE
                            teamwork_ofp_id in ({join_ids(ids)})
                        GROUP BY teamwork_ofp_id
                    ) wtmax ON wt.teamwork_ofp_id=wtmax.teamwork_ofp_id and wt.id=wtmax.id
                GROUP BY wt.teamwork_ofp_id

            """
        )
    #pprint(items_dict)
    #print("\n\ncomments:")
    #pprint(comments)
    for c in comments:
        #print('c:',c)

        if l:=items_dict.get(c['id']):

            l['last_comment']=f"{date_to_rus(c['reg'])}: {c['comment']}"

    #pprint(_list)


async def action_load_sr_list(form,field,R):
    app_id=R.get('app_id')
    db=form.db
    if app_id:
        app = await db.query(
            query=f"""
                select
                    a.*,
                    s.type,
                    dp.user_id
                from
                    dogovor_app a
                    JOIN service s ON s.id=a.service_id
                    JOIN docpack dp ON dp.id=a.dogovor_id
                where a.id=%s""",
            values=[app_id],
            onerow=1
        )
        if app:
            t=app['type']

            if t==1:
                # юр. услуга

                query=f"""
                        SELECT
                            wt.teamwork_ofp_id id,
                            if(wt.regnumber<>'', wt.regnumber,'-') v, date(wt.born) from_date, '' comment,
                            concat("/edit-form/teamwork_ofp/",wt.teamwork_ofp_id) link
                        FROM
                            teamwork_ofp wt
                            LEFT JOIN dogovor_app a ON a.card_id=wt.teamwork_ofp_id
                            LEFT JOIN service s ON s.id=a.service_id
                        WHERE wt.user_id=%s and (a.id is null or s.type<>1) and wt.born >= (curdate() - interval 3 month)
                """


            elif t==2:
                # фин. услуга
                query=f"""
                        SELECT
                            wt.teamwork_ofp_id id,if(wt.regnumber, wt.regnumber,'-') v, date(wt.born) from_date, '' comment,
                            concat("/edit-form/user_fin/",wt.id) link
                        FROM
                            user_fin wt
                            LEFT JOIN dogovor_app a ON a.card_id=wt.id
                            LEFT JOIN service s ON s.id=a.service_id
                        WHERE wt.user_id=%s and not(s.type=1 and a.id is not null)
                """

            else:
                return {'success': True, 'error':''}

            _list = await db.query(
                    query=query,
                    values=[app['user_id']]
            )
            #pprint(_list)
            await process_list(db, t, _list)
            return {'success':True, 'list':_list}

        else:
            return {'success':False,'errors':[f"приложение к договору с id={app_id} не найдено"]}

