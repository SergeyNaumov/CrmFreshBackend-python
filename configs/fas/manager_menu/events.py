def events_permission1(form):
    print('form: ',form)
    #if form.manager['login']!='admin':
    #    form.errors.append('Доступ запрещён')

def events_permission2(form):
    print('perm2')

def events_before_code(form):
    print('is_before_code')

async def before_delete(form):
    print('before_detele STARTED!')
    form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[

  ],
  'before_delete':before_delete,
  #'before_code':events_before_code
}