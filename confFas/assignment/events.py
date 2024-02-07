from lib.core import exists_arg

def permission(form):
    entity = exists_arg('cgi_params;entity',form.R)
    manager=form.manager
    login=manager['login']
    perm=manager['permissions']
    title=''

    if entity=='6':
        title='Уклонения РегРф (список менеджеров)'

    elif entity=='9':
        title='Уклонения Ревизор (список менеджеров)'
    elif entity=='5':
        title='Расторжения РегРф (список менеджеров)'
    elif entity=='8':
        title='Расторжения Ревизор (список менеджеров)'
    elif entity=='7':
        title='Реестр РНП РегРф (список менеджеров)'
    elif entity=='10':
        title='Реестр РНП Ревизор (список менеджеров)'

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

def events_permission2(form):
    pass

def events_before_code(form):
    #print('is_before_code')
    pass

def before_delete(form):
    pass
    #form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
      permission,
      
  ],
  'before_delete':before_delete,
  'before_code':events_before_code
}