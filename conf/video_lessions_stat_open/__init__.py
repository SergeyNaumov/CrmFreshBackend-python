from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    events=events
    def __init__(self,arg):
        super().__init__(arg) 
        
        self.title='Статистика просмотра видеоматериалов'
        self.explain=0
        self.read_only=1
        self.make_delete=0
        self.not_create=1
        self.not_edit=1
        self.QUERY_SEARCH_TABLES=[
            {'t':self.work_table,'a':'wt'},
            {'t':'video_lessions','a':'v','l':'v.id=wt.video_id'},
            {'t':'manager','a':'m','l':'wt.manager_id=m.id'},
            
            # Аптека
            {'t':'apteka','a':'apt','l':'apt.manager_id=wt.manager_id','lj':1},
            {'t':'ur_lico','a':'ul_apt','l':'ul_apt.id=apt.ur_lico_id','lj':1},
            
            # Юрлицо
            {'t':'ur_lico_manager','a':'ulm','l':'ulm.manager_id=wt.manager_id','lj':1},
            {'t':'ur_lico','a':'ul','l':'ul.id=ulm.ur_lico_id','lj':1},

            # Фармацевт
            {'t':'manager_pharmacist','a':'mph','l':'mph.id=wt.manager_id','lj':1},
            {'t':'apteka','a':'pharm_apt','l':'pharm_apt.id=mph.apteka_id','lj':1},
            {'t':'ur_lico','a':'pharm_ul','l':'pharm_ul.id=pharm_apt.ur_lico_id','lj':1},

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
        self.GROUP_BY='wt.id'
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