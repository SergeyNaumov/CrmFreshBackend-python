from lib.core import cur_date
async def paid(form,values):
  paid=values.get('paid',0)
  ov=form.ov
  print('ov_paid:',ov['paid'], 'paid: ',paid )

  if not(ov.get('paid')) and paid:
    return [
      'paid_summ',{'value':ov['summ'],'hide':False},
      'paid_date',{'value':cur_date(),'hide':False}
    ]
  if not(paid):
    return [
      'paid_summ',{'value':0,'hide':True},
      'paid_date',{'value':'','hide':True}
    ]
  return []
ajax={

  'paid':paid
}