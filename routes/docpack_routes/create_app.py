from lib.core import exists_arg
from .get_bills import get_bills
"""
CREATE TABLE `dogovor_app` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `service_id` int unsigned DEFAULT NULL,
  `card_id` int unsigned NOT NULL COMMENT 'это карта teamwork_ofp или user.fin в зависимости от service.type',
  `registered` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `summ` int unsigned NOT NULL DEFAULT '0',
  `summ_post` int unsigned NOT NULL DEFAULT '0',
  `postpaid_bill_id` int unsigned NOT NULL DEFAULT '0',
  `num_of_dogovor` tinyint unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `service_id` (`service_id`),
  CONSTRAINT FOREIGN KEY (`service_id`) REFERENCES `service` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3 COMMENT='Приложение к договору';

CREATE TABLE `app_values` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `dogovor_app_id` int unsigned DEFAULT NULL,
  `field_id` int unsigned DEFAULT NULL,
  `value` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  CONSTRAINT  FOREIGN KEY (`field_id`) REFERENCES `service_field` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT  FOREIGN KEY (`dogovor_app_id`) REFERENCES `dogovor_app` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COMMENT='Значения доп. полей в технических характеристиках';
"""
async def action_create_app(form,field,R):
  #if 'create_bill' in field:
  #  print("CREATE BILL",form,field,R)
  #  return await field['create_bill'](form,field,R)

  bills_data={}
  summ=exists_arg('summ',R)
  summ_post=exists_arg('summ_post',R)
  tech_fields=R.get('tech_fields')
  service_id=exists_arg('service_id',R)
  comment=exists_arg('comment',R)
  docpack_id=exists_arg('dogovor_id',R)
  service=None

  if not(summ):
    form.errors.append('сумма предоплаты не указана или указана не верно')

  if not(summ_post):
    form.errors.append('сумма постоплаты не указана или указана не верно')
  #print('tech_fields:',tech_fields)
  if not('tech_fields' in R):
    form.errors.append('не получены дополнительные поля')

  if not(service_id):
    form.errors.append('не указан параметр service_id')
  else:
    service = await form.db.query(
      query=f"select * from {field['service_table']} where id=%s",
      values=[service_id],
      onerow=1
    )
    if not(service):
      form.errors.append('Услуга не найдена')

  if not(docpack_id):
    form.errors.append('отсутствует параметр dogovor_id')
  else:
    docpack=await form.db.query(
      query="SELECT * from docpack where id=%s",
      values=[docpack_id],
      onerow=1
    )
    if not(docpack):
      form.errors.append(f'пакет документов {docpack_id} не найден')

    elif not(docpack.get('ur_lico_id')):
      form.errors.append(f'не удалось определить юрлицо для пакета документов {docpack_id}')


    if form.success():
        db=form.db
        # Узнаём максимальный номер приложения в рамках данного договора
        max_app_number = await db.query(
            query="""
              SELECT
                a.num_of_dogovor
              FROM
                dogovor_app a
                join bill b ON a.id=b.dogovor_app_id
              WHERE b.docpack_id=%s
              ORDER BY a.num_of_dogovor desc limit 1
            """,
            debug=1,
            values=[docpack_id],
            onevalue=1
        )
        if not(max_app_number):
            max_app_number=1
        else:
            max_app_number+=1

        print('max_app_number:',max_app_number)

        app_id = await db.save(
            table='dogovor_app',
            data={
              'num_of_dogovor':max_app_number,
              'dogovor_id':docpack_id,
              'service_id':service_id,
              #'card_id':card_id,
              'summ':summ,
              'summ_post':summ_post
            },
            debug=1
        )
        for f in tech_fields:
            await form.db.save(
                table='dogovor_app_values',
                data={
                    'dogovor_app_id':app_id,
                    'field_id':f['id'],
                    'value':f['value']
                }
            )

        # Теперь создаём счёт на предоплату
        (number_today,number_bill)=await field['bill_number_rule'](form, field, docpack['ur_lico_id'])


        bill_id = await db.save(
            table='bill',
            data={
              'docpack_id':docpack_id,
              'registered':'func:curdate()',
              'number_today':number_today,
              'number':number_bill,
              'manager_id':form.manager['id'],
              'group_id':form.manager['group_id'],
              'summ':summ,
              'type':1,
              'dogovor_app_id':app_id,
              'comment':f"Предоплата в рамках приложения №{max_app_number} к договору"
            },
            debug=1
        )
        # await form.db.save(
        #   table='bill',
        #   data=data,
        # );
        bills_data=await get_bills(form,field,R);

    return {'success':form.success(),'errors':form.errors, 'bills':bills_data}
