from lib.core import join_ids, date_to_rus
async def beeline_records_before_code(form,field):
    if form.id:



        contacts = await form.db.query(
           query="select phone from user_contact where user_id=%s and phone<>''",
           values=[form.id]
        )
        phone_list=[]
        for c in contacts:
            #form.pre({'c':c})
            phones=c['phone'].split(',')
            for p in phones:

                phone_list.append(f"'{p.strip()}'")

        #form.pre(phone_list)
        if len(phone_list):
            where=f"phone in ("+",".join(phone_list)+")"
            manager=form.manager
            if manager['login'] not in ('pzm','akulov','admin','sed'):
                
                if form.is_owner_group:
                    manager_ids = await form.db.query(query=f'select id from manager where group_id in ({join_ids(manager["CHILD_GROUPS"])})',massive=1)
                    where+=f' and manager_id in ({join_ids(manager_ids)})'
                else:
                    where+=f' and manager_id={manager["id"]}'

            records = await form.db.query(
                   query=f"select * from beeline_records where {where}",
            )

            #form.pre(records)
            if len(records):
                records_html=""
                for r in records:
                    #if r['downloaded'] and r['date']:
                    full_name=f"/files/beeline/{r['date'].strftime('%Y/%m/%d')}/{r['id']}.mp3"
                    #if form.manager['login']=='admin':
                        #form.pre(r)
                    # result=f"""{result}
                    # <div style='padding-top: 5px'>
                    #     <audio controls>
                    #       <source src="{full_name}" type="audio/ogg">
                    #       <source src="{full_name}" type="audio/mpeg">
                    #     </audio>
                    # </div>
                    #     """
                    records_html+=\
                    "<div style='padding-top: 5px'>"+\
                        f"{date_to_rus(r['date'])}"+\
                        "<audio controls>"+\
                          f"<source src='{full_name}' type='audio/ogg'>"+\
                          f"<source src='{full_name}'' type='audio/mpeg'>"+\
                        "</audio>"+\
                    "</div>"

                field['after_html']=f"<div style='border: 1px solid gray; padding: 10px; border-radius: 5px;'>Записи разговоров:{records_html}</div>"

beeline_records={
    'description':'',
    'name':'beeline_records',
    'tab':'sale',
    'type':'code',
    'before_code':beeline_records_before_code
}
