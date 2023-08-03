from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    events=events
    def __init__(form,arg):
        super().__init__(arg) 

        form.title='Новости'
        
        form.work_table='news' 
        form.QUERY_SEARCH_TABLES=[
            {'table':form.work_table,'alias':'wt'},

            # 
        ]
        form.headers=[
            {'h':'Название ', 'n':'header','sort':'header'},
            {'h':'Дата новости','n':'registered','sort':'reg'},
            {'h':'Краткое описание','n':'anons','sort':'anons'},
            #{'h':'Ссылка на конференци','n':'link'},
            #{'h':'Идентификатор конференции','n':'conf_id'},
            #{'h':'Код доступа','n':'access_code'},
            #{'h':'Комментарий','n':'comment'},

        ]
        form.data=[]
        form.sort='reg' # поле, по которому сортируем изначально
        form.sort_desc=True
        form.GROUP_BY='wt.id'
        form.read_only=1
        form.events=events
        form.not_create=1
        #form.explain=1

        form.filters_groups=[]
        form.on_filters=[

        ]
        form.search_on_load=1

        # обязательно через функцию, чтобы очищались
        form.fields=get_fields()

