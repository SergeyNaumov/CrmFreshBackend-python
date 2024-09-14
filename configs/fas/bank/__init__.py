from lib.core import cur_date, join_ids
from lib.core_crm import child_groups
from datetime import datetime
from config import config

async def search(form,R):
    result_list=[]
    filters=R['filters']
    log=[]
    result=[]

    manager_id=filters.get('manager_id')
    group_id=filters.get('group_id')
    from_date=filters.get('from_date')
    to_date=filters.get('to_date')
    #log.append(from_date)
    #log.append(to_date)

    where1=[] ; values1=[] ; where2=[]; values2=[]
    if from_date:
        where1.append('b.paid_date>=%s')
        values1.append(from_date)
        where2.append('b.paid_date>=%s')
        values2.append(from_date)

    if to_date:
        where1.append('paid_date<=%s')
        values1.append(to_date)
        where2.append('paid_date<=%s')
        values2.append(to_date)

    if manager_id:
        for v in manager_id:
            if v and isinstance(v, int):
                where1.append(f'm.id={v}')
                where2.append(f'm.id={v}')
    if group_id:
        for v in group_id:
            if v and isinstance(v, int):
                where1.append(f'mg.id={v}')
                where2.append(f'mg.id={v}')
    
    # if group_id and group_id.isnumeric():
    #     where1.append(f'mg.id={group_id}')
    #     where2.append(f'mg.id={manager_id}')

    if len(where1):
        query=f"""
            SELECT * 
            FROM
            (
                (
                SELECT
                    b.id bill_id, 'bill' as type, b.number, mg.header group_name,
                    b.manager_id, m.name manager_name, b.paid_summ, 0 manager_summ, b.paid_date
                FROM
                    bill b
                    LEFT join manager m ON b.manager_id=m.id
                    LEFT JOIN manager_group mg ON mg.id=m.group_id 
                    WHERE {' AND '.join(where1)}
                )
                UNION
                (
                SELECT
                    b.id bill_id, 'div' as type, b.number, mg.header group_name,
                    b.manager_id, m.name manager_name, b.paid_summ, bd.summ manager_summ, b.paid_date
                FROM
                    bill b
                    join bill_division bd ON b.id=bd.bill_id 
                    LEFT join manager m ON b.manager_id=m.id
                    LEFT JOIN manager_group mg ON mg.id=m.group_id 
                    WHERE {' AND '.join(where2)}
                )
            ) x ORDER BY paid_date
        """
        result = await form.db.query(
            query=query,
            values=values1+values2
        )
        #log=[result]
        total_bank={}
        for r in result:
            if r['type']=='bill':
                r['division'] = await form.db.query(
                    query="""
                        select
                            bd.summ, bd.manager_id
                        from
                            bill_division bd
                        WHERE
                            bd.bill_id=%s
                    """,
                    values=[r['bill_id']]
                )
                if len(r['division']):
                    r['manager_summ']=0
                    for d in r['division']:
                        if d['manager_id']==r['manager_id']:
                            r['manager_summ']+=d['summ']
                else:
                    # если разделений нет, то вся сумма счёта достаётся менеджеру
                    r['manager_summ']=r['paid_summ']
                #log.append(r['division'])
            #log.append(r)
            if r['manager_name'] in total_bank:
                total_bank[r['manager_name']]+=r['manager_summ']
            else:
                total_bank[r['manager_name']]=r['manager_summ']
        #log.append(total_bank)
        result_list.append(
            {
                'type':'html',
                'body': form.template(
                    filename=f'./{config["config_folder"]}/bank/template/table.html',
                    list=result,
                    total_bank=total_bank
                ),
            }
        )
    return {
        'success':True,
        'result_type':'',
        'errors':[],
        'log':log,
        'list':result_list,

    }

async def permissions(form):
    ...

form={
    'title':'Архив оплат',
    'work_table':'',
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
            'description':'С',
            'type':'date',
            'name':'from_date',
            'value':datetime.today().strftime('%Y-%m-01')
          },
          {
            'description':'По',
            'type':'date',
            'name':'to_date',
            'value':datetime.today().strftime('%Y-%m-%d')
          },
        ],
        'events':{
            'permissions':permissions,
            'search':search
        },
    
}