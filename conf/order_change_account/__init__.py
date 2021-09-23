from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    events=events
    def __init__(self,arg):
        super().__init__(arg) 
        
        self.title='Заявки на изменение рег. данных аккаунта'
        self.explain=0
        self.make_delete=0
        self.not_create=1
        self.read_only=0

        self.QUERY_SEARCH_TABLES=[
            {'table':self.work_table,'alias':'wt'},
            {'t':'manager','a':'m','l':'wt.manager_id=m.id','lj':1},
            {'t':'apteka','a':'apt','l':'wt.manager_id=apt.manager_id','lj':1},
            {'t':'ur_lico_manager','a':'ulm','l':'ulm.manager_id=m.id','lj':1},
            {'t':'ur_lico','a':'ul','l':'ulm.ur_lico_id=ul.id','lj':1},
            {'t':'ur_lico','a':'ul2','l':'apt.ur_lico_id=ul2.id','lj':1},
        ]
        self.GROUP='wt.id'
        self.events=events
        self.filters_groups=[]
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