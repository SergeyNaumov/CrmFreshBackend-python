from lib.core import cur_date, join_ids
from lib.core_crm import child_groups
from datetime import datetime
from config import config
# получаем комментарии для списка


async def search(form, R):
    #R['cgi_params']['type']='43'
    filters=R['filters']
    log=[]
    form.errors.append('111')

    where=[]
    values=[]

    registered=filters.get('registered','').split(' ')[0]

    if registered:

        where.append('wt.registered>=%s and wt.registered<=%s')
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
            where.append(f"wt.manager_id IN ({join_ids(manager_list)})")

    #фильтр "группа"
    group_id=filters.get('group_id',[])
    if isinstance(group_id, list):
        group_list=[]
        group_hash={}
        group_list=await child_groups(db=form.db, group_id=group_id)
        #log.append({'hash':group_hash})
        if len(group_list):
            where.append(f"m.group_id IN ({join_ids(group_list)})")

    #log.append({
    #    'where':where,
    #    'values':values
    #})
    accordion_data=[]
    if registered and len(where):

        query=f"""
            SELECT
                hour(wt.registered) `hour`, time(wt.registered) registered, wt.manager_id, wt.body, m.name, u.firm, wt.user_id
            FROM
                user_memo wt
                LEFT JOIN user u ON u.id=wt.user_id
                LEFT JOIN manager m ON m.id=wt.manager_id

            WHERE {' AND '.join(where)} ORDER BY wt.registered
        """
        #log=query
        result=await form.db.query(
            query=query,
            values=values,
            #log=log
        )
        managers_hash={}
        managers_ids=[]
        hour=-1
        for r in result:
            if not(r['firm']):
                r['firm']='***'
            if(r['hour'] != hour):
                r['new_hour']=1
                hour=r['hour']
            else:
                r['new_hour']=0

            if manager_id:=r.get('manager_id'):

                if not(managers_hash.get(manager_id)):
                    managers_ids.append(manager_id)
                    managers_hash[manager_id]=1

        if len(managers_ids):
            managers_hash={}
            for m in await form.db.query(query=f"select name, id from manager where id in ({join_ids(managers_ids)}) order BY name"):
                item={'name':m['name'],'comments':[]}

                for r in result:
                    if r['manager_id']==manager_id:
                        item['comments'].append(r)

                managers_hash[m['id']]=item

                accordion_data.append({
                    "header": m['name'],

                    #"header_links":[{'url':'sasa','style':'','header':'link1'}],
                    'not_container':True,
                    "content":[
                        {
                            'type':'html',

                            'body': form.template(
                                    filename=f'./{config["config_folder"]}/stat_comments_op/template/table.html', list_comments=item['comments']
                            ),
                        }
                    ]
                })



        #log=[managers_hash]
        #print("all_managers :", join_ids(managers_ids) )
        #log.append({'hash': managers_hash.keys() });
    else:
        form.errors.append('Необходимо выбрать дату')


    result_list=[]
    if len(accordion_data):
        result_list.append(
            { # раскрывающийся блок
                'type':'accordion',
                'data': accordion_data



            },
        )


    #print(query)
    accordion_data=[]
    # for m in lst:
    #     accordion_data.append({
    #         "header":form.template(
    #             filename='./conf/transfere_result/template/accordion_header.html', **m
    #         ),
    #         #"header_links":[{'url':'sasa','style':'','header':'link1'}],
    #         'not_container':True,
    #         "content":[
    #             {
    #                 'type':'html',

    #                 'body': get_table_for_manager(form, _type,  m['id'], ts)
    #             }
    #         ]
    #     })



    # if len(accordion_data):
    #     result_list.append(
    #         { # раскрывающийся блок
    #             'type':'accordion',
    #             'data': accordion_data
    #         },
    #     )
    return {
        'success':True,
        'errors':[],
        'log':log,
        'list':result_list
    }

    

# async def permissions(form):
#     ...
    
form={
        'title':'Комментарии за день',
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
            #'permissions':permissions,
            'search':search
        }
    
}

