from lib.core import exists_arg, join_ids
from lib.send_mes import send_mes
from lib.core_crm import get_manager, get_owner, get_email_list_from_manager_id
async def send_after_create(form):
  ov=form.ov ; manager_id=form.manager['id']
  # PZM: При создании карты уведомление идет мне, sed, менеджеру ОП который создал и его руководителю
  if form.ov and not(form.ov['create_sended']):
      
      to={7576: True, 12057: True, 4201: True, manager_id: True} # pzm, sed, Агиб
      owner=await get_owner(manager_id=manager_id,db=form.db)
      if owner and owner.get('id'):
        form.pre({'owner':owner})
        to[owner['id']]=True

      to_emails=await get_email_list_from_manager_id(form.db, to)
      #form.pre({'to_emails':to_emails})
      send_mes(
        from_addr='info@fascrm.ru',
        to=','.join(to_emails.keys()),
        subject="Создана новая карта фин. услуг",
        message=f"<p>Только что {form.manager['name']} создал(а) карту Фин. услуг для компании: <b>{ov['firm']}</b>( ИНН: {ov['inn']})</p>"+\
                f"<p><a href='{form.s.config['system_url']}edit_form/user_fin/{form.id}'>Перейти в карту</a></p>"
      )
      await form.db.query(query=f"UPDATE user_fin set create_sended WHERE id={form.id}")

