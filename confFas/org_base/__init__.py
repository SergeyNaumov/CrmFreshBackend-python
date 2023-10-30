from lib.core import exists_arg
from lib.CRM.form import Form
from .fields import fields

from .ajax import ajax

form={
    'wide_form':True,
    'title':'Контакты из протоколов',
    'work_table':'org_base',
    'ajax':ajax,
    'is_admin':False,
    'QUERY_SEARCH_TABLES':[
        {'t':'org_base','a':'wt'},
        {'t':'region','a':'r','link':'wt.region_id=r.region_id','lj':1},
        #{'t':'protocols.reestr_nostroy','a':'rn',link=>q{rn.inn<>'' and rn.inn is not null and wt.inn=rn.inn},left_join=>1},
        #{'t':'protocols.mchs_gov_ru_reestr','a':'mchs',link=>q{mchs.inn<>'' and mchs.inn is not null and wt.inn=mchs.inn},left_join=>1},
        #{'t':'protocols.reestr_nopriz','a':'nopriz',link=>q{nopriz.inn<>'' and nopriz.inn is not null and wt.inn=nopriz.inn},left_join=>1},
        #{'t':'protocols_records.legal_entity_table','a':'let',link=>q{let.inn<>'' and let.inn is not null and wt.inn=let.inn},left_join=>1},
        #{'t':'protocols_records.fns_sample','a':'fns','l':'fns.eruz_id=let.reg_number',left_join=>1}
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
    'read_only':1,
    'GROUP_BY':'wt.id',
    'fields':fields
}

#form['fields']=get_fields()


