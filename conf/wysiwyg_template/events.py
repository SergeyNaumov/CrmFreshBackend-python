def permissions(form):
    if not(hasattr(form.s,'project_id')) or not(form.s.project_id):
        
        form.errors.append('Доступ запрещён!')
        return 
        
    form.foreign_key='project_id'
    form.foreign_key_value=form.s.project_id  
    form.load_data({'foreign_key':'project_id','foreign_key_value':form.s.project_id})

#def events_before_code(form):
    #pass

#def before_delete(form):
#    pass
    

events={
  'permissions':[
      permissions
  ],
  #'before_delete':before_delete,
  #'before_code':events_before_code
}