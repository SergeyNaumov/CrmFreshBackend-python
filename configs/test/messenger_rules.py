from lib.core import date_to_rus
"""
CREATE TABLE `messages` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `ts` timestamp NOT NULL DEFAULT current_timestamp(),
  `sender_id` bigint(20) unsigned NOT NULL DEFAULT 0 COMMENT 'id отправителя: 0-администратор системы, либо chat_id из telegram',
  `recipient_id` bigint(20) unsigned NOT NULL DEFAULT 0 COMMENT 'id получателя: 0-администратор системы, либо chat_id из telegram',
  `readed` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `body` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
"""
async def get_new_messages(db,user_id):
	v = await db.query(
		query="select count(*) from messages where recipient_id=%s and readed=0",
		values=[user_id],
		onevalue=1
	)
	return v

def get_socket_name(manager_id):
	#	изначально именем сокета был manager_id, но потом выяснилось, что
	#	один и тот же менеджер может находиться в разных хостах, поэтому решено было унифицировать

	return str(manager_id)

async def script_send_to_manager(s, user_id:int, message:str, connections_hash):
	result={'message_id':None, 'cnt_sockets':0}
	#print(f"shop_id: {shop_id} user_id: {user_id} message: {message}")
	print('Script_send_to_manager user_id:',user_id, 'message:',message)
	print(connections_hash)
	db=s.db

	user=await db.query(
		query='select * from manager where id=%s',
		values=[user_id],onerow=1
	)
	if not user:
		return {'success':False,'errors':'user not found'}

	# Сохраняем сообщение в базу
	result['message_id']=await  db.save(
		table='messages',
		data={
			'sender_id':0,
			'recipient_id':user_id,
			'readed':0,
			'body': message
		}
	)


	# считаем, сколько новых сообщений
	new_messages = await get_new_messages(db,user_id)
	print('connections_hash:',connections_hash)
	# Отправляем сообщение через websocket
	socket_name = get_socket_name(user_id)
	if socket_name in connections_hash:
		#print(f"send to_socket: {shop_id}.{owner_id}")
		for websocket in connections_hash[socket_name]:
			try:
				await websocket.send_text(f"chat_id:{user_id}:{new_messages}")
				result['cnt_sockets']+=1
				print('send ok')
			except Exception as e:
				print(f'error send: {e}')


	return result

# получение списка чатов (пользователей)
async def get_chatlist(s, manager_id:int):

	#return shop_id
	userlist=await s.db.query(
		query=f'''
			SELECT * from
			(
				SELECT
				    0 id, 'Системные оповещения' name, sum(m.readed=0) new_messages
				FROM
				    messages m
				WHERE
				    m.sender_id=0 and m.recipient_id=1
				GROUP BY m.sender_id
					UNION
				SELECT
					u.id, u.name, sum(m.readed=0) new_messages
				FROM
					manager u
					LEFT JOIN messages m ON m.sender_id=u.id and m.recipient_id={manager_id}
				GROUP BY u.id
			) x
			WHERE id=0

		''',
	)
	return {
		'success':True,
		'chat_list':userlist
	}

# Загрузка чата с пользователем
async def get_chat(s, manager_id:int, user_id:int, last_chat_message_id=0):
	# считаем кол-во непрочитанных сообщений в чате и помечаем их прочитанными (если они есть)
	#print(f'MANAGER_ID: {manager_id}')

	db=s.db

	if user_id:
		user = await db.query(
			query=f"select * from manager where id={user_id}",
			onerow=1
		)
	else:
		user={
			'id':0,
			'name':'Системные оповещения'
		}

	if not user:
		return {'success':False,'error':'Чат не найден!'}

	not_read_messages=await db.query(
		query=f"""
			select
				count(*)
			from
				messages
			where
				sender_id={user['id']} and
				recipient_id={manager_id} and readed=0
			""",
			onevalue=1
	)
	# Если есть непрочитанные сообщения, то помечаем их прочитанными
	if not_read_messages:
		await db.query(
			query=f"""
				UPDATE messages set readed=1
				WHERE
					sender_id={user['id']} and
					recipient_id={manager_id} and readed=0
			"""
		)


	messages=await db.query(
		query=f'''
		select * from
		(

			(
				SELECT
					m.id, m.body, m.ts, 0 your
				FROM
					messages m
				WHERE
					m.id>{last_chat_message_id}  and
					recipient_id={manager_id} and sender_id={user['id']}
				ORDER BY ts
			)
		UNION
			(
				SELECT
					m.id, m.body, m.ts, 1 your
				FROM
					messages m
				WHERE
					m.id>{last_chat_message_id} and
					sender_id={manager_id} and recipient_id={user['id']}
				ORDER BY ts
			)
		) x order by ts

		''',

		values=[]
	)
	for m in messages:
		m['ts']=date_to_rus(m['ts'])
	return {
		'success':True,
		'messages':messages,
		'not_read_messages':not_read_messages,
		'read_only':True
	}

async def init(s, manager_id:int):
	new_messages= await get_new_messages(s.db, manager_id)

	return {
		'success':True,
		'new_messages':new_messages
	}

async def send(s,R):
	# отправляем сообщение в телегу
	#print('send message!')
	if not('chat_id' in R) or not(R['chat_id']):
		return {'success':False,'errors':['отсутствует chat_id']}

	user = await s.db.query(
		query="select * from manager where id=%s",
		values=[R['chat_id']],
		onerow=1
	)
	if not(user):
		return {'success':False,'errors':['Пользователь не найден в системе']}

	if not(user['tg_id']):
		return {'success':False,'errors':['Неизвестный tg_id']}


	if not( 'last_chat_message_id' in R) or not(R['last_chat_message_id']):
		R['last_chat_message_id']=0

	if not(	str(R['last_chat_message_id']).isnumeric() ):
		return {'success':False,'errors':['Неправильный last_chat_message_id']}



	global bot_dict
	#token = s.shop['token']

	#bot = None
	#if token in bot_dict:
	#	bot=bot_dict[token]
	#else:
	#	bot=telebot.TeleBot(token)
	#	bot_dict[token]=bot

	#bot.send_message(user['id'],R['message'])
	# добавляем сообщение в список
	await s.db.save(
		table='messages',
		data={
			'sender_id':s.request.state.manager['id'],
			'recipient_id': user['id'],
			'readed':1,
			'body':R['message']
		}
	)

	cur_chat = await get_chat(s, user['id'], R['last_chat_message_id'])
	#print('cur_chat:',cur_chat)
	return {
		'success':True,
		'messages':cur_chat['messages']
	}

messenger_rules={
	'socket_name':get_socket_name,
	'init':init,
	'chat_list':get_chatlist,
	'get_chat':get_chat,
	'send':send,
	'script_send_to_manager':script_send_to_manager,
	'get_socket_name':get_socket_name
}