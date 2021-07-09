from lib.CRM.form import Form
from .fields import get_fields
from .filters import get_filters
from .events import events


class Config(Form):
    events=events
    def __init__(form,arg):
        super().__init__(arg) 
        
        form.title='Прогнозный бонус для юридических лиц'
        form.explain=0
        form.read_only=1
        form.make_delete=0
        form.not_edit=1
        
        form.QUERY_SEARCH_TABLES=[
            {'t':form.work_table,'a':'wt'},
            {'t':'prognoz_bonus_period','a':'pbp','l':'pbp.id=wt.period_id'},
            {'t':'action','a':'a','l':'wt.action_id=a.id'},
            {'t':'action_plan','a':'ap','l':'ap.id=wt.action_plan_id'},
            {'t':'ur_lico','a':'u','l':'u.id=wt.ur_lico_id'},
            
        ]
        form.events=events
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
        
        if arg['script'] in ('admin_table','find_objects','autocomplete'):
            form.fields=get_filters()
        else:
            form.fields=get_fields()
        


