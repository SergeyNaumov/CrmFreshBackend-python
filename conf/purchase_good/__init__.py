from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    events=events
    def __init__(self,arg):
        super().__init__(arg) 
        
        self.title='Отчёты онлайн'
        self.not_edit=1
        self.explain=1
        self.read_only=1
        self.make_delete=0
        self.QUERY_SEARCH_TABLES=[
            {'table':self.work_table,'alias':'wt'},
            {'table':'purchase','alias':'p','link':'p.id=wt.purchase_id','left_join':1},
            {'table':'action','alias':'act','link':'p.action_id=act.id','left_join':1},
            {'table':'action_plan','alias':'ap','link':'ap.action_id=act.id','left_join':1,'not_add_in_select_fields':1},
            {'table':'action_plan_supplier','alias':'aps','link':'aps.action_plan_id=ap.id','left_join':1,'not_add_in_select_fields':1},
            {'table':'supplier','alias':'s2','link':'s2.id=aps.supplier_id','left_join':1,'not_add_in_select_fields':1},
            {'table':'apteka','alias':'a','link':'wt.apteka_id = a.id','left_join':1},
            {'table':'supplier','alias':'s','link':'wt.supplier_id = s.id','left_join':1},
        ]
        self.GROUP_BY='wt.id'
        self.events=events
        self.filters_groups=[]
        # self.on_filters=[
        #     # {'name':'header'},
        #     # {'name':'code'},
        #     # {'name':'cnt'},
        #     # {'name':'summ'},
        #     # {'name':'apteka_id'},
        #     # {'name':'supplier_id'},

        # ]
        #self.search_on_load=1
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