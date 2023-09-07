def events_permission(form):
    pass
    #if form.manager['login']!='admin':
    #    form.errors.append('Доступ запрещён')

def events_permission2(form):
    pass
    #print('perm2')

def events_before_code(form):
    pass
    #print('is_before_code')

def before_delete(form):
    pass
    #print('before_detele STARTED!')
    #form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
     
  ],
  #'before_delete':before_delete,
  #'before_code':events_before_code
}