from lib.core import exists_arg

def links_before_code(form,field):
    
    #field['before_html']='before_html'
    field['after_html']=f'<a href="/edit_form/user/{form.id}?action=create_ofp_card" target="_blank">Создать карту ОФП</a>'
    #field['after_html']='after_html'

def firm_filter_code(form,field,row):
    return f"<a href='/edit_form/user/{row['wt__id']}' target='_blank'>{row['wt__firm']}</a>"

def kladr_after_search(data):
    i=0
    list=[]
    if not data:
        return list
    
    for d in data:
        res=[]
        for d2 in d['parents']:

            if d2['name']=='Москва' and d2['contentType']!='city':
                continue
            res.append,f'{d2["typeShort"]} {d2["name"]}'


        res.append(f'{d["typeShort"]} {d["name"]}')
        h=', '.join(res)
        list.append({'header':h})
    return list

def dt2_before_code(form,field):
    if exists_arg('admin_dt2', form.manager['permissions']):
        field['read_only']=False

def otk_before_code(form,field):
    if exists_arg('admin_otk', form.manager['permissions']):
        field['read_only']=False

def brand_id_before_code(form,field):
    if form.manager['login'] in ('akulov','sed','pzm'):
        field['read_only']=0



events={
  'links':{
    'before_code':links_before_code
  },
  'brand_id':{
    'before_code':brand_id_before_code
  },
  'firm':{
    'filter_code':firm_filter_code
  },
  'otk':{
    'before_code':otk_before_code
  },
  'dt2':{
    'before_code':dt2_before_code
  },


}