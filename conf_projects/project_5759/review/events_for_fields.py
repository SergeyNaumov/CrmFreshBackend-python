from lib.core import cur_date

def enabled_before_code (form,field):
    if form.action=='new':
        field['value']=1

def dat_before_code(form,field):
    if form.action=='new':
        field['value']=cur_date()
        
        #print(dt)
events={
    'enabled':{
        'before_code':enabled_before_code
    },
    'dat':{
        'before_code':dat_before_code
    }
}
