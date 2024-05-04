from lib.core import cur_date, join_ids
from lib.core_crm import child_groups
from datetime import datetime
from config import config
from pprint import pprint
# получаем комментарии для списка


def search(form, R):
    #R['cgi_params']['type']='43'
    filters=R['filters']
    log=[]
    form.errors.append('111')

    where=[] ; where_records=[]
    values=[]

    registered=filters.get('registered','').split(' ')[0]

    if registered:

        where.append('( (um.registered>=%s and um.registered<=%s) )')
        where_records.append('( (r.date>=%s and r.date<=%s) )')

        # um.registered>='2024-02-08 00:00:00' and um.registered<='2024-02-08 23:59:59' and r.date>='2024-02-08 00:00:00' and r.date<='2024-02-08 23:59:59'
        #values.append(f"{registered} 00:00:00")
        #values.append(f"{registered} 23:59:59")
        #values.append(f"{registered} 00:00:00")
        #values.append(f"{registered} 23:59:59")

    # фильтр "менеджер"
    manager_id=filters.get('manager_id',[])
    if isinstance(manager_id, list):
        manager_list=[]
        for v in manager_id:
            if isinstance(v, int):
                manager_list.append(v )

        if len(manager_list):
            where.append(f"m.id IN ({join_ids(manager_list)})")
            where_records.append(f"m.id IN ({join_ids(manager_list)})")

    #фильтр "группа"
    group_id=filters.get('group_id',[])
    if isinstance(group_id, list):
        group_list=[]
        group_hash={}
        group_list=child_groups(db=form.db, group_id=group_id)
        #log.append({'hash':group_hash})
        if len(group_list):
            where.append(f"m.group_id IN ({join_ids(group_list)})")
            where_records.append(f"m.group_id IN ({join_ids(group_list)})")

    result_list=[]
    accordion_data=[]



    if registered:
        # Комментарии с записями
        # query=f"""
        #     select
        #         u.id user_id, u.firm, m.name, hour(um.registered) hour, um.registered, um.body,
        #         uc.phone, if(uc.fio,uc.fio,'') contact_name,
        #         group_concat( concat(time(r.date),';',r.download_link,';',if(r.direction='OUTBOUND','исх','вх'),';',r.duration) SEPARATOR ';;;' ) records,
        #         um.id um_id
        #     from
        #         user_memo um
        #         join manager m ON m.id=um.manager_id
        #         join user u ON u.manager_id=m.id and um.user_id=u.id
        #         LEFT join beeline_records r ON r.manager_id=m.id and (r.date>=%s and r.date<=%s)
        #         join user_contact uc ON uc.user_id=u.id and uc.phone=r.phone
        #     WHERE
        #         {' AND '.join(where)}
        #     GROUP BY um.id
        #     ORDER BY um.registered
        # """

        # #print('query:',query)
        # result=form.db.query(
        #     query=query,
        #     values=values,
        #     #debug=1,
        #     #log=log
        # )

        query=f"""
            select
                u.id user_id, u.firm, m.name, hour(um.registered) hour, um.registered, um.body,
                '' phone, '' contact_name,
                group_concat(uc.phone) phones, unix_timestamp(um.registered) ts
            from
                user_memo um
                join manager m ON m.id=um.manager_id
                join user u ON u.manager_id=m.id and um.user_id=u.id
                left join user_contact uc ON uc.user_id=u.id
            WHERE
                {' AND '.join(where)}
            GROUP BY um.id
            ORDER BY um.registered
        """

        # Комментарии без записей
        result=form.db.query(
            query=query,
            values=[f"{registered} 00:00:00", f"{registered} 23:59:59"],
            #debug=1,
            #log=log
        )
        all_phones=[]

        phone_dict={} # список item-ов для memo, привязанных к телефону

        for memo_item in result:
            memo_item['records']=[]
            if memo_item['phones']:
                memo_item['phones']=memo_item['phones'].split(',')
                for p in memo_item['phones']:
                    if p:
                        if not phone_dict.get(p):
                            phone_dict[p]=[]

                        all_phones.append(p)
                        phone_dict[p].append(memo_item)
            else:
                memo_item['phones']=[]

            #print(memo_item)


        if len(all_phones):
            # Дёргаем звонки
            where_records.append(f"""r.phone in ("{'","'.join(all_phones)}")""")
            #print('where_records:',where_records)
            records=form.db.query(
                query=f"""
                    SELECT
                        r.id, concat('',time(r.date)) registered, if(r.direction='OUTBOUND','исх','вх') direction,
                        r.duration, r.download_link src, r.phone, uc.fio,
                        unix_timestamp(r.date) ts
                    from
                        manager m
                        join beeline_records r ON r.manager_id=m.id
                        join user_contact uc on uc.phone=r.phone
                    WHERE {' AND '.join(where_records)} GROUP BY r.id

                """,
                #debug=1,
                values=[f"{registered} 00:00:00", f"{registered} 23:59:59"],
            )
            for rec in records:
                #print('r:',r)
                if memo_items:=phone_dict[rec['phone']]:
                    # Здесь получаем список всех записей из memo, привязанных к телефону
                    min_ts=10000 ; act_item=None
                    for mitem in memo_items:
                        cur_ts=abs(rec['ts'] - mitem['ts'])

                        if cur_ts < min_ts:
                            min_ts=cur_ts
                            act_item=mitem

                    if act_item:
                        act_item['records'].append(rec)


                    #print(memo_item)



        #print('result ok')
        # result_comments=form.db.query(
        #     query=f"""
        #         select
        #             u.id user_id, u.firm, m.name, hour(um.registered) hour, um.registered, um.body,
        #             uc.phone, if(uc.fio,uc.fio,'') contact_name,
        #             group_concat( concat(time(r.date),';',r.download_link,';',if(r.direction='OUTBOUND','исх','вх'),';',r.duration) SEPARATOR ';;;' ) records
        #         from
        #             manager m
        #             join user u ON u.manager_id=m.id
        #             join user_memo um ON um.user_id=u.id and um.manager_id=m.id
        #             LEFT join user_contact uc ON uc.user_id=u.id
        #             LEFT join beeline_records r ON r.manager_id=m.id and r.phone=uc.phone and (r.date>=%s and r.date<=%s)
        #         WHERE
        #             (um.registered>=%s and um.registered<=%s)
        #         GROUP BY um.id
        #         ORDER BY um.registered
        #     """,
        #     values=[f"{registered} 00:00:00", f"{registered} 23:59:59"]

        # )



        #
        #print('result:',result)
        rid=1
        if len(result):
            prev_hour=-1
            j=0
            for r in result:
                #records=[]
                #print(r)
                if prev_hour != r['hour']:
                    r['new_hour']=1
                    prev_hour=r['hour']
                    j=1
                else:
                    r['new_hour']=0

                r['j']=j


                j+=1

            #pprint(result[0:10])

            #print('END result')
            result_list.append(
                {
                    'type':'html',
                    'body': form.template(filename=f'./{config["config_folder"]}/stat_comments_op2/template/table.html', list=result),
                }
            )

        # managers_hash={}
        # managers_ids=[]
        # hour=-1
        # for r in result:
        #     if not(r['firm']):
        #         r['firm']='***'
        #     if(r['hour'] != hour):
        #         r['new_hour']=1
        #         hour=r['hour']
        #     else:
        #         r['new_hour']=0

        #     if manager_id:=r.get('manager_id'):

        #         if not(managers_hash.get(manager_id)):
        #             managers_ids.append(manager_id)
        #             managers_hash[manager_id]=1

        # if len(managers_ids):
        #     managers_hash={}
        #     for m in form.db.query(query=f"select name, id from manager where id in ({join_ids(managers_ids)}) order BY name"):
        #         item={'name':m['name'],'comments':[]}

        #         for r in result:
        #             if r['manager_id']==manager_id:
        #                 item['comments'].append(r)

        #         managers_hash[m['id']]=item

        #         accordion_data.append({
        #             "header": m['name'],

        #             #"header_links":[{'url':'sasa','style':'','header':'link1'}],
        #             'not_container':True,
        #             "content":[
        #                 {
        #                     'type':'html',

        #                     'body': form.template(
        #                             filename=f'./{config["config_folder"]}/stat_comments_op2/template/table.html', list_comments=item['comments']
        #                     ),
        #                 }
        #             ]
        #         })



        #log=[managers_hash]
        #print("all_managers :", join_ids(managers_ids) )
        #log.append({'hash': managers_hash.keys() });
    else:
        form.errors.append('Необходимо выбрать дату')



    #log.append('xxx')
    return {
        'success':True,
        'result_type':'',
        'errors':[],
        'log':log,
        'list':result_list,

    }



def permissions(form):
    ...

form={
        'title':'Комментарии и звонки',
        'filters':[
          {
            'description':'Группы',
            'name':'group_id',
            'type':'select_from_table',
            'table':'manager_group',
            'header_field':'header',
            'value_field':'id',
          },
          {
            'description':'Менеджеры',
            'name':'manager_id',
            'type':'select_from_table',
            'table':'manager',
            'header_field':'name',
            'value_field':'id'
          },
          {
            'description':'Дата комментария',
            'type':'date',
            'name':'registered',
            'value':datetime.today().strftime('%Y-%m-%d')
          }
        ],
        'events':{
            'permissions':permissions,
            'search':search
        },
        #'javascript':"""window.toggle=(sel)=>{el=document.querySelector(sel);if(el){el.style.display=(el.style.display=='none')?'':'none'};return false}"""


}

