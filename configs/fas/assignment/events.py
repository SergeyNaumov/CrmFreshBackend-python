from lib.core import exists_arg

async def permission(form):
    entity = exists_arg('cgi_params;entity',form.R)
    if entity:
        form.type_value=entity
    manager=form.manager
    login=manager['login']
    perm=manager['permissions']
    title=''
    entity_dict={
        '6':'Уклонения РегРф (список менеджеров)',
        '7':'Реестр РНП РегРф (список менеджеров)',
        '8':'Расторжения Ревизор (список менеджеров)',
        '9':'Уклонения Ревизор (список менеджеров)',
        '10':'Реестр РНП Ревизор (список менеджеров)',
        '11':'Ответчики РегРФ (список менеджеров)',
        '12':'Ответчики НС Ревизор (список менеджеров)',
        '13':'Ответчики BzInfo(список менеджеров)',
        '14':'Расторжения BzInfo (список менеджеров)',
        '15':'Уклонения BzInfo (список менеджеров)',
        '16':'Реестр РНП BzInfo (список менеджеров)',
        '17':'Уклонения ФАС-сервис (список менеджеров)',
        '18':'Расторжения ФАС-сервис (список менеджеров)',
        '19':'РНП ФАС-сервис (список менеджеров)',
        '20':'Ответчики ФАС-сервис (список менеджеров)'
    }
    if form.id:
        form.ov=await form.db.query(
            query=f"select * from {form.work_table} where id=%s",
            values=[form.id],
            onerow=1
        )
        if t:=form.ov.get('type'):
            entity=t
            form.foreign_key_value=t
        else:
            form.errors.append('Ошибка, не указан type, обратитесь к программисту')

    if entity in entity_dict:
        title=entity_dict.get(entity)

    if entity:
        form.add_where=f"wt.type={entity}"
        form.foreign_key_value=int(entity)

    if not(entity) and form.script!='delete_element' and not(form.script=='edit_form' and form.id):
        form.errors.append(f'не указано entity!')
    #form.explain=1


    if login in ('akulov','pzm','sed','anna','admin') or login=='lgf' and entity in ('6','5','7') or login=='sheglova' and entity in ('9','8','10'):
        form.read_only=0
        form.not_create=0
        form.make_delete=1
    else:
        form.errors.append('доступ запрещён')
        form.read_only=1
        form.not_create=1
        form.make_delete=0


    form.title=title

async def events_permission2(form):
    pass

async def events_before_code(form):
    #print('is_before_code')
    pass

async def before_delete(form):
    pass
    #form.errors.append('Вам запрещено удалять!')

async def after_update(form):
    form.pre({'form.ov':form.ov, 'values':form.values})


events={
  'permissions':[
      permission,
      
  ],
  'before_delete':before_delete,
  'before_code':events_before_code,
  #'before_update':before_update
}