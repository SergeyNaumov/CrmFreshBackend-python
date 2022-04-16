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
            {'h':'Название ', 'n':'header'},
            {'h':'Дата новости','n':'registered'},
            {'h':'Краткое описание','n':'anons'},
            #{'h':'Ссылка на конференци','n':'link'},
            #{'h':'Идентификатор конференции','n':'conf_id'},
            #{'h':'Код доступа','n':'access_code'},
            #{'h':'Комментарий','n':'comment'},

        ]
        form.data=[]
        form.sort='registered' # поле, по которому сортируем изначально
        form.sort_desc=True
        form.GROUP_BY='wt.id'
        form.read_only=1
        form.events=events
        form.not_create=1
        #form.explain=1

        form.filters_groups=[]
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

        # обязательно через функцию, чтобы очищались
        form.fields=get_fields()

