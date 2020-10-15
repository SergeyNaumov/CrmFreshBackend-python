from lib.CRM.classes.form import Form
from .fields import fields
from .events import events


class Config(Form):
    events=events
    def __init__(self,arg):
        super().__init__(arg)

        self.work_table='test'
        self.title='тестовый конфиг'
        self.cols=[
            [
                {'description':'wysiwyg','name':'wysiwyg','hide':1},
                {'description':'Простые типы данных','name':'plain'},
                {'description':'Тэги','name':'tags','hide':1},
                {'description':'Комментарии','name':'memo','hide':1},
            ],
            [
                {'description':'Файлы','name':'files','hide':1},
                {'description':'Один ко многим','name':'one_to_m','hide':0},
                {'description':'Дата, время и т.д.','name':'timing','hide':1},
            ]
        ]
        self.on_filters=[
            {
                'name':'f_date',
                'value':["2020-01-01","2020-01-02"]
            },
            {
                'name':'header'
            },
        ]
        self.fields=fields
