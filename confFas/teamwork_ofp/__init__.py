from lib.core import exists_arg
from lib.CRM.form import Form
#from .fields import get_fields
from .ajax import ajax
from .fields import fields


form={
    'wide_form':True,
    'title':'Совместная работа Юр. услуг',
    'work_table':'teamwork_ofp',
    'work_table_id':'teamwork_ofp_id',
    'make_delete':0,
    'read_only':1,
    #'not_create':1,
    'explain':0,
    'ajax':ajax,
    'is_admin':False,
    'cols':[
            [ # Колонка1
              
              {'description':'Общая информация','name':'main','hide':0},
              
            ],
            [
              {'description':'Работа с картой','name':'work','hide':0},
              {'description':'Контакты','name':'contacts','hide':0},
            ]
    ],
    'QUERY_SEARCH_TABLES':[
      {'t':'teamwork_ofp','a':'wt'},
      {'t':'user','a':'u','l':'u.id=wt.user_id','lj':1, 'for_fields':['firm', 'inn', 'f_city','manager_id']},
      {'t':'manager','a':'m','l':'m.id=u.manager_id','lj':1, 'for_fields':['manager_id']},

      {'t':'manager','a':'mf','l':'wt.manager_from=mf.id','lj':1, 'for_fields':['manager_from','managers_groups_name']},
      {'t':'manager','a':'mt','l':'wt.manager_to=mt.id','lj':1},
      {'t':'manager','a':'mt2','l':'wt.manager_to2=mt2.id','lj':1,'for_fields':['manager_to2']},
      {'t':'manager','a':'me','l':'wt.exhibitor_id=me.id','lj':1,'for_fields':['exhibitor_id']},
      {'t':'manager','a':'m_oso','l':'wt.manager_oso=m_oso.id','lj':1,'for_fields':['manager_oso']},
      {'t':'manager_group','a':'mfg','l':'mf.group_id=mfg.id','lj':1,'for_fields':['manager_from','managers_groups_name']},
      {'t':'city','a':'city','l':'city.city_id=wt.city_id','lj':1,'for_fields':['city_id']},
      {'t':'teamwork_ofp_memo','a':'memo','l':'memo.teamwork_ofp_id=wt.teamwork_ofp_id','for_fields':['comment1']},
      {'t':'manager','a':'m_memo','l':'m_memo.id=memo.manager_id','for_fields':['comment1']},
      #{'t':'users_fs_memo_fp','a':'memo4','l':'memo4.users_fs_id=wt.user_id','for_fields':['comment4']},
      #{'t':'manager','a':'m_memo4','l':'m_memo4.id=memo4.manager_id','for_fields':['comment4']},
    ],
    #'explain':1,
    'filters_groups':[],

    'GROUP_BY':'wt.teamwork_ofp_id',
    'fields':fields

}

#form['fields']=get_fields()


