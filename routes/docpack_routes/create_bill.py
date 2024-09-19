from lib.core import exists_arg
from .get_bills import get_bills
async def action_create_bill(form,field,R):
  if 'create_bill' in field:
    print("CREATE BILL",form,field,R)
    return await field['create_bill'](form,field,R)

  lst=[]
  summ=exists_arg('summ',R)
  comment=exists_arg('comment',R)
  docpack_id=exists_arg('dogovor_id',R)


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


            
      await form.db.save(
        table='bill',
        data=data,
      );
      lst=await get_bills(form,field,R);

  return {'success':form.success(),'errors':form.errors, 'list':lst}
