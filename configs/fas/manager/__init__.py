from lib.CRM.form import Form
from .fields import get_fields

from .ajax import ajax
form={
    'title':'Учётные записи системы',
    'work_table':'manager',
    'ajax':ajax,
    'is_admin':False,
    #'explain':1,
    'QUERY_SEARCH_TABLES':[
            {'table':'manager','alias':'wt'},
            {'t':'manager_email','a':'me','l':'me.manager_id=wt.id','lj':1},
            {'t':'manager_group','a':'mg','l':'wt.group_id=mg.id','lj':1, 'for_fields':['group_id']},
            {'t':'manager_permissions','a':'mp','l':'mp.manager_id=wt.id','lj':1},
            {'t':'permissions','a':'p','l':'p.id=mp.permissions_id','lj':1},

            # 
    ],
    'cols':[
            [ # Колонка1
              {'description':'Общая информация','name':'main','hide':0},
              {'description':'HR','name':'hr','hide':0},
            ],
            [
              #{'description':'Юридические лица','name':'comp','hide':1},
              #{'description':'Аптеки','name':'apteka','hide':1},
              {'description':'Права','name':'permissions','hide':0},
              
            ]
    ],
    'filters_groups':[],
    # 'on_filters':[
    #     {
    #      'name':'address'
    #     },
    #     {
    #      'name':'f_date',
    #      #'value':["2020-01-01","2020-01-02"]
    #     },
    # ],
    'search_on_load':1,

    'not_create':1,
    'read_only':1,
    'GROUP_BY':'wt.id',
}

form['fields']=get_fields()


