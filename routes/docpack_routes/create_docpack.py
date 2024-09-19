from .lib import need_manager_fld
from lib.core import exists_arg

# Создание пакета документов + договора

async def action_create_docpack(form, field, R):
    need_manager=need_manager_fld(form)
    manager_id=form.manager['id']
        
    if need_manager and exists_arg('manager_id', R):
        manager_id=R['manager_id']
        
    docpack_foreign_key=field['docpack_foreign_key']

    if form.success():
        number,number_today = await field['dogovor_number_rule'](form, field, R['ur_lico_id'])

        
        data={
            docpack_foreign_key:form.id,
            'tarif_id':R['tarif_id'],
            'ur_lico_id':R['ur_lico_id'],
            'manager_id':manager_id,
            'registered':'func:now()'
        };

        docpack_id=await form.db.save(
                    table='docpack',
                    data=data,
                    errors=form.errors
        );
        
        data={
            'docpack_id':docpack_id,
            'registered':'func:curdate()',
            'number_today':number_today,
            'number':number
        }

        await form.db.save(
            table='dogovor',
            data=data,
        );
        

    return {'success':form.success(),'errors':form.errors}