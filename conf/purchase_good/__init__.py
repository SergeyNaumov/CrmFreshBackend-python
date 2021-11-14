from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    events=events
    def __init__(form,arg):
        super().__init__(arg) 
        
        form.title='Отчёты онлайн'
        form.not_edit=1
        form.explain=0
        form.read_only=1
        form.make_delete=0
        form.not_create=1
        form.QUERY_SEARCH_TABLES=[
            {'t':form.work_table,'a':'wt'},
            {'t':'purchase','a':'p','link':'p.id=wt.purchase_id ','left_join':1},
            {'t':'action','a':'act','link':'p.action_id=act.id','left_join':1},
            {'t':'action_plan','a':'ap','link':'ap.action_id=act.id and wt.action_plan_id=ap.id','left_join':1,'not_add_in_select_fields':1},
            #{'t':'action_plan_supplier','a':'aps','link':'aps.action_plan_id=ap.id','left_join':1,'not_add_in_select_fields':1},
            #{'t':'supplier','a':'s2','l':'s2.id=aps.supplier_id','lj':1,'not_add_in_select_fields':1},
            {'t':'apteka','a':'a','l':'wt.apteka_id = a.id','lj':1},
            {'t':'ur_lico','a':'ul','l':'a.ur_lico_id=ul.id','lj':1}
            #{'table':'supplier','alias':'s','link':'wt.supplier_id = s.id','left_join':1},
        ]
        form.GROUP_BY='wt.id'
        form.events=events
        form.filters_groups=[]
        # form.on_filters=[
        #     # {'name':'header'},
        #     # {'name':'code'},
        #     # {'name':'cnt'},
        #     # {'name':'summ'},
        #     # {'name':'apteka_id'},
        #     # {'name':'supplier_id'},

        # ]
        #form.search_on_load=1

        form.fields=get_fields()

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