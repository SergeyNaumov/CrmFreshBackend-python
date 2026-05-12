# Привязка приложения к СР
from lib.core import exists_arg, date_to_rus, join_ids

async def action_unlink_sr(form,field,R):
    db=form.db
    errors=[]

    app_id=R.get('app_id')

    if not(app_id):
        errors.append('не передан параметр app_id')

    if not(len(errors)):
        app = await db.query(
            query="""
                UPDATE dogovor_app SET card_id=0 WHERE id=%s
            """,
            values=[R['app_id']],
            onerow=1
        )
        return {'success':True,'errors':errors}

    return {'success':False,'errors':errors}