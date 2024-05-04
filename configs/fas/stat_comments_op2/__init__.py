from lib.core import cur_date, join_ids
from lib.core_crm import child_groups
from datetime import datetime
from config import config
# получаем комментарии для списка


def search(form, R):
    #R['cgi_params']['type']='43'
    filters=R['filters']
    log=[]
    form.errors.append('111')

    where=[]
    values=[]

    registered=filters.get('registered','').split(' ')[0]

    if registered:

        where.append('( (um.registered>=%s and um.registered<=%s) and  (r.date>=%s and r.date<=%s) )')
        # um.registered>='2024-02-08 00:00:00' and um.registered<='2024-02-08 23:59:59' and r.date>='2024-02-08 00:00:00' and r.date<='2024-02-08 23:59:59'
        values.append(f"{registered} 00:00:00")
        values.append(f"{registered} 23:59:59")
        values.append(f"{registered} 00:00:00")
        values.append(f"{registered} 23:59:59")

    # фильтр "менеджер"
    manager_id=filters.get('manager_id',[])
    if isinstance(manager_id, list):
        manager_list=[]
        for v in manager_id:
            if isinstance(v, int):
                manager_list.append(v )

        if len(manager_list):
            where.append(f"m.id IN ({join_ids(manager_list)})")

    #фильтр "группа"
    group_id=filters.get('group_id',[])
    if isinstance(group_id, list):
        group_list=[]
        group_hash={}
        group_list=child_groups(db=form.db, group_id=group_id)
        #log.append({'hash':group_hash})
        if len(group_list):
            where.append(f"m.group_id IN ({join_ids(group_list)})")

    result_list=[]
    accordion_data=[]



    if registered:
        # Комментарии с записями
        query=f"""
            select
                u.id user_id, u.firm, m.name, hour(um.registered) hour, um.registered, um.body,
                uc.phone, if(uc.fio,uc.fio,'') contact_name,
                group_concat( concat(time(r.date),';',r.download_link,';',if(r.direction='OUTBOUND','исх','вх'),';',r.duration) SEPARATOR ';;;' ) records
            from
                manager m
                join user u ON u.manager_id=m.id
                join user_memo um ON um.user_id=u.id and um.manager_id=m.id
                join user_contact uc ON uc.user_id=u.id
                LEFT join beeline_records r ON r.manager_id=m.id and r.phone=uc.phone and (r.date>=%s and r.date<=%s)
            WHERE
                (um.registered>=%s and um.registered<=%s)
            GROUP BY um.id
            ORDER BY um.registered
        """


        result=form.db.query(
            query=query,
            values=values,
            #debug=1,
            #log=log
        )

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
                records=[]
                #print(r)
                if prev_hour != r['hour']:
                    r['new_hour']=1
                    prev_hour=r['hour']
                    j=1
                else:
                    r['new_hour']=0

                r['j']=j
                if not(r['records']):
                    r['records']=''

                for i in r['records'].split(';;;'):
                    i=i.split(';')
                    if len(i)>2:

                        records.append({
                            'id':rid,
                            'registered':i[0],
                            'src':i[1],
                            'direction':i[2],
                            'duration':i[3]
                        })
                        rid+=1

                r['records']=records
                j+=1


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

