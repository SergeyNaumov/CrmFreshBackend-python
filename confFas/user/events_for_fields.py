from lib.core import exists_arg

def links_before_code(form,field):
    
    if not(form.action == 'edit' and form.id):
        return

    field['after_html']=f'<div><a href="/edit_form/user/{form.id}?action=create_ofp_card" target="_blank">Создать карту ОФП</a></div>'

    # вывод карт ОФП в блоке ссылок
    ofp=form.db.query(
        query=f"select teamwork_ofp_id id,count(*) cnt from teamwork_ofp where user_id={form.id} limit 1",
        debug=1,
        onerow=1
    )
    #form.pre({'ofp':ofp})
    if ofp and ofp['cnt']:
        if ofp['cnt']>1:
            field['after_html']+=f'<div><a href="/admin_table/teamwork_ofp?user_id={form.id}" target="_blank">Показать все карты ({ofp["cnt"]})</a></div>'
        else:
            field['after_html']+=f'<div><a href="/edit_form/teamwork_ofp/{ofp["id"]}" target="_blank">Перейти в карту ОФП</a></div>'
        
            

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

    if form.manager['permissions']['user_change_brand']:
        # может менять бренд в картах ОП
        field['read_only']=0

    if form.action in ('new'):
        field['value']=form.manager_brand

def manager_id_before_code(form,field):
    if form.manager['permissions']['card_op_make_change_manager']:
        field['read_only']=0

    # Если это руководитель:
    if form.manager['CHILD_GROUPS_HASH'].get(form.ov['group_id']):
        field['read_only']=0
        
    #form.pre(form.ov)
    #form.pre(form.manager)
    if form.action in ('new'):
        field['value']=form.manager['id']
    
        

events={

  'brand_id':{
    'before_code':brand_id_before_code
  },
  'manager_id':{
    'before_code':manager_id_before_code
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