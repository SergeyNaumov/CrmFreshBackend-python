from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    #events=events
    def __init__(form,arg):
        super().__init__(arg) 
#        self.work_table='manager_menu' 
        form.events=events
        form.title='Конференции'
        form.sort=0
        form.tree_use=0
        form.header_field='header'
        form.default_find_filter='header'
        form.not_create=1
        form.read_only=1
        form.make_delete=False
        form.javascript={
            'page':form.template(
                './conf/conference/page.js'
            )
        }
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
        form.filters_groups=[]

        form.fields=get_fields()

