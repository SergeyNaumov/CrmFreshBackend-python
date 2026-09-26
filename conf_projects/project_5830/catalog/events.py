from .ajax import ajax
from lib.CRM.plugins.InExtUrl import InExtUrl

async def permissions(form):

    project_id=form.request.state.project['project_id']
    #project_id=form.s.project_id
    await InExtUrl(form,
     {
        'foreign_key':'project_id',
        'foreign_key_value':project_id,
        'dependence_field':'header',
        'in_url':'/catalog/<%id%>',
        'after_field':'header',
        'url_prefix':'/catalog/',
        'ajax':'in_ext_url',
        'tab':'promo',
     }
    )
    #form.pre(form.fields)
    form.work_table=f'struct_{project_id}_catalog'
    #form.pre(project_id)
    form.ov=None
    if form.id:
        form.ov = await form.db.query(
            query=f"select * from {form.work_table} where id={form.id}",
            onerow=1
        )

    form.ajax=ajax


    if form.script=='edit_form' and form.id:
        form.ov=await form.db.query(
            query=f"select * from {form.work_table} where {form.work_table_id}={form.id}",
            onerow=1
        )
        #form.pre(ov)

    #header_field=form.get_field('header')
    #header_field['frontend']={'ajax':{'name':'gen_url','timeout':100}}

    #url_field=form.get_field('url')
    #url_field['frontend']={'ajax':{'name':'url','timeout':100}}
    #form.pre(url_field)

# def after_insert(form):

#     form.db.query(
#         query=f"UPDATE {form.work_table} SET url='/catalog/{form.id}' where id={form.id}"
#     )

events={
    'permissions':permissions,
    #'after_insert':after_insert
}