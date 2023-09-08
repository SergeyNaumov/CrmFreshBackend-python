from lib.core import exists_arg
from .get_bills import get_bills
def action_create_bill(form,field,R):
  lst=[]
  summ=exists_arg('summ',R)
  comment=exists_arg('comment',R)
  dogovor_id=exists_arg('dogovor_id',R)


  if not(summ):
    form.errors('сумма не указана или указана не верно')

  if not(dogovor_id):
    form.errors('отсутствует параметр dogovor_id')

  

  if form.success():
      (number_today,number_bill)=field['bill_number_rule'](form, field)
      print('number_today:',number_today)
      print('number_bill:',number_bill)
      if not(comment): comment=''          
            
      data={
          'docpack_id':R['dogovor_id'],
          'registered':'func:curdate()',
          'number_today':number_today,
          'number':number_bill,
          'manager_id':form.manager['id'],
          'group_id':form.manager['group_id'],
          'summ':summ,
          'comment':comment
      };
      print('data:',data)


            
      form.db.save(
        table='bill',
        data=data,
      );
      lst=get_bills(form,field,R);

  return {'success':form.success(),'errors':form.errors, 'list':lst}