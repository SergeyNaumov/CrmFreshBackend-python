def events_permission1(form):
    
    if form.script=='video_list':
        pass
        


    else:
        # Редактировать дерево запрещаем всем кроме админа
        if form.manager['type']!=1:
            form.errors.append('Доступ запрещён')



def events_before_code(form):
    print('is_before_code')

def before_delete(form):
    print('before_detele STARTED!')
    form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
      events_permission1,

  ],
  'before_delete':before_delete,
  'before_code':events_before_code
}