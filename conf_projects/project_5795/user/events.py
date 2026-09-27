
#from lib.CRM.plugins.InExtUrl import InExtUrl
        
async def permissions(form):


    bot_id=await form.db.query(
        query="select id from bot where project_id=%s",
        values=[form.request.state.project['project_id']],
        onevalue=1
    )
    if not(bot_id):
        form.errors.append('не найден id бота, обратитесь к разработчику')

    form.foreign_key='bot_id'
    form.foreign_key_value=bot_id
        
    if form.script=='edit_form' and form.id:
        form.ov=await form.db.query(
            query=f"select * from {form.work_table} where {form.work_table_id}={form.id}",
            onerow=1
        )


events={
    'permissions':permissions
}