from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    events=events
    def __init__(form,arg):
        super().__init__(arg) 
        
        form.title='Юридические лица'
        form.explain=0
        form.read_only=1
        form.make_delete=0
        form.QUERY_SEARCH_TABLES=[
            {'table':form.work_table,'alias':'wt'},
            #{'table':'manager','alias':'m1','link':'wt.manager_id=m1.id','left_join':1},
            {'table':'manager','alias':'m2','link':'wt.anna_manager_id=m2.id','left_join':1},
            {'table':'apteka','alias':'a','link':'a.ur_lico_id=wt.id'},
            {'t':'ur_lico_manager','a':'ulm','l':'ulm.ur_lico_id=wt.id','lj':1},
            {'t':'manager','a':'m1','l':'ulm.manager_id=m1.id','lj':1},
        ]
        form.events=events
        form.filters_groups=[]
        #form.explain=1
        form.on_filters=[
            # {
            #     'name':'address'
            # },
            # {
            #     'name':'f_date',
            #     #'value':["2020-01-01","2020-01-02"]
            # },
        ]
        form.search_on_load=1
        form.fields=get_fields()
        form.GROUP_BY='wt.id'

"""
create table test(
    id int primary key auto_increment,
    address varchar(255) not null default '',
    textarea text,
    wysiwyg text,
    checkbox tinyint unsigned not null default '0',
    switch  tinyint unsigned not null default '0',
    f_datetime datetime,
    status  tinyint unsigned not null default '0'
) engine=innodb default charset=utf8;
"""