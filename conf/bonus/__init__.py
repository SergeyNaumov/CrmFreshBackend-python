from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    events=events
    def __init__(self,arg):
        super().__init__(arg) 
        
        self.title='Бонусы'
        self.explain=0
        self.read_only=1
        self.make_delete=0
        self.not_create=1
        self.not_edit=1
        self.GROUP_BY='wt.id'
        self.QUERY_SEARCH_TABLES=[
            {'t':self.work_table,'a':'wt'},
            {'t':'bonus_order','a':'bo','l':'wt.id=bo.bonus_id'}
        ]
        self.events=events
        self.not_order=0
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