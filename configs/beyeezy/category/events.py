def events_permission1(form):
    #print('form: ',form)
    if form.id:
        ov=form.db.query(
            query="select * from category where id=%s",
            values=[form.id],
            onerow=1
        )

        if ov:
            form.title=ov['header']
    #if form.manager['login']!='admin':
    #    form.errors.append('Доступ запрещён')

def events_permission2(form):
    ...

def events_before_code(form):
    ...

def before_delete(form):
    print('before_detele STARTED!')
    form.errors.append('Запрещено удалять категории')

events={
  'permissions':[
      events_permission1,
      events_permission2
  ],
  'before_delete':before_delete,
  'before_code':events_before_code
}