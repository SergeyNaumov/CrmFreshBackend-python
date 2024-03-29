from lib.core import exists_arg
def save_summ_bill(form,field, R):
  bill_id=R.get('bill_id')
  summ=R.get('summ')

  if not( len(form.errors)):
    bill=form.db.query(
      query="select * from bill where id=%s",
      values=[bill_id],
      onerow=1
    )


    if bill:
      form.db.query(
        query="UPDATE bill set summ=%s where id=%s",
        values=[summ,bill_id]
      )

    else:
      form.errors.append('счёт не найден')
  return {
    'success':form.success(),
    'bill':bill,
    'errors': form.errors
  }