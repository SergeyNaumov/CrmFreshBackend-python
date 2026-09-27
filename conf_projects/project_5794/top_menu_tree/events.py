async def permissions(form):
    #form.s.project_id=0

    #print('PERMISSIONS RUNNED',form.s.project_id)
    if not(getattr(form.request.state,'project',None)):
        print('Доступ запрещён!')
        form.errors.append('Доступ запрещён!')
        return

    form.foreign_key='project_id'
    form.foreign_key_value=form.request.state.project['project_id']



    form.load_data({'foreign_key':'project_id','foreign_key_value':form.request.state.project['project_id']})

    #icon_field=form.get_field('icon')
    #icon_field['filedir']=f"./files/project_{form.s.project_id}/top_menu"

    print('PERMISSIONS!',form.foreign_key,form.request.state.project['project_id']  )

async def events_before_code(form):
    pass

async def before_delete(form):
    pass


events={
  'permissions':[
      permissions
  ],
  'before_delete':before_delete,
  'before_code':events_before_code
}