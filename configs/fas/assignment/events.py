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
        '20':'Ответчики ФАС-сервис (список менеджеров)',
        '21':'Уклонения AUZ (список менеджеров)',
        '22':'Расторжения AUZ (список менеджеров)',
        '23':'Реестр РНП AUZ (список менеджеров)',
        '24':'Ответчики AUZ (список менеджеров)',
    }
    if form.id:
        form.ov=await form.db.query(
            query=f"select * from {form.work_table} where id=%s",
            values=[form.id],
            onerow=1
        )
        
        if t:=form.ov.get('type'):
            entity=str(t)
            form.foreign_key_value=t
        else:
            form.errors.append('Ошибка, не указан type, обратитесь к программисту')

    if entity in entity_dict:
        title=entity_dict.get(entity)
    
    is_regrf=False
    is_fas_servis=False
    is_revisor=False
    is_bz_info=False
    is_auz=False
    #is_auz=
    if entity in ('5','6','7','11'):
        is_regrf=True
    if entity in ('17','18','19','20'):
        is_fas_servis=True
    if entity in ('8','9','10','12'):
        is_revisor=True
    if entity in ('13','14','15','16'):
        is_bz_info=True
    if entity in ('21','22','23','24'):
        is_auz=True

    if entity:
        form.add_where=f"wt.type={entity}"
        form.foreign_key_value=int(entity)

    if not(entity) and form.script!='delete_element' and not(form.script=='edit_form' and form.id):
        form.errors.append(f'не указано entity!')
    #form.explain=1


    if login in ('akulov','pzm','sed','admin') or  (is_auz and login in ('anna')) or \
    (is_regrf and login in ('lgf')) or (is_fas_servis and login in ('lgf')) or (is_revisor and login in ('ahmetova','naumova')) or (is_bz_info and login in ('veronika')):
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