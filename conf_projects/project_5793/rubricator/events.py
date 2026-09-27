async def permissions(form):
    project_id=form.request.state.project['project_id']
    #form.pre(project_id)
    form.work_table=f'struct_{project_id}_rubricator'
    photo_field=form.get_field('photo')
    photo_field['filedir']=f'./files/project_{project_id}/rubricator'
    if form.script=='edit_form' and form.id:
        form.ov=await form.db.query(
            query=f"select * from {form.work_table} where {form.work_table_id}={form.id}",
            onerow=1
        )
        #form.pre(ov)


            


events={
    'permissions':permissions
}