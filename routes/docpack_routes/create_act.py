from lib.core import exists_arg
from .get_acts import get_acts
def action_create_act(form,field,R):
  lst=[]
  summ=exists_arg('summ',R)
  #comment=exists_arg('comment',R)
  bill_id=exists_arg('bill_id',R)
  registered=exists_arg('date',R)


  if not(summ):
    form.errors.append('сумма не указана или указана не верно')

  if not(bill_id):
    form.errors.append('отсутствует параметр bill_id')

  

  if form.success():
      ur_lico_id=form.db.query(
        query="""
          SELECT
            dp.ur_lico_id
          from
            bill b
            join docpack dp ON b.docpack_id=dp.id
          WHERE
            b.id=%s
        """,
        values=[bill_id],

        onevalue=1
      )
      if not(ur_lico_id):
        form.errors.append(f'не удалось определить юрлицо для счёта {bill_id}')
      else:
        (number_today,number_act)=field['act_number_rule'](form, field,registered,ur_lico_id)


        data={
            'bill_id':bill_id,
            'registered':registered,
            'number_today':number_today,
            'number':number_act,
            'manager_id':form.manager['id'],
            'summ':summ,

        };



        form.db.save(
          table='act',
          data=data,
        );
        lst=get_acts(form,field,R);

  return {'success':form.success(),'errors':form.errors, 'list':lst}
