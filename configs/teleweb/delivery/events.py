def permissions(form):
    if not(hasattr(form.s,'shop_id')) or not(form.s.shop_id):
        form.errors.append('Доступ запрещён!')
        return 
    
    form.foreign_key='shop_id'
    form.foreign_key_value=form.s.shop_id   


    
    

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