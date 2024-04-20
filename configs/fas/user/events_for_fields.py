from lib.core import exists_arg, join_ids
def contact_date_before_code(form,field):
    if form.script=='admin_table':
        field['type']='date'


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

def archive_before_code(form,field):
    # Доступ к галке "в архиве" у руководителя, либо у того, у кого есть соответствующая галка
    if (form.id and form.is_owner_group) or form.manager['permissions'].get('archive_in_card_op'):
        field['read_only']=0

def brand_id_before_code(form,field):

    if form.manager['permissions']['user_change_brand']:
        # может менять бренд в картах ОП
        field['read_only']=0

    if form.action=='new' and form.script=='edit_form' and len(form.manager_brand)>1:
        field['value']=form.manager_brand[1]

def manager_id_before_code(form,field):
    perm=form.manager['permissions']
    #field['read_only']=True
    if perm['card_op_make_change_manager']:
        field['read_only']=0

    # Если это руководитель:
    if form.ov:
        if form.manager['CHILD_GROUPS_HASH'].get(form.ov['group_id']):
            field['read_only']=0
            # даём возможность выбрать менеджера только из своей группы
            if len(form.manager['CHILD_GROUPS']):
                field['where']=f"group_id in ({join_ids(form.manager['CHILD_GROUPS'])})"

    #form.pre(form.ov)
    #form.pre(form.manager)
    if form.action=='new':
        field['value']=form.manager['id']
    
    # if form.script in ('find_result', 'admin_table'):
    #     field['make_change_in_search']=1
    #     field['read_only']=0

def region_id_filter_code(form, field, row):
    if row['r__header']:
        ts=row['r__timeshift']
        if ts>=0:
            ts=f"+{ts}"
        return f"{row['r__header']} ({ts})"
    return '-'

events={

  'brand_id':{
    'before_code':brand_id_before_code
  },
  'archive':{
    'before_code':archive_before_code
  },
  'manager_id':{
    'before_code':manager_id_before_code
  },
  'contact_date': {
    'before_code':contact_date_before_code
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
  'region_id':{
    'filter_code':region_id_filter_code
  },

  #'inn':{
    #'before_code': inn_before_code
  #}


}