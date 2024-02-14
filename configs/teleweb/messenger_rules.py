# Правила поведения messenger-а
# для AssistWeb-а
import telebot
from lib.core import date_to_rus

bot_dict={}
async def get_new_messages(db,shop_id,manager_id):
	v=db.query(
		query="select count(*) from messages where recipient_id=%s and shop_id=%s and readed=0",
		values=[manager_id, shop_id],
		onevalue=1
	)
	return v
async def  init(s):
	#print('s:',s.manager)
	
	
	new_messages= await get_new_messages(s.db,s.shop_id,s.manager['id'])

	return {
		'success':True,
		'new_messages':new_messages
	}



# получение списка чатов (пользователей)
def get_chatlist(s):
	
	shop_id=s.shop['id']
	#return shop_id
	userlist=s.db.query(
		query=f'''
			SELECT
				u.id, concat(u.first_name,' ',u.last_name) name, sum(m.readed=0) new_messages
			FROM
				user u
				LEFT JOIN messages m ON m.sender_id=u.tg_id and m.recipient_id={s.manager['id']}
			WHERE u.shop_id={shop_id} and m.shop_id={shop_id}
			GROUP BY u.id
		''',
	)
	return {
		'success':True,
		'chat_list':userlist
	}

# Загрузка чата с пользователем
def get_chat(s,user_id, last_chat_message_id=0):
	# считаем кол-во непрочитанных сообщений в чате и помечаем их прочитанными (если они есть)

	db=s.db
	user=db.query(
		query=f"select * from user where id={user_id} and shop_id={s.shop_id}",
		onerow=1
	)
	if not user:
		return {'success':False,'error':'Чат не найден!'}

	not_read_messages=db.query(
		query=f"""
			select
				count(*)
			from
				messages
			where
				shop_id={s.shop_id} and sender_id={user['tg_id']} and 
				recipient_id={s.manager['id']} and readed=0
			""",
			onevalue=1
	)
	# Если есть непрочитанные сообщения, то помечаем их прочитанными
	if not_read_messages:
		db.query(
			query=f"""
				UPDATE messages set readed=1
				WHERE
					shop_id={s.shop_id} and sender_id={user['tg_id']} and 
					recipient_id={s.manager['id']} and readed=0
			"""
		)


	messages=db.query(
		query=f'''
		select * from
		(
		
			(
				SELECT
					m.id, m.body, m.ts, 0 your
				FROM
					messages m
				WHERE 
					m.id>{last_chat_message_id} and m.shop_id={s.shop_id} and
					recipient_id={s.manager['id']} and sender_id={user['tg_id']}
				ORDER BY ts
			)
		UNION
			(
				SELECT
					m.id, m.body, m.ts, 1 your
				FROM
					messages m
				WHERE 
					m.id>{last_chat_message_id} and m.shop_id={s.shop_id} and
					sender_id={s.manager['id']} and recipient_id={user['tg_id']}
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
		'not_read_messages':not_read_messages
	}

	

def send(s,R):
	# отправляем сообщение в телегу
	#print('send message!')
	if not('chat_id' in R) or not(R['chat_id']):
		return {'success':False,'errors':['отсутствует chat_id']}

	user=s.db.query(
		query="select * from user where id=%s",
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
	token = s.shop['token']
	#print('token:',token)
	#print('bot_dict:',bot_dict)
	bot = None
	if token in bot_dict:
		bot=bot_dict[token]
	else:
		bot=telebot.TeleBot(token)
		bot_dict[token]=bot

	bot.send_message(user['tg_id'],R['message'])
	# добавляем сообщение в список
	s.db.save(
		table='messages',
		data={
			'shop_id': s.shop_id,
			'sender_id':s.manager['id'],
			'recipient_id': user['tg_id'],
			'readed':1,
			'body':R['message']
		}
	)

	cur_chat=get_chat(s, user['id'], R['last_chat_message_id'])
	#print('cur_chat:',cur_chat)
	return {
		'success':True,
		'messages':cur_chat['messages']
	}

async def script_send_to_manager(s, shop_id:int, user_id:int, message:str, connections_hash):
	result={'message_id':None, 'cnt_sockets':0}
	#print(f"shop_id: {shop_id} user_id: {user_id} message: {message}")
	
	db=s.db
	shop = db.query(
		query="""
			select
				s.*
			from
				shop s
				join owner o ON o.id=s.owner_id
			where s.id=%s
		""",
		values=[shop_id],onerow=1
	)
	if not shop:
		return {'success':False,'errors':'shop_id not found'}
	user=db.query(
		query='select * from user where id=%s and shop_id=%s',
		values=[user_id,shop_id],onerow=1
	)
	if not user:
		return {'success':False,'errors':'user not found'}
	
	# Сохраняем сообщение в базу
	result['message_id']=db.save(
		table='messages',
		data={
			'shop_id':shop_id,
			'sender_id':user['tg_id'],
			'recipient_id':shop['owner_id'],
			'readed':0,
			'body': message
		}
	)
	owner_id=shop['owner_id']

	# считаем, сколько новых сообщений
	new_messages = await get_new_messages(db,shop_id,shop['owner_id'])

	# Отправляем сообщение через websocket
	socket_name=get_socket_name(shop_id,owner_id)
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


def get_socket_name(shop_id, manager_id):
	#	изначально именем сокета был manager_id, но потом выяснилось, что
	#	один и тот же менеджер может находиться в разных хостах, поэтому решено было унифицировать

	return f"{shop_id}.{manager_id}"

messenger_rules={
	'socket_name':get_socket_name,
	'init':init,
	'chat_list':get_chatlist,
	'get_chat':get_chat,
	'send':send,
	'script_send_to_manager':script_send_to_manager,
	'get_socket_name':get_socket_name
}
