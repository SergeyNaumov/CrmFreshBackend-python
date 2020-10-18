def events_permission1(form):
    print('perm1')

def events_permission2(form):
    print(perm2)

def events_before_code(form):
    print('is_before_code')

def before_delete(form):
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