from .gpt_fields import add_gpt_fields
def permissions(form):
    db=form.db

    add_gpt_fields(form)

    form.filedir=f"./files/project_{form.s.project_id}"
    form.filedir_http=f"/files/project_{form.s.project_id}"
    
    form.foreign_key='project_id'
    form.foreign_key_value=form.s.project_id

    #print('CONST_LIST:', form.fields)
    
    
events={
    'permissions':permissions
}