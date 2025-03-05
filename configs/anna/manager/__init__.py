from lib.CRM.form import Form
from .fields import get_fields
from .events import events
from .ajax import ajax

class Config(Form):
    events=events
    def __init__(form,arg):
        super().__init__(arg) 

        form.title='Учётные записи системы'
        
        form.work_table='manager' 
        form.QUERY_SEARCH_TABLES=[
            {'table':form.work_table,'alias':'wt'},
            {'t':'manager','a':'ma','l':'wt.anna_manager_id=ma.id','lj':1},
            # Фармацевт (связь с юрлицом)
            {'t':'manager_pharmacist','a':'pharm','l':'pharm.id=wt.id','lj':1},
            {'t':'apteka','a':'af','l':'af.id=pharm.apteka_id','lj':1},
            {'t':'ur_lico','a':'uf','l':'uf.id=af.ur_lico_id','lj':1},

            {'t':'ur_lico_manager','a':'ulm','l':'ulm.manager_id=wt.id','lj':1},
            {'t':'ur_lico','a':'u','l':'u.id=ulm.ur_lico_id','lj':1},
            
            
            {'t':'manager_permissions','a':'mp','l':'mp.manager_id=wt.id','lj':1},
            {'t':'permissions','a':'p','l':'p.id=mp.permissions_id','lj':1}
            # 
        ]
        form.GROUP_BY='wt.id'
        form.read_only=1
        form.events=events
        form.not_create=1
        #form.explain=1
        form.cols=[
            [ # Колонка1
              {'description':'Общая информация','name':'main','hide':0},
            ],
            [
              #{'description':'Юридические лица','name':'comp','hide':1},
              #{'description':'Аптеки','name':'apteka','hide':1},
              {'description':'Права','name':'permissions','hide':0},
              
            ]
        ]
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
        form.ajax=ajax

        # обязательно через функцию, чтобы очищались
        form.fields=get_fields()

