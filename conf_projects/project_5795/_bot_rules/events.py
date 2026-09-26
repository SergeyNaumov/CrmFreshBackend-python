from .update_bot_commands_var import update_bot_commands_var
def permissions(form):
    
    

    
    form.db.query(query="set character_set_results=utf8mb4")
    #print('PERMISSIONS RUNNED',form.s.project_id)
    if not(hasattr(form.s,'project_id')) or not(form.s.project_id):
        print('Доступ запрещён!')
        form.errors.append('Доступ запрещён!')
        return 

    project_id=form.s.project_id
    photo_field=form.get_field('photo')
    photo_field['filedir']=f'./files/project_{project_id}/bot_photos'
    bot_id=form.db.query(
        query='SELECT id from bot where project_id=%s',
        values=[form.s.project_id],
        onevalue=1
    )
    #form.pre({'bot_id:': bot_id})
    if bot_id:
       form.foreign_key='bot_id'
       form.foreign_key_value=bot_id
        #form.load_data({'foreign_key':'bot_id','foreign_key_value':form.s.project_id})
    #else:
    #    form.errors.append('Боты не найдены, обратитесь к администратору')
    #print('PERMISSIONS!',form.foreign_key,form.s.project_id  )

def events_before_code(form):
    pass

def before_delete(form):
    pass
    

def after_save(form):
    if form.id:
        update_bot_commands_var(form)
        #print(f'after_save bot rules {form.foreign_key_value}')
events={
  'permissions':[
      permissions
  ],
  'before_delete':before_delete,
  'before_code':events_before_code,
  'after_save':after_save
}