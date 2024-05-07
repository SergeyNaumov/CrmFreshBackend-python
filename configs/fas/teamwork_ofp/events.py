from lib.core import exists_arg, join_ids
from lib.send_mes import send_mes
from lib.core_crm import get_manager, get_owner, get_email_list_from_manager_id

async def get_old_values(form):
  product_hash={
    3:'Банковская Гарантия (Аукцион выигран с нашей помощью)',
    4:'Банковская Гарантия (есть победитель)',
    5:'Банковская гарантия, консультация для продажи тарифа (50/50 от оплаченного тарифа)',
    10:'Банковская гарантия (консультация на будущее)',
    7:'Тендерный займ (нужен под конкретный аукцион)',
    8:'Подготовка документации',
    9:'Юридические услуги (разное)',
    14:'Юридические услуги (ФАС)',
    15:'Юридические услуги (Арбитраж)',
    11:'Оформление сро, Лицензий, Допусков',
    12:'Лизинг',
    13:'Факторинг'
  };

  ov=None
  if form.id:

    """
      mfin.name mfin__name,mfin.id mfin__id,
            mfin.group_id mfin__group_id,

      LEFT JOIN manager mfin ON (mfin.id=u.manager_fin)
    """
    ov=await form.db.query(
      query='''
        SELECT
                  wt.teamwork_ofp_id as id, wt.regnumber, wt.user_id, wt.product, '' as link, '' as product_label, wt.manager_from, wt.manager_to, wt.manager_to2,
                  wt.group_id, u.firm, u.inn, mf.id mf__id, mf.group_id manager_from_group, mf.email manager_from_email,
                  mf.phone manager_from_phone,
                  mt.group_id manager_to_group, mt2.group_id manager_to2_group,
                  mt.email manager_to_email, mt.phone manager_to_phone,
                  mt2.email manager_to2_email, mt2.phone manager_to2_phone,
                  u.city, u.firm,
                  mu.name mu__name,
                  mg.header mg__header, mg.id m__group_id,
                  m_oso.id m_oso__id, m_oso.email m_oso__email, m_oso.group_id m_oso__group_id,
                  ( wt.product in (9,14,15) and wt.dat_session<>'0000-00-00' and date(wt.dat_session)<=curdate() and wt.win_status=0) block_card,
                  mfg.owner_id mfg__owner, mgu.owner_id mgu__owner, mgu.id mgu__id, if(b.header is null,'',b.header) brand
                FROM
                  teamwork_ofp wt
                  LEFT JOIN user u ON (u.id=wt.user_id)
                  LEFT JOIN brand b ON u.brand_id=b.id
                  LEFT JOIN manager mf ON (mf.id=wt.manager_from)
                  LEFT JOIN manager_group mfg ON mfg.id=mf.group_id
                  LEFT JOIN manager mt ON (mt.id=wt.manager_to)
                  LEFT JOIN manager mt2 ON (mt2.id=wt.manager_to2)
                  LEFT JOIN manager mu ON (mu.id=u.manager_id)
                  LEFT JOIN manager_group mg ON (mg.id=mu.group_id)
                  LEFT JOIN manager_group mgu ON (mgu.id=wt.group_id)
                  LEFT JOIN manager m_oso ON (m_oso.id=wt.manager_oso)
                WHERE wt.teamwork_ofp_id=%s
      ''',

      values=[form.id],
      onerow=1,
      errors=form.errors
    )


  if ov:
    if ov.get('product'):
      ov['product_label']=product_hash.get(ov['product'])
    #print('config: ',)
    #ov['link']=f'''<a href="{form.s.config['system_url']}"edit_form/teamwork_ofp/{form.ov['id']}">{form.ov['firm']}</a>'''
    ov['link']=f'''<a href="{form.s.config['system_url']}edit_form/teamwork_ofp/{ov['id']}">{ov["firm"]}</a>'''
    #form.pre({'ov':ov})

    ov['block_card']=0
  form.ov=ov
  form.old_values=ov

async def permissions(form):

  form.is_admin=False
  form.is_manager_from=False
  form.is_manager_to=False
  form.is_manager_to2=False
  form.is_group_owner=False # руководитель группы юристов

  if form.script=='admin_table':
    user_id=exists_arg('cgi_params;user_id',form.R)
    #field['value']=f'user_id:{user_id}'
    form.title=f'Совместная работа (поиск по карте ОП: {user_id})'
    form.search_on_load=True
    #return

  await get_old_values(form)
  # Админ ОФП
  if form.manager['login'] in ('admin', 'akulov','sed','pzm'):
    form.is_admin=True

  #form.pre({'is_admin':form.is_admin})
  #form.pre({'ov':form.ov['firm']})
  if form.ov:

    if form.ov['mgu__owner']==form.manager['id']:
      #form.pre(['ow',form.ov['mgu__owner'],form.manager['id']])
      form.is_group_owner=True

    #form.pre([form.ov['manager_to'],form.manager['id'],form.ov['manager_to']==form.manager['id']])
    #form.pre(form.manager)
    #form.pre([form.ov['manager_to_group'],])
    #print('CHILD_GROUPS_HASH:',form.manager['CHILD_GROUPS_HASH'])



    # Менеджер
    if form.ov['manager_from']==form.manager['id'] or (form.ov['manager_from_group'] in form.manager['CHILD_GROUPS_HASH'] ) :
      form.is_manager_from=True


    # Менеджер ОФП
    if form.ov['manager_to']==form.manager['id'] or (form.ov['manager_to_group'] in form.manager['CHILD_GROUPS_HASH']):
      form.is_manager_to=True


    # менеджер ОФП2
    if form.ov['manager_to2']==form.manager['id'] or (form.ov['manager_to2_group'] in form.manager['CHILD_GROUPS_HASH']):
      form.is_manager_to2=True


    if (form.is_admin or form.is_manager_from or form.is_manager_to or form.is_manager_to2 or form.is_group_owner):
      form.read_only=0


    form.title=f"ОФП: {form.ov.get('firm','')}"
  form.user_id=None


  if form.action in ('new','insert'):
    user_id=form.param('user_id')
    if user_id and user_id.isnumeric(): form.user_id=user_id

  if form.id:
    form.user_id=form.ov.get('user_id')
  #form.pre(form.read_only)



