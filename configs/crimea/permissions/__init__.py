from lib.CRM.form import Form
from .fields import get_fields
from .events import events

form={
    'work_table':'permissions',
    'title':'Права менеджеров',
    'sort':1,
    'tree_use':1,
    'max_level':2,
    'header_field':'header',
    'default_find_filter':'header',
    'explain':0,
    'filters_groups':[],
    'changed_in_tree':True,
    'fields':get_fields()
}

# class Config(Form):
#     #events=events
#     def __init__(self,arg):
#         super().__init__(arg) 
#         self.work_table='permissions' 
#         self.events=events
#         self.title='Права менеджеров'
#         self.sort=1
#         self.tree_use=1
#         self.max_level=1
#         self.header_field='header'
#         self.default_find_filter='header'
#         self.explain=1

#         # self.cols=[
#         #     [
#         #         {'description':'wysiwyg','name':'wysiwyg','hide':1},
#         #         {'description':'Простые типы данных','name':'plain'},
#         #         {'description':'Тэги','name':'tags','hide':1},
#         #         {'description':'Комментарии','name':'memo','hide':1},
#         #     ],
#         #     [
#         #         {'description':'Файлы','name':'files','hide':1},
#         #         {'description':'Один ко многим','name':'one_to_m','hide':0},
#         #         {'description':'Дата, время и т.д.','name':'timing','hide':1},
#         #     ]
#         # ]
#         self.filters_groups=[]

#         self.fields=get_fields()

