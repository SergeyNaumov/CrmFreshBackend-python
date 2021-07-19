from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    events=events
    def __init__(self,arg):
        super().__init__(arg) 
        
        self.title='Аптеки'
        #self.explain=0
        self.read_only=1
        self.not_create=1
        self.make_delete=False
        self.QUERY_SEARCH_TABLES=[
            {'t':self.work_table,'a':'wt'},
            {'t':'manager','a':'m','l':'wt.manager_id=m.id','lj':1}
        ]
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