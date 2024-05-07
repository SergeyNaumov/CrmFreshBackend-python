from lib.core import cur_date, exists_arg, join_ids
from .search import search
from fastapi.responses import FileResponse
import random, time
from datetime import date, timedelta

import os
def gen_tmpl_prefix():
    now=str(int(time.time()))
    return str(int(time.time())) + \
    '_' +  ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUV0123456780') for i in range(5))






async def permissions(form):
    manager=form.manager
    perm=manager['permissions']
    #form.pre(manager)
    if perm['admin_paids']:
        # менеджеру платежей выводим  всё
        list_groups=await form.db.query(
            query="select id, header from manager_group order by header"
        )
        values_groups=[]

        on_groups_id=[]
        for g in list_groups:
            values_groups.append({'v':g['id'],'d':g['header']})
            if  manager.get('is_owner') and len(manager['CHILD_GROUPS']) and g['id'] in manager['CHILD_GROUPS_HASH']:
                on_groups_id.append(g['id'])

        values_managers=[]
        list_managers=await form.db.query(
            query="select id, name from manager order by name"
        )
        for g in list_managers:
            values_managers.append({'v':g['id'],'d':g['name']})



        form.fields.append(
            {
                'description':'Группа менеджеров',
                'name':'group_id',
                'type':'select',
                'values':values_groups,
                'value':on_groups_id
            }
        )

        form.fields.append(
            {
                'description':'Менеджер',
                'name':'manager_id',
                'type':'select',
                'values':values_managers,

            }
        )
    elif manager.get('is_owner') and len(manager['CHILD_GROUPS']):
        # руководитель, выводим доп. фильтры
        list_groups=await form.db.query(
            query="select id, header from manager_group where id in ("+join_ids(manager['CHILD_GROUPS'])+') order by header'
        )
        values_groups=[]

        on_groups_id=[]
        for g in list_groups:
            values_groups.append({'v':g['id'],'d':g['header']})
            on_groups_id.append(g['id'])
        values_managers=[]
        list_managers=await form.db.query(
            query="select id, name from manager where group_id in ("+join_ids(manager['CHILD_GROUPS'])+') order by name'
        )
        for g in list_managers:
            values_managers.append({'v':g['id'],'d':g['name']})

        form.fields.append(
            {
                'description':'Группа менеджеров',
                'name':'group_id',
                'type':'select',
                'values':values_groups,
                'value':on_groups_id
            }
        )

        form.fields.append(
            {
                'description':'Менеджер',
                'name':'manager_id_id',
                'type':'select',
                'values':values_managers,

            }
        )

    #form.pre(form.fields)




def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)

def period_before_code(form, field):
    #now = datetime.datetime.now()

    #year=now.year
    #mon=now.month

    #p2=''
    #if mon==12:
    #else:
    #    p2
    #print('mon:',mon)

    #field['value']=[now.strftime("%Y-%m-01")]
    #print('p1_value:',p1_value)

    start_day_of_month = date.today().replace(day=1)

    field['value']=[date.today().replace(day=1) , last_day_of_month(date.today())]
    #print("First day of prev month:", start_day_of_prev_month)
    #print("Last day of prev month:", last_day_of_prev_month)
form={
    'title':'Архив оплат',
    'work_table':'',
    'log':[],
    'fields':[
      {
        'description':'Начало периода',
        'type':'date',
        'name':'period',

        'range':True,
        'before_code': period_before_code,




      },
    ],

    'events':{
        'permissions':permissions,
        'search':search
    }

}


