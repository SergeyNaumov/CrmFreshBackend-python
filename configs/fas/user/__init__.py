from lib.core import exists_arg
from lib.CRM.form import Form
from .fields import fields

from .ajax import ajax

form={
    'wide_form':True,
    'title':'Карты ОП',
    'work_table':'user',
    'ajax':ajax,
    'is_admin':False,
    #'explain':1,
    'is_owner':False, # Владелец карты
    'is_owner_group':False, # Руководитель группы
    'QUERY_SEARCH_TABLES':[
            {'table':'user','alias':'wt'},
            {'t':'manager','a':'m','l':'m.id=wt.manager_id','lj':1,'for_fields':['manager_id','f_manager_group']},
            {'t':'manager_group', 'a':'mg', 'l':'m.group_id','for_fields':['f_manager_group']},
            {'t':'user_contact','a':'uc','l':'uc.user_id=wt.id','lj':1, 'for_fields':['f_fio','f_email','f_phone']},
            {'t':'brand','a':'b','l':'wt.brand_id=b.id','lj':1,'for_fields':['brand_id']},
            # регион
            {'t':'region','a':'r','l':'wt.region_id=r.region_id','lj':1,'for_fields':['region_id']},
            # город
            {'t':'city','a':'c','l':'wt.city_id=c.city_id','lj':1,'for_fields':['city_id']},
            # memo
            {'t':'user_memo','a':'memo','l':'wt.id=memo.user_id','lj':1,'for_fields':['memo']},
            {'t':'manager','a':'memo_m','l':'memo.manager_id=memo_m.id','lj':1,'for_fields':['memo']},

    ],
    'cols':[
            [ # Колонка1
              {
                'description':'Ссылки','name':'links','hide':0, 'not_save_button':1,
                #'on_show':'console.log("this is show")'
              },
              {'description':'Общая информация','name':'main','hide':0},
            ],
            [
              {'description':'Продажи','name':'sale','hide':0},
              {'description':'Платежи','name':'paids','hide':0, 'not_save_button':1},
              {'description':'Документы','name':'docpack','hide':0},
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
    #'search_on_load':1,

    #'not_create':1,
    'make_delete':0,
    'read_only':1,
    'GROUP_BY':'wt.id',
    'fields':fields
}

#form['fields']=get_fields()


