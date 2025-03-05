from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    events=events
    def __init__(form,arg):
        super().__init__(arg) 
        
        form.title='Редактирование списка тестирования'
        form.explain=0
        form.read_only=1
        form.make_delete=0
        form.not_create=1
        form.make_edit=0
        form.QUERY_SEARCH_TABLES=[
            {'table':form.work_table,'alias':'wt'}
        ]
        form.headers=[
            {'h':'Наименование опроса', 'n':'header'},
            {'h':'Ссылка на тестирование','n':'link'},
            {'h':'Период','n':'period'},
            #{'h':'Ссылка на конференци','n':'link'},
            #{'h':'Идентификатор конференции','n':'conf_id'},
            #{'h':'Код доступа','n':'access_code'},
            #{'h':'Комментарий','n':'comment'},

        ]
        form.events=events
        form.filters_groups=[]
        form.data=[]
        form.sort='period' # поле, по которому сортируем изначально
        form.sort_desc=False

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