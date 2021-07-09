from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    events=events
    def __init__(form,arg):
        
        super().__init__(arg) 
        
        form.title='Планы акций'
        form.explain=0
        form.read_only=1
        form.make_delete=0
        form.not_edit=1
        form.QUERY_SEARCH_TABLES=[
            {'table':form.work_table,'alias':'wt'},

        ]
        form.events=events
        form.filters_groups=[]
        form.GROUP_BY='wt.id'
        #form.on_filters=[
            # {
            #     'name':'address'
            # },
            # {
            #     'name':'f_date',
            #     #'value':["2020-01-01","2020-01-02"]
            # },
        #]
        #form.javascript['edit_form']=form.template('./js/Chart.bundle.min.js')
        #form.javascript['edit_form']+=form.template('./conf/action_plan/templates/edit_form.js')
        

        # form.tabs=[
        #     {'description':'Группы товаров','name':'goods'},
        #     {'description':'<span style="color: red;">Прогнозный бонус</span>','name':'pr_bonus','tab_style':'color: red;'},
        #     {'description':'Разрешённые дистрибьюторы','name':'distrib'},
        # ]
        form.search_on_load=0
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