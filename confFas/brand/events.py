def permission(form):
    pass
    #if form.manager['login']!='admin':
    #    form.errors.append('Доступ запрещён')

def events_permission2(form):
    pass

def events_before_code(form):
    #print('is_before_code')
    pass

def before_delete(form):
    pass
    #form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
      permission,
      
  ],
  'before_delete':before_delete,
  'before_code':events_before_code
}