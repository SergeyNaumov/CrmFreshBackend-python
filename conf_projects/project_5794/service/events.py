from .ajax import ajax
def permissions(form):
    project_id=form.s.project_id
    #form.pre(project_id)
    form.work_table=f'struct_{project_id}_service'
    if form.id:
        form.ov=form.db.query(
            query=f"select * from {form.work_table} where id={form.id}",
            onerow=1
        )
    form.ajax=ajax
    for name in ('photo','photo_menu','photo_sidebar','photo_dark', 'photo_menu'):
        #print('name:',name)
        photo_field=form.get_field(name)
        photo_field['filedir']=photo_field['filedir'].replace('[project_id]',str(project_id))

    if form.script=='edit_form' and form.id:
        form.ov=form.db.query(
            query=f"select * from {form.work_table} where {form.work_table_id}={form.id}",
            onerow=1
        )
        #form.pre(ov)
    header_field=form.get_field('header')
    header_field['frontend']={'ajax':{'name':'gen_url','timeout':100}}

    url_field=form.get_field('url')
    url_field['frontend']={'ajax':{'name':'url','timeout':100}}

            
def after_insert(form):

    form.db.query(
        query=f"UPDATE {form.work_table} SET url='/service/{form.id}' where id={form.id}"
    )

events={
    'permissions':permissions,
    'after_insert':after_insert
}