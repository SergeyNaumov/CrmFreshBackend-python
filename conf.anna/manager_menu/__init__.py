from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    #events=events
    def __init__(self,arg):
        super().__init__(arg) 
        self.work_table='manager_menu' 
        self.events=events
        self.title='Пункты меню'
        self.sort=1
        self.tree_use=1
        self.header_field='header'
        self.default_find_filter='header'
        self.cols=[
          [{'name':'main','description':'Основные Параметры'}],
          [{'name':'advanced','description':'Дополнительные Параметры'}]
        ]
        # self.cols=[
        #     [
        #         {'description':'wysiwyg','name':'wysiwyg','hide':1},
        #         {'description':'Простые типы данных','name':'plain'},
        #         {'description':'Тэги','name':'tags','hide':1},
        #         {'description':'Комментарии','name':'memo','hide':1},
        #     ],
        #     [
        #         {'description':'Файлы','name':'files','hide':1},
        #         {'description':'Один ко многим','name':'one_to_m','hide':0},
        #         {'description':'Дата, время и т.д.','name':'timing','hide':1},
        #     ]
        # ]
        self.filters_groups=[]

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