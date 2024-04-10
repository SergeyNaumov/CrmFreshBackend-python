from lib.core import exists_arg
from .create_ofp_card import *
from .create_bbg_card import *
from .filters_for_manager_op import prepare_filters_for_manager_op
from .find_inn_doubles import prepare_filters_for_find_inn_doubles
from .components_actions import components_actions

def permissions(form):
  
  R=form.R
  db=form.db

  form.ov={}

  if form.id:

    form.ov=db.query(
      query=f"""
        SELECT
          u.*, m.group_id
        FROM
          user u
          LEFT JOIN manager m ON m.id=u.manager_id
        WHERE u.id={form.id}""",
      onerow=1
    )

  # Для работы компонентов (статистика и т.п.)
  components_actions(form)

  if form.response:
    # если есть кастомный ответ, тогда завершаем permissions

    return



  # Смотрим, какой бренд у данного менеджера
  manager_group=db.query(
    query="select * from manager_group where id=%s",
    values=[form.manager['group_id']], # 
    onerow=1
  )

  manager_brand=0
  if manager_group and manager_group['brand_id']:
      manager_brand=manager_group['brand_id']
  
  form.manager_brand=manager_brand
  
  perm=form.manager['permissions']



  # Убираем поле "бренд" всем, у кого нет прав доступ
  if not(perm.get('show_brand_in_card_op')):
    form.remove_field('brand_id')
  # Список фильтров
  if form.script=='admin_table':

    if perm.get('is_manager_op'):
      # особый список фильтров для менеджеров ОП
      prepare_filters_for_manager_op(form)

    # превращаем инструмент в "поиск по ИНН"
    inn=exists_arg('cgi_params;find_inn_doubles',R)
    if inn or inn=='':
      prepare_filters_for_find_inn_doubles(form,inn)

  if perm['user_delete']:
    form.make_delete=1
  
  
  # Если не разрешено видеть все бренды
  if not perm['user_show_all_brand']:
    form.add_where=f'wt.brand_id={manager_brand}'



  if form.id:
      if form.ov:

        form.title=form.ov['firm']

      # Создание карты ОФП
      if exists_arg('cgi_params;action',R) == 'create_ofp_card':
          create_ofp_card(form)
      
      # Создание карты ББГ
      if exists_arg('cgi_params;action',R) == 'create_bbg_card':
          create_bbg_card(form)

      #form.pre({'manager_brand':manager_brand})
      # В карте выбран брэнд
      if not perm['user_show_all_brand']:
        if form.ov['brand_id'] and form.ov['brand_id'] != manager_brand:
          form.errors.append('Вам запрещено просматривать данную карту (Вы работаете в рамках другого бренда)')

      
      
      # Возможность редактировать все карты ОП
      if perm.get('user_edit_all'):
        form.read_only=0
      
      # Возможность редактировать руководителю
      if form.ov:
        if form.manager['CHILD_GROUPS_HASH'].get(form.ov['group_id']):
          form.is_owner=True # владелец карты
          if form.manager['is_owner']:
            form.is_owner_group=True


        if form.ov['manager_id']==form.manager['id'] or form.is_owner:
          form.read_only=0
      #form.read_only=0
  
  if form.action in ('new', 'insert'):
      form.read_only=0

def after_insert(form):
  set_str=[]
  #print('after_insert!!!')

  perm=form.manager['permissions']
  # Если не может менять бренд
  if not(perm['user_change_brand']) and form.manager_brand:
    set_str.append(f"brand_id={form.manager_brand}")

  # если не может менять менеджера, то менеджер назначается текущим
  if not perm['card_op_make_change_manager']:
    set_str.append(f"manager_id={form.manager['id']}")
  
  
  if len(set_str):
    form.db.query(
      query=f"UPDATE user set {', '.join(set_str)} where id=%s",
      values=[form.id],
      #errors=form.errors,
      #debug=form.explain,
      #debug=1
    )

def before_search(form):
  qs=form.query_search
  #form.pre(qs)

  if not('archive' in qs['on_filters_hash']):
    #form.add_where.append('wt.archive=0')
    qs['WHERE'].append('wt.archive=0')

  #form.pre(qs['WHERE'])
  #form.explain=1

events={
  'permissions':permissions,
  'after_insert':after_insert,
  'before_search':before_search
}