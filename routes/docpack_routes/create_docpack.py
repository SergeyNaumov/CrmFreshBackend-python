from datetime import date

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
        
        # проверяем наличие реквизитов в карте бухгалтера для данной компании
        buhgalter_card_requisits=await form.db.query(
            query='select * from buhgalter_card_requisits where id=%s and user_id=%s',
            errors=form.errors,
            values=[R.get('buhgalter_card_requisits_id'), form.id], onerow=1
        )
        #print('buhgalter_card_requisits:',buhgalter_card_requisits)
        if buhgalter_card_requisits:
            # проверяем, создавался ли уже ранее пакет документов в рамках этого года (для этих реквизитов)
            exists_docpack = await form.db.query(
                query='''
                    select
                        dp.id, if(ul.firm,ul.firm,'') ur_lico
                    from
                        docpack dp
                        LEFT JOIN ur_lico ul ON dp.ur_lico_id = ul.id
                        LEFT JOIN buhgalter_card_requisits bcr ON bcr.id=dp.buhgalter_card_requisits_id 
                    where dp.user_id=%s and ur_lico_id=%s and bcr.inn=%s and YEAR(dp.registered)=YEAR(curdate())
                ''',
                values=[form.id, R['ur_lico_id'], buhgalter_card_requisits['inn']],
                onerow=1,
                debug=1
            )
            #print('exists_docpack:',exists_docpack)
            if exists_docpack:
                form.errors.append(f"Пакет документов с юридическим лицом {exists_docpack['ur_lico']} уже был создан в рамках этого года")

        
        

        
        if not buhgalter_card_requisits:
            form.errors.append('Не указаны реквизиты при создании пакета документов')
            return {'success': form.success(), 'errors': form.errors}

        
        if form.success():
            # create docpack
            docpack_id=await form.db.save(
                        table='docpack',
                        errors=form.errors,
                        data={
                            docpack_foreign_key:form.id,
                            'buhgalter_card_requisits_id':R['buhgalter_card_requisits_id'],
                            'tarif_id':R['tarif_id'],
                            'ur_lico_id':R['ur_lico_id'],
                            'manager_id':manager_id,
                            'registered':'func:now()'
                        },
            )
            # create fogovor
            await form.db.save(
                table='dogovor',
                errors=form.errors,
                data={
                    'docpack_id':docpack_id,
                    'registered':'func:curdate()',
                    'number_today':number_today,
                    'number':number
                }
            )
        

    return {'success':form.success(),'errors':form.errors}