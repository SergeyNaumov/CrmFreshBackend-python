async def events_permission1(form):
    print('form: ',form)
    #if form.manager['login']!='admin':
    #    form.errors.append('Доступ запрещён')

async def events_permission2(form):
    print('perm2')

async def events_before_code(form):
    print('is_before_code')

async def before_delete(form):
    print('before_detele STARTED!')
    form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
      events_permission1,
      events_permission2
  ],
  'before_delete':before_delete,
  'before_code':events_before_code
}