from .gpt_fields import add_gpt_fields
async def permissions(form):
    db=form.db

    #add_gpt_fields(form)

    form.filedir=f"./files/project_{form.request.state.project['project_id']}"
    form.filedir_http=f"/files/project_{form.request.state.project['project_id']}"
    
    form.foreign_key='project_id'
    form.foreign_key_value=form.request.state.project['project_id']

    #print('CONST_LIST:', form.fields)
    
    
async def after_insert(form):

    await form.db.query(
        query=f"UPDATE {form.work_table} SET url='/catalog/{form.id}' where id={form.id}"
    )

events={
    'permissions':permissions,
    'after_insert':after_insert
}