from lib.CRM.form import Form
from .fields import fields
#from .events import events


class Config(Form):
    #events=events
    def __init__(self,arg):
        super().__init__(arg) 
#        self.work_table='manager_menu' 
        #self.events=events
        self.title='Руководство пользователя'
        self.sort=1
        self.tree_use=1
        self.header_field='header'
        self.default_find_filter='header'

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

        self.fields=fields

