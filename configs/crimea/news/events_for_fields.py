from lib.core import join_ids

def snt_id_before_code(form,field):
    if form.script=='edit_form' and form.action in ('edit','update'):
        field['read_only']=1

    if not(form.admin_all_snt):
        #print('snt_ids:',form.snt_ids)
        if len(form.snt_ids):
            field['where']=f"id in ({join_ids(form.snt_ids)})"

def set_filedir(form,field):

    #print('action:',form.action)
    snt_id=None
    if form.script in ('find_objects','admin_table') or form.action=='new':
        return
    R=form.R
    if form.action=='insert':
        if values:=R.get('values'):
            snt_id=values.get('snt_id')
        #print('new_values:',R)
    else:
        if form.ov:
            snt_id=form.ov.get('snt_id')


    if not(snt_id):
        form.errors.append('не удалось определить snt_id')

    if not(len(form.errors)) and snt_id:
        field['filedir']=f'./files/snt_{snt_id}/news'

def filter_code_photo2(form,field,row):
    name=row['wt__'+field['name']]
    snt_id=row['wt__snt_id']
    if snt_id and name:
        name_without_ext,ext = name.split('.')
        if name_without_ext and ext:
            src=f"/files/snt_{snt_id}/news/{name_without_ext}_mini1.{ext}"
            return f"<img src='{src}' width='150'>"

def body_before_code(form,field):
    if form.id and form.ov:
        if snt_id:=form.ov.get('snt_id'):
            return

    field['read_only']=True


events={
    'snt_id':{
        'before_code':snt_id_before_code
    },
    'photo':{
        'before_code':set_filedir,
    },
    'photo2':{
        #'permissions':set_filedir,
        'before_code':set_filedir,
        'filter_code':filter_code_photo2
    },
    'body':{
        'before_code':body_before_code
    }
}