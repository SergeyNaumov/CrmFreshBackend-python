def events_permissions(form):
    if form.id:
      form.ov=form.db.query(
        query="select * from manager where id=%s",
        values=[form.id],
        onerow=1
      )
      form.title='Учётные записи: '+form.ov['name']

def events_before_code(form):
    print('is_before_code')

def before_delete(form,opt):
    print('before_detele STARTED!')
    #form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
      events_permissions
    
  ],
  'before_delete':before_delete,
  'before_code':events_before_code
}