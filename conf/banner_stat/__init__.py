from lib.CRM.form import Form
from .fields import get_fields
from .events import events


class Config(Form):
    
    def __init__(form,arg):
        super().__init__(arg) 
        form.events=events
        form.title='Статистика просмотра баннеров'
        form.not_create=1
        form.make_delete=0
        form.read_only=1        
        form.work_table='banner_stat' 
        form.QUERY_SEARCH_TABLES=[
            {'t':form.work_table,'a':'wt'},
            {'t':'banner','a':'b','l':'wt.banner_id=b.id'},
            {'t':'manager','a':'m','l':'m.id=wt.manager_id'},
            {'table':'ur_lico_manager','a':'ulm','l':'ulm.manager_id=m.id','lj':1},
            {'table':'ur_lico','a':'ul','l':'ul.id=ulm.ur_lico_id','lj':1},
            {'table':'apteka','a':'apt','l':'apt.manager_id=m.id','lj':1},
            {'table':'ur_lico','a':'ul2','l':'ul2.id=apt.ur_lico_id','lj':1} # юрлицо аптеки
            # 
        ]
        #form.explain=1
        form.GROUP_BY='wt.id'

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

