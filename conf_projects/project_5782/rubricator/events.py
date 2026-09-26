def permissions(form):
    project_id=form.s.project_id
    #form.pre(project_id)
    form.work_table=f'struct_{project_id}_rubricator'

    if form.script=='edit_form' and form.id:
        form.ov=form.db.query(
            query=f"select * from {form.work_table} where {form.work_table_id}={form.id}",
            onerow=1
        )
        #form.pre(ov)

events={
    'permissions':permissions
}