async def get_old_values(form):
  product_hash={
    1:'Банковская гарантия (есть победитель)',
    2:'Банковская гарантия (консультация на будущее)',
    3:'Тендерный займ',
    4:'Лизинг',
    7:'Оформление СРО / лицензий / допусков',
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
          wt.id, wt.rnt, wt.create_sended, wt.user_id, wt.product, '' as link, '' as product_label, wt.group_id, wt.manager_id, wt.manager_fin, wt.underwriter,
          wt.group_id, u.firm, u.inn, m.group_id manager_group, m.email manager_email,
          m.phone manager_phone, m_fin.group_id m_fin__group_id, m_un.group_id m_un__group_id,
          mfg.owner_id mfg__owner, mgu.owner_id mgu__owner, mgu.id mgu__id, if(b.header is null,'',b.header) brand, b.logo brand_logo
        FROM
          user_fin wt
          LEFT JOIN user u ON (u.id=wt.user_id)
          LEFT JOIN brand b ON u.brand_id=b.id
          LEFT JOIN manager m ON (m.id=wt.manager_id)
          LEFT JOIN manager_group mfg ON mfg.id=m.group_id
          LEFT JOIN manager m_fin ON (m_fin.id=wt.manager_fin)
          LEFT JOIN manager m_un ON (m_un.id=wt.underwriter)
          LEFT JOIN manager mu ON (mu.id=u.manager_id)
          LEFT JOIN manager_group mg ON (mg.id=mu.group_id)
          LEFT JOIN manager_group mgu ON (mgu.id=wt.group_id)
        WHERE wt.id=%s
      ''',

      values=[form.id],
      onerow=1,
      errors=form.errors
    )
    form.ov={}
    #print('ov:',ov)

  if ov:
    #if ov.get('product'):
    ov['product_label']=product_hash.get(ov['product'],'')
    
  #   #print('config: ',)
  
    ov['link']=f'''<a href="{form.s.config['system_url']}edit_form/user_fin/{ov['id']}">{ov["firm"]}</a>'''
    #form.pre({'ov':ov})
    #form.pre(ov)
  #   ov['block_card']=0
  form.ov=ov
  form.old_values=ov

async def permissions(form):

  form.is_admin=False
  form.is_manager=False
  form.is_manager_fin=False
  form.is_manager_fin_owner=False

  form.is_underwriter=False
  form.is_group_owner=False # руководитель группы финансистов
  if form.script=='admin_table':
    user_id=exists_arg('cgi_params;user_id',form.R)
    #field['value']=f'user_id:{user_id}'
    if user_id:
      form.title=f'Совместная работа фин. услуг (поиск по карте ОП: {user_id})'
    form.search_on_load=True
    #return

  await get_old_values(form)
  # Админ юр. услуг
  if form.manager['login'] in ('admin', 'akulov','sed','pzm'):
    form.is_admin=True

  #form.pre({'is_admin':form.is_admin})
  #form.pre({'ov':form.ov['firm']})
  if form.ov:

    if form.ov['mgu__owner']==form.manager['id']:
      form.is_group_owner=True


    # Менеджер
    if form.ov['manager_id']==form.manager['id'] or (form.ov['manager_group'] in form.manager['CHILD_GROUPS_HASH'] ) :
      form.is_manager=True


    # Менеджер фин. услуг
    if form.ov['manager_fin']==form.manager['id'] or (form.ov['m_fin__group_id'] in form.manager['CHILD_GROUPS_HASH']):
      form.is_manager_fin=True

    if form.ov['mgu__owner']==form.id or form.is_manager:
      # Руководитель менеджера фин. услуг
      form.is_manager_fin_owner=True
      form.is_manager_fin=True

    # Андеррайтер
    if form.ov['underwriter']==form.manager['id'] or (form.ov['m_un__group_id'] in form.manager['CHILD_GROUPS_HASH']):
      form.is_underwriter=True


    
    if form.is_admin or form.is_manager_fin:
    #if (form.is_admin or form.is_manager_from or form.is_manager_to or form.is_manager_to2 or form.is_group_owner):
      form.read_only=0
    elif form.is_underwriter or form.is_manager:
      for f in form.fields:
        form.read_only=0
        if f['name']=='memo':
          f['read_only']=False
        else:
          f['read_only']=True

    form.title=f"Фин. Услуги: {form.ov.get('firm','')}"
  form.user_id=None


  if form.action in ('new','insert'):
    user_id=form.param('user_id')
    if user_id and user_id.isnumeric(): form.user_id=user_id

  if form.id:
    form.user_id=form.ov.get('user_id')
    #
  #form.pre(form.ov)



async def before_update(form):
  # Отправка сообщения после назначения юриста
  async def send_fin_mes(manager_id):
    if not(manager_id):
      return

    subject=f"Создана карточка Фин.Услуг: {form.ov['firm']}, ИНН: {form.ov['inn']}"
    message=f"{form.manager['name']} назначил(а) Вас менеджером фин.услуг в карточке <a href='{form.s.config['system_url']}edit_form/user_fin/{form.id}'>{form.ov['firm']}</a>"
    to_hash={
      manager_id: 1,
      7576: 1 # pzm
    }

    if manager_id:=form.ov.get('manager_fin'):
      manager=await get_manager( id=manager_id, db=form.db)
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
    # end_send_fin_mes

  values=form.R.get('values')
  if values:
    old_manager_fin=0
    #old_manager_to2=0
    old_group_id=0
    if form.ov:
      old_manager_fin=form.ov['manager_fin']
      #old_manager_to2=form.ov['manager_to2']
      old_group_id=form.ov['group_id']

    new_manager_fin=values['manager_fin']
    #new_manager_to2=values['manager_to2']
    new_group_id=values['group_id']

    #print(f"new_manager_to: {new_manager_to} ; old_manager_to: {old_manager_to}")
    if new_manager_fin and int(new_manager_fin)!=old_manager_fin:
      await send_fin_mes(int(new_manager_fin))



    if new_group_id and int(new_group_id)!=old_group_id:
      fin_group=await form.db.query(
        query="select header, owner_id from manager_group where id=%s",
        values=[new_group_id],
        onerow=1,
      )
      if fin_group:
        subject=f"Изменена группа фин. услуг: {form.ov['firm']}, ИНН: {form.ov['inn']}"
        message=f"Только что <b>{form.manager['name']}</b> установил(а) группу фин. услуг <b>{fin_group['header']}</b><br>"+\
        f"В карте Юр.услуг: <a href='{form.s.config['system_url']}edit_form/teamwork_ofp/{form.id}'>{form.ov['firm']}</a>"
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
        if fin_group['owner_id']:
          to_hash[fin_group['owner_id']]=1

        to=await get_email_list_from_manager_id(form.db, to_hash)
        if len(to):
          send_mes(
            from_addr='info@fascrm.ru',
            to=','.join(to.keys()),
            subject=subject,
            message=message
          )



async def after_save(form):
  ov=form.ov
  manager_id=exists_arg('values;manager_id', form.R)
  user_id=exists_arg('user_id', form.ov)
  if manager_id and form.manager['login'] in ('akulov','sed','pzm'):
    await form.db.query(
      query='UPDATE user set manager_id=%s where id=%s',
      values=[manager_id,user_id],

    )

  if form.id and form.ov:
    # Проверяем, отправлялось ли ранее сообщение о создании карты, и, если нет, отправляем
    await send_after_create(form)

    # при смене группы фин. услуг, обнуляем менеджера фин. услуг
    new_group_id=exists_arg('values;group_id', form.R)
    if new_group_id: new_group_id=int(new_group_id)
    old_group_id=ov['group_id']
    if new_group_id and new_group_id!=old_group_id:
      await form.db.query(
        query="UPDATE user_fin SET manager_fin=0 WHERE id=%s",
        values=[form.id]
      )

    new_manager_fin=exists_arg('values;manager_fin',form.R)
    
    if new_manager_fin:
        # При назначении нового менеджера фин. услуг -- уведомление этому менеджеру
        new_manager_fin=int(new_manager_fin)
        old_manager_fin=ov['manager_fin']
        #form.pre({'old_manager_fin':old_manager_fin, 'new_manager_fin':new_manager_fin})
        
        if new_manager_fin and old_manager_fin!=new_manager_fin:
          # Уведомление новому менеджеру фин. услуг
          to=[new_manager_fin]
          to_emails=await get_email_list_from_manager_id(form.db, to)

          send_mes(
            from_addr='info@fascrm.ru',
            to=','.join(to_emails.keys()),
            subject=f"На Вас переведена карта фин. услуг {ov['firm']}",
            message=f"<p>Только что {form.manager['name']} перевёл(а) карту Фин. услуг для компании: <b>{ov['firm']}</b>( ИНН: {ov['inn']})</p>"+\
                    f"<p><a href='{form.s.config['system_url']}edit_form/user_fin/{form.id}'>Перейти в карту</a></p>"
          )

    new_underwriter=exists_arg('values;underwriter',form.R)
    if new_underwriter:
      # При назначении нового андеррайтера -- увдомление андеррайтеру
      new_underwriter=int(new_underwriter)
      old_underwriter=ov['underwriter']
      if new_underwriter and new_underwriter!=old_underwriter:
        to=[new_underwriter]
        to_emails=await get_email_list_from_manager_id(form.db, to)
        #print('Андеррайтер:',to_emails)
        send_mes(
          from_addr='info@fascrm.ru',
          to=','.join(to_emails.keys()),
          subject=f"Вы назначены андеррайтером в карте фин. услуг {ov['firm']}",
          message=f"<p>Только что {form.manager['name']} назначил Вас андеррайтером в карте Фин. услуг для компании: <b>{ov['firm']}</b>( ИНН: {ov['inn']})</p>"+\
                  f"<p><a href='{form.s.config['system_url']}edit_form/user_fin/{form.id}'>Перейти в карту</a></p>"
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
      qs['WHERE'].append(f"(wt.manager_id={manager_id} or u.manager_id={manager_id})")
    

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
  'before_search':before_search,

}
