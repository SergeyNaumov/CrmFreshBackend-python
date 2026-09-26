from .ajax import ajax
from lib.CRM.plugins.InExtUrl import InExtUrl

async def permissions(form):
    project_id=form.request.state.project['project_id']
    # InExtUrl(form,
    #  {
    #     'foreign_key':'project_id',
    #     'foreign_key_value':project_id,
    #     'dependence_field':'header',
    #     'in_url':'/vendor/<%id%>',
    #     'after_field':'header',
    #     'url_prefix':'/vendor/',
    #     'ajax':'in_ext_url',
    #     'tab':'promo',
    #  }
    # )
    
    
    
    form.ov=None
    if form.id:
        form.ov=await form.db.query(
            query=f"select * from {form.work_table} where id={form.id}",
            onerow=1
        )

    form.ajax=ajax

events={
    'permissions':permissions,
    #'after_insert':after_insert
}