from lib.CRM.form import Form
from .fields import fields
from .events import events


class Config(Form):
    #events=events
    def __init__(form,arg):
        super().__init__(arg) 
        form.work_table='video_lessions' 
        form.table_stat_open='video_lessions_stat_open' # Статистика просмотров видео
        form.events=events
        form.title='Видео лекции'
        form.sort=1
        form.tree_use=1
        form.max_level=2
        form.header_field='header'
        form.default_find_filter='header'
        form.filters_groups=[]
        form.fields=fields
        form.links=[]
