from lib.core import exists_arg
async def get_role(db, manager_id: int):

  manager_table='manager'
  manager_role_table='manager_role'

  r=await db.query(
    query="""
      SELECT
        m2.id
      FROM
        """+manager_table+' m JOIN '+manager_role_table+""" mr ON (m.id = mr.manager_id)
        JOIN """+manager_table+""" m2  ON (m2.id = mr.role AND m.current_role = m2.id)
      WHERE m.id=%s
    """,
    values=[manager_id],
    onevalue=1,
  )

  if r:
    return r
  else:
    return manager_id
def get_triade(num):
	if isinstance(num, int) or isinstance(num, float):
		return '{:,}'.format(num).replace(',', ' ')
	else:
		return num

# получает словарь получателей, 
async def get_email_list_from_manager_id(db, to: dict):
	ids=[]
	for manager_id in to:
		ids.append(str(manager_id))
	
	if len(ids):
		to_emails={}
		for email in await db.query(
			query=f'''
				SELECT
					me.email
				FROM
					manager m
					join manager_email me ON me.manager_id=m.id
				WHERE m.id in ({','.join(ids)}) and me.email<>''
			''',
			massive=1
		):
			#print('email:',email)
			if '@' in email:
				to_emails[email]=True
		#возвращает словарь email-ов их email-ов

		return to_emails
	return {}



async def child_groups(**arg):
	list_hash={}
	db=arg['db']
	if exists_arg('group_id',arg):
		if isinstance(arg['group_id'], int):
			list_hash[arg['group_id']]=1

			_list = await db.query(
				query='select id from manager_group where parent_id=%s',
				values=[arg['group_id']],
				massive=1
			)
			
			for g in _list: list_hash[g]=1

		else:
			for g in arg['group_id']:
				list_hash[g]=1
				#print('g:',g)
				_list = await child_groups(db=arg['db'],group_id=g)
				if _list:
					for gl in _list:
						list_hash[gl]=1
	return list(list_hash.keys())

async def get_manager(**arg):
	where=[]
	values=[]
	if exists_arg('login',arg):
		where.append('m.login=%s')
		values.append(arg['login'])
	
	elif exists_arg('id',arg):
		where.append(f'm.id={arg["id"]}')

	else:
		if exists_arg('errors',arg):
			errors.append('lib/core_crm.py -> get_manager need argument login or argument id')
			return

	manager_table='manager'

	db=arg['db']
	args_for_query={
		'query':f'''
		    SELECT
		      m.*, (mg.owner_id = m.id) owner, concat(mg.path,'/',mg.id) group_path,
		      group_concat(p.pname SEPARATOR ';') options
		    FROM
		      {manager_table} m LEFT JOIN manager_group mg ON (m.group_id = mg.id)
		      left join manager_permissions mp ON (m.id = mp.manager_id)
		      left join permissions p ON (p.id = mp.permissions_id)
		    WHERE
		    	{ ' AND '.join(where)}
		''',
		'values':values,
		'onerow':True
	}

	if exists_arg('errors',arg):
		args_for_query['errors']=arg['errors']	

	if exists_arg('include_gone',arg):
		manager_table='manager_full'

	#print('ERRORS:',errors, exists_arg('errors',arg), arg)
	#quit()

	m = await db.query(
		**args_for_query
	)
	
	# Если не найден менеджер
	if not(m) or not(m['id']): return None

	# роль
	if m and exists_arg('use_role',m) and m['current_role']:
		m=await get_manager(id=m['current_role'],db=arg['db'])

	# руководитель?
	m['owner'] = await db.query(
		query=f'SELECT id from manager_group where owner_id={m["id"]}',
		onevalue=1
	)
	m['CHILD_GROUPS']=[]

	if exists_arg('child_groups',arg) or exists_arg('use_role',arg):
		if m['owner']:
			m['CHILD_GROUPS'] = await child_groups(db=db,group_id=m['owner'])
		elif m['group_id']:
			m['CHILD_GROUPS'] = await child_groups(db=db,group_id=m['group_id'])

	# получаем права менеджера
	if exists_arg('options_hash',arg):
	    new_options={}
	    if m['options']:
		    for o in m['options'].split(';'):
		      new_options[o]=1
	    
	    m['options']=new_options

	return m

async def get_group_options(**arg):
	# get_group_options(db=db, group_id=ID)

	if arg['group_id']:
		result={}
		_list = await arg['db'].query(
			query="select p.pname from manager_group_permissions mgp join permissions p ON p.id=mgp.permissions_id where mgp.group_id=%s",
			values=[arg['group_id']],
			massive=1
		)
		for l in _list:
			result[l]=True
		return result
	else:
		return {}




async def get_owner(**arg):
	db=arg['db']
	cur_manager=exists_arg('cur_manager',arg)
	
	if not(cur_manager) and arg['manager_id']:
		cur_manager=await get_manager(
			id=arg['manager_id'],
			db=db,
			include_gone=exists_arg('include_gone',arg)
		)
		
	if cur_manager: 
		path=f'{cur_manager["group_path"]}/{cur_manager["group_id"]}'
		for group_id in list(reversed(path.split('/'))):

			if not(group_id): next
			r=await db.query(
				query=f'''
					SELECT
						m.id, m.name, m.group_id, m.phone, mg.id group_owner, me.email
					FROM
						manager m
						JOIN manager_group mg ON (m.id=mg.owner_id)
						LEFT JOIN manager_email me ON (me.manager_id=m.id and me.main=1)
					WHERE
						mg.id=%s and m.id>0
					GROUP BY m.id
				''',
				values=[group_id],
				onerow=1
			)
			if r:
				
				if exists_arg('child_groups',arg) or exists_arg('child_groups_hash',arg):
					r['CHILD_GROUPS']=child_groups(db=db,group_id=r['group_owner'])
				
				if exists_arg('child_groups_hash',arg) and len(r['CHILD_GROUPS']):
					child_group_hash={}
					for gr in r['CHILD_GROUPS']:
						child_group_hash[gr]=1
					r['CHILD_GROUPS']=child_group_hash
				return r
	return None

