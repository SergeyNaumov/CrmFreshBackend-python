def permissions(form):
    #form.s.project_id=0
    
    #print('PERMISSIONS RUNNED',form.s.shop_id)
    if not(hasattr(form.s,'shop_id')) or not(form.s.shop_id):
        print('Доступ запрещён!')
        form.errors.append('Доступ запрещён!')
        return 
    
    #form.pre(form.s.shop_id)
    form.foreign_key='shop_id'
    form.foreign_key_value=form.s.shop_id  
    form.load_data({'foreign_key':'shop_id','foreign_key_value':form.s.shop_id})
    field_photo=form.fields[1]
    field_photo['filedir']=field_photo['filedir'].replace('<%shop_id%>',str(form.s.shop_id) )
    #f'./files/project_{form.s.shop_id}/catalog'
   # form.pre(field_photo)
    #print('PERMISSIONS!',form.foreign_key,form.s.shop_id  )

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