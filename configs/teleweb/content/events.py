def permissions(form):
    #form.s.project_id=0
    #print('EVENTS PERMISSIONS!')
    #print('project_id:',form.s.project_id)
    if not(hasattr(form.s,'shop_id')) or not(form.s.shop_id):
        form.errors.append('Доступ запрещён!')
        return 
    
    form.foreign_key='shop_id'
    form.foreign_key_value=form.s.shop_id   

    # Определяем ajax для контроля уникальности url-а    
    def ajax_url(form,v):
        error=''

        where=[f'shop_id={form.s.shop_id}']
        
        if form.id:
            where.append(f'{form.work_table_id}<>{form.id}')

        where.append(f'url=%s')
    
        exists=form.db.getrow(
            table=form.work_table,
            where=(' and '.join(where)),
            values=[v['url']],
        )

        if exists:
            error='такой url уже используется'


        return ['url',{'error':error}]


    form.ajax={'url':ajax_url}
    
    

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
