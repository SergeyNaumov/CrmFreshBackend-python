from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    events=events
    def __init__(self,arg):
        super().__init__(arg) 
        
        self.title='Юридические лица'
        self.explain=0
        self.read_only=1
        self.make_delete=0
        self.QUERY_SEARCH_TABLES=[
            {'table':self.work_table,'alias':'wt'},
            {'table':'manager','alias':'m1','link':'wt.manager_id=m1.id','left_join':1},
            {'table':'manager','alias':'m2','link':'wt.anna_manager_id=m2.id','left_join':1},
        ]
        self.events=events
        self.filters_groups=[]
        #self.explain=1
        self.on_filters=[
            # {
            #     'name':'address'
            # },
            # {
            #     'name':'f_date',
            #     #'value':["2020-01-01","2020-01-02"]
            # },
        ]
        self.search_on_load=1
        self.fields=get_fields()

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