from lib.core import cur_date

def enabled_before_code (form,field):
    if form.action=='new':
        field['value']=1

def dat_before_code(form,field):
    if form.action=='new':
        field['value']=cur_date()
        
def logo_filter_code(form,field,row):
    #form.pre(field)
    #form.pre(row)
    if row['wt__'+field['name']]:
        field['type']='html'
        return f"""<img src="{field['filedir'].replace('./','/')}/{row['wt__'+field['name']]}">"""
    
    return ''
        #print(dt)
events={
    'enabled':{
        'before_code':enabled_before_code
    },
    'dat':{
        'before_code':dat_before_code
    },
    'logo':{
       # 'filter_code':logo_filter_code
    }
}
