def events_permission1(form):
    
    if form.script=='video_list':
        #pass
        if not form.manager['access_to_video']:
            form.errors.append('Вам запрещён доступ к видеоматериалам')
            return        

        if form.manager['type']==1:
            form.links=[
                {
                    'type':'url',
                    'link':'/admin_tree/video_lessions',
                    'description':'Редактирование видео'
                },
            ]
    else:
        # Редактировать дерево запрещаем всем кроме админа
        if form.manager['type']!=1:
            form.errors.append('Доступ запрещён')



def events_before_code(form):
    #print('is_before_code')
    pass

def before_delete(form):
    #print('before_detele STARTED!')
    form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
      events_permission1,

  ],
  'before_delete':before_delete,
  'before_code':events_before_code
}