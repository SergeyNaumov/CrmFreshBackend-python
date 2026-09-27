from .gpt_fields import add_gpt_fields
async def permissions(form):
    db=form.db

    await add_gpt_fields(form)

    form.filedir=f"./files/project_{form.request.state.project['project_id']}"
    form.filedir_http=f"/files/project_{form.request.state.project['project_id']}"
    
    form.foreign_key='project_id'
    form.foreign_key_value=form.request.state.project['project_id']

    #print('CONST_LIST:', form.fields)
    
    
events={
    'permissions':permissions
}