async def before_update(form):
  # Отправка сообщения после назначения юриста
  async def send_lawer_mes(manager_id):
    if not(manager_id):
      return

    subject=f"Создана карточка совместной работы: {form.ov['firm']}, ИНН: {form.ov['inn']}"
    message=f"{form.manager['name']} назначил(а) Вас юристом в карточке <a href='{form.s.config['system_url']}edit_form/teamwork_ofp/{form.id}'>{form.ov['firm']}</a>"
    to_hash={
      manager_id: 1,
      7576: 1 # pzm
    }

    if manager_from:=form.ov.get('mf__id'):
      to_hash[manager_from]=1
      manager=await get_manager( id=manager_from, db=form.db)
      if owner:=await get_owner(cur_manager=manager,db=form.db):
        to_hash[owner['id']]=1


    manager=await get_manager( id=manager_id, db=form.db)

    if owner:=await get_owner(cur_manager=manager,db=form.db):
      to_hash[owner['id']]=1

    to=await get_email_list_from_manager_id(form.db, to_hash)
    if len(to):
      send_mes(
        from_addr='info@fascrm.ru',
        to=','.join(to.keys()),
        subject=subject,
        message=message
      )

  values=form.R.get('values')
  if values:
    old_manager_to=0
    old_manager_to2=0
    old_group_id=0
    if form.ov:
      old_manager_to=form.ov['manager_to']
      old_manager_to2=form.ov['manager_to2']
      old_group_id=form.ov['group_id']

    new_manager_to=values['manager_to']
    new_manager_to2=values['manager_to2']
    new_group_id=values['group_id']

    #print(f"new_manager_to: {new_manager_to} ; old_manager_to: {old_manager_to}")
    if new_manager_to and int(new_manager_to)!=old_manager_to:
      await send_lawer_mes(int(new_manager_to))

    if new_manager_to2 and int(new_manager_to2)!=old_manager_to2:
      await send_lawer_mes(int(new_manager_to2))

    if new_group_id and int(new_group_id)!=old_group_id:
      lower_group=await form.db.query(
        query="select header, owner_id from manager_group where id=%s",
        values=[new_group_id],
        onerow=1,
      )
      if lower_group:
        subject=f"Изменена группа юристов: {form.ov['firm']}, ИНН: {form.ov['inn']}"
        message=f"Только что <b>{form.manager['name']}</b> установил(а) группу юристов <b>{lower_group['header']}</b><br>"+\
        f"В карте ОФП: <a href='{form.s.config['system_url']}edit_form/teamwork_ofp/{form.id}'>{form.ov['firm']}</a>"
        #print(subject)
        #print(message)
        to_hash={
          7576: 1 # pzm
        }

        #print('manager_op:',form.ov['manager_from'])
        if manager_op:=form.ov['manager_from']:
          # менеджер ОП
          to_hash[manager_op]=1

          if owner_op:=await get_owner(manager_id=manager_op,db=form.db):
            to_hash[owner_op['id']]=1

        #if owner:=get_owner(manager_id=manager,db=form.db):
        #  to_hash[owner['id']]=1
        # руководитель группы юристов
        if lower_group['owner_id']:
          to_hash[lower_group['owner_id']]=1

        to=await get_email_list_from_manager_id(form.db, to_hash)
        if len(to):
          send_mes(
            from_addr='info@fascrm.ru',
            to=','.join(to.keys()),
            subject=subject,
            message=message
          )
        #print('to:',to)
        #if owner:=get_owner(cur_manager=manager,db=form.db):
        #form.pre({'lower_group':lower_group})


async def after_save(form):
  manager_id=exists_arg('values;manager_id', form.R)
  user_id=exists_arg('user_id', form.ov)
  if manager_id and form.manager['login'] in ('akulov','sed','pzm'):
    await form.db.query(
      query='UPDATE user set manager_id=%s where id=%s',
      values=[manager_id,user_id],

    )



  #form.pre([old_manager_to,form.values['manager_to']])
  #form.errors.append('test')

async def before_search(form):
  manager=form.manager
  user_id=exists_arg('cgi_params;user_id',form.R)
  qs=form.query_search

  if user_id:
    
    qs['WHERE'].append(f'wt.user_id={user_id}')

  if not(form.is_admin) and not(manager['permissions'].get('lawer')):
    # Если это не админ и не юрист  
    if manager['is_owner'] and len(manager['CHILD_GROUPS']):
      # Если это руководитель
      group_ids=join_ids(manager['CHILD_GROUPS'])

      qs['WHERE'].append(f"(mf.group_id in ({group_ids}) or m.group_id in ({group_ids}))")
    else:
      # Если это менеджер
      manager_id=manager['id']
      qs['WHERE'].append(f"(wt.manager_from={manager_id} or u.manager_id={manager_id})")
    

  #form.pre(form.manager)
  #form.pre(qs['WHERE'])
  #firm=exists_arg('on_filters_hash;firm',form.query_search)

  #if firm.startswith('user_id:'):
  # user_id=firm.replace('user_id:','')
  # form.pre({'user_id':user_id})
  # del qs['on_filters_hash']['firm']
  # form.explain=1

events={
  'permissions':permissions,
  'after_save':after_save,
  'before_update':before_update,
  'before_search':before_search
}
