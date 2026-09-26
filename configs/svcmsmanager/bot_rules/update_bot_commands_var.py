async def update_bot_commands_var(form):
    var = await form.db.query(
        query="select * from bot_const where bot_id=%s and name=%s",
        values=[form.foreign_key_value,'_last_update_botcommands'],
        onerow=1
    )
    if var:
        await form.db.query(
            query="UPDATE bot_const set value=unix_timestamp(now()) where bot_id=%s and name=%s",
            values=[form.foreign_key_value,'_last_update_botcommands'],
            debug=1
        )
    else:
        await form.db.query(
            query='INSERT INTO bot_const(bot_id,name,value) values(%s,%s,unix_timestamp(now()) )',
            debug=1,
            values=[form.foreign_key_value,'_last_update_botcommands'],
        )
