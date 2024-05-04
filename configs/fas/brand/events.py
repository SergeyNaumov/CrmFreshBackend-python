async def permission(form):
    perm=form.manager['permissions']
    if not(perm['brand']):
        form.errors.append('Доступ запрещён')
    
    #if form.manager['login']!='admin':
    #    form.errors.append('Доступ запрещён')

async def events_permission2(form):
    pass

async def events_before_code(form):
    #print('is_before_code')
    pass

async def before_delete(form):
    pass
    #form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
      permission,
      
  ],
  'before_delete':before_delete,
  'before_code':events_before_code
}