from lib.core import exists_arg
from lib.fas.create_fin_card import create_fin_card
from lib.fas.create_ofp_card import create_ofp_card
from routes.docpack_routes.get_bills import get_bills


async def create_bill(form, field,R):
  lst=[]
  summ=exists_arg('summ',R)
  summ_post=exists_arg('summ_post',R)
  service_id=exists_arg('service_id',R)
  comment=exists_arg('comment',R)
  docpack_id=exists_arg('dogovor_id',R)
  tech_fields=exists_arg('tech_fields',R)
  db=form.db
  service=None

  if not(summ):
    form.errors.append('сумма предоплаты не указана или указана не верно')

  if not(summ_post):
    form.errors.append('сумма постоплаты не указана или указана не верно')

  if not(tech_fields):
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
      (number_today,number_bill)=await field['bill_number_rule'](form, field, docpack['ur_lico_id'])
      if not(comment): comment=''

      data={
          'docpack_id':docpack_id,
          'registered':'func:curdate()',
          'number_today':number_today,
          'number':number_bill,
          'manager_id':form.manager['id'],
          'group_id':form.manager['group_id'],
          'summ':summ,
          'comment':comment
      };



      bill_id = await db.save(
        table='bill',
        data=data,
      )
      table=''
      card_id=None
      if service['type']==1:
        # юр. услуга
        card_id = await create_ofp_card(form)
      else:
        # фин. услуга
        card_id = await create_fin_card(form)
        #table='user_fin'
      #print('card_id:',card_id)
      # Узнаём, сколько приложений уже есть в договоре
      max_tech_number = await db.query(
        query="""
          SELECT
            t.num_of_dogovor
          FROM
            tech t
            join bill b ON t.bill_id=b.id
          WHERE b.docpack_id=%s
          ORDER BY t.num_of_dogovor desc limit 1
        """,
        debug=1,
        values=[docpack_id],
        onevalue=1
      )
      print('max_tech_number:',max_tech_number)

      if not(max_tech_number):
        max_tech_number=1
      else:
        max_tech_number+=1

      # Сохранение техзадания


      tech_id = await db.save(
        table='tech',
        data={
          'num_of_dogovor':max_tech_number,
          'bill_id':bill_id,
          'service_id':service_id,
          'card_id':card_id,
          'summ':summ,
          'summ_post':summ_post
        }
      )
      for f in tech_fields:
      	await form.db.save(
      		table='tech_values',
      		data={
      			'tech_id':tech_id,
      			'field_id':f['id'],
      			'value':f['value']
      		}
      	)

      lst=await get_bills(form,field,R);

  return {'success':form.success(),'errors':form.errors, 'list':lst}
