from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    events=events
    def __init__(form,arg):
        super().__init__(arg) 
        
        form.title='Запросы на подписку от аптек'
        #form.explain=1
        form.read_only=1
        form.not_edit=1
        form.not_create=1
        form.make_delete=False
        #form.work_table_id='action_id,apteka_id'
        form.work_table_id='id'
        form.QUERY_SEARCH_TABLES=[
            {'t':form.work_table,'a':'wt'},
            {'t':'action','a':'a','l':'a.id=wt.action_id'},
            {'t':'apteka','a':'apt','l':'apt.id=wt.apteka_id'},
            {'t':'ur_lico','a':'ul','l':'apt.ur_lico_id=ul.id'}
        ]

        form.events=events
        form.filters_groups=[]
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