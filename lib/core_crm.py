from lib.core import exists_arg

def get_triade(num):
	if isinstance(num, int) or isinstance(num, float):
		return '{:,}'.format(num).replace(',', ' ')
	else:
		return num

def child_groups(**arg):
	list_hash={}
	db=arg['db']
	if exists_arg('group_id',arg):
		if isinstance(arg['group_id'], int):
			list_hash[arg['group_id']]=1

			_list=db.query(
				query='select id from manager_group where parent_id=%s',
				values=[arg['group_id']],
				massive=1
			)
			
			for g in _list: list_hash[g]=1

		else:
			for g in arg['group_id']:
				list_hash[g]=1
				#print('g:',g)
				_list=child_groups(db=arg['db'],group_id=g)
				if _list:
					for gl in _list:
						lost_hash[gl]=1
	return list(list_hash.keys())

def get_manager(**arg):
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

	m=db.query(
		**args_for_query
	)
	
	# Если не найден менеджер
	if not(m) or not(m['id']): return None

	# роль
	if m and exists_arg('use_role',m) and m['current_role']:
		m=get_manager(id=m['current_role'],db=arg['db'])

	# руководитель?
	m['owner']=db.query(
		query=f'SELECT id from manager_group where owner_id={m["id"]}',
		onevalue=1
	)
	m['CHILD_GROUPS']=[]

	if exists_arg('child_groups',arg) or exists_arg('use_role',arg):
		if m['owner']:
			m['CHILD_GROUPS']=child_groups(db=db,group_id=m['owner'])
		elif m['group_id']:
			m['CHILD_GROUPS']=child_groups(db=db,group_id=m['group_id'])

	# получаем права менеджера
	if True and exists_arg('options_hash',arg):
	    new_options={}
	    for o in m['options'].split(';'):
	      new_options[o]=1
	    
	    m['options']=new_options

	return m

	




def get_owner(**arg):
	db=arg['db']
	cur_manager=exists_arg('cur_manager',arg)
	
	if not(cur_manager) and arg['manager_id']:
		cur_manager=get_manager(
			id=arg['manager_id'],
			db=db,
			include_gone=exists_arg('include_gone',arg)
		)
		print('cur_manager:',cur_manager)
	if cur_manager: 
		path=f'{cur_manager["group_path"]}/{cur_manager["group_id"]}'
		for group_id in list(reversed(path.split('/'))):
			if not(group_id): next
			r=db.query(
				query='SELECT m.*,mg.id group_owner from manager m JOIN manager_group mg ON (m.id=mg.owner_id) where mg.id=%s and m.id>0',
				values=[group_id],
				onerow=1
			)
			if r:
				pass
				if exists_arg('child_groups',arg) or exists_arg('child_groups_hash',arg):
					r['CHILD_GROUPS']=child_groups(db=db,group_id=r['group_owner'])
				
				if exists_arg('child_groups_hash',arg) and len(r['CHILD_GROUPS']):
					child_group_hash={}
					for gr in r['CHILD_GROUPS']:
						child_group_hash[gr]=1
					r['CHILD_GROUPS']=child_group_hash
				return r
	return None

