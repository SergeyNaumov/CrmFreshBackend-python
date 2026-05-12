from lib.core import exists_arg
from lib.core_crm import get_owner, get_manager_email
from lib.send_mes import send_mes
from .get_bills import get_bills
async def action_create_bill(form,field,R):
  #if 'create_bill' in field:
  #print("CREATE BILL",form,field,R)
  #  return await field['create_bill'](form,field,R)

  lst=[]
  summ=exists_arg('summ',R)
  comment=exists_arg('comment',R)
  docpack_id=exists_arg('dogovor_id',R)
  app_id=R.get('app_id')

  if not(summ):
    form.errors.append('сумма не указана или указана не верно')

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
      if not(type(app_id)==int):
        app_id=0

      data={
          'docpack_id':docpack_id,
          'registered':'func:curdate()',
          'number_today':number_today,
          'number':number_bill,
          'manager_id':form.manager['id'],
          'group_id':form.manager['group_id'],
          'summ':summ,
          'comment':comment,
          'type':0,
          'dogovor_app_id':app_id
      };
            
      bill_id = await form.db.save(
        table='bill',
        data=data,
      );
      manager = await form.db.query(
          query=f'select u.manager_id from user u left join docpack d ON d.user_id=u.id where d.id={docpack_id}', onevalue=1
      )
      if manager and bill_id:
          owner_email = ''
          if owner := await get_owner(manager_id=manager, db=form.db):
              owner_email = await get_manager_email(db=form.db, manager_id=owner['id'])
          manager_email = await get_manager_email(db=form.db, manager_id=manager)
          user_data = await form.db.query(
              query=f"""
                  SELECT u.id, u.address, u.inn, u.firm, GROUP_CONCAT(uc.email) AS emails, ul.firm AS ur_lico, t.header
                  from user u 
                  left join docpack d ON d.user_id=u.id 
                  left join user_contact uc ON uc.user_id = u.id
                  left join ur_lico ul ON ul.id=d.ur_lico_id
                  left join tarif t ON t.id=d.tarif_id
                  where d.id={docpack_id}
              """,
              onerow=1
          )
          bill = await form.db.query(
              query=f"""SELECT b.registered, b.number, b.summ from bill b where b.id={bill_id}""", onerow=1
          )
          message = f"""
              Менеджером {form.manager['name']} выставлен счёт №{bill['number']} на сумму {bill['summ']} от {bill['registered']}\n
              Карта ОП: <a href="/edit_form/user/{user_data['id']}">{user_data['firm']}</a>\n
              Email: {user_data['emails']}\n
              Адрес: {user_data['address']}\n
              ИНН: {user_data['inn']}\n
              Юр.лицо: {user_data['ur_lico']}\n
              Тариф: {user_data['header']}\n
              Комментарий: {comment}"""
          send_mes(
              from_addr='info@fascrm.ru',
              to=f'{manager_email}, {owner_email}',
              subject=f"Выставлен счёт для {user_data['firm']}",
              message=message
          )

      lst=await get_bills(form,field,R);

  return {'success':form.success(),'errors':form.errors, 'list':lst}
