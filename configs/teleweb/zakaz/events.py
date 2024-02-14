def permissions(form):
    #form.s.project_id=0
    #print('EVENTS PERMISSIONS!')
    #print('project_id:',form.s.project_id)
    if not(hasattr(form.s,'shop_id')) or not(form.s.shop_id):
        form.errors.append('Доступ запрещён!')
        return 
    
    form.foreign_key='shop_id'
    form.foreign_key_value=form.s.shop_id    
    
    #catalog_id_fld=form.fields[2]
    #catalog_id_fld['where']=f'shop_id={form.s.shop_id}'
    
    
    

def events_before_code(form):
    pass

def before_delete(form):
    pass
    

events={
  'permissions':[
      permissions
  ],
  'before_delete':before_delete,
  'before_code':events_before_code
}