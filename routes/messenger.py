from fastapi import APIRouter, Request
from fastapi import WebSocket, WebSocketDisconnect

from lib.engine import s
from config import config
import json

messenger_rules = config['messenger_rules']

router = APIRouter()




class ConnectionManager:
	def __init__(self):
		self.active_connections: List[WebSocket] = []
		self.active_connections_hash={}
		self.id_by_socket={}
	async def connect(self, websocket: WebSocket, socket_name:str):
		await websocket.accept()
		#print('connect: ',websocket, socket_name)
		self.active_connections.append(websocket)

		if not(socket_name in self.active_connections_hash):
			self.active_connections_hash[socket_name]=[]

		self.active_connections_hash[socket_name].append(websocket)
		#print('active_connections:',self.active_connections)
		#print('active_connections_hash:',self.active_connections_hash)
	def disconnect(self, websocket: WebSocket,socket_name:str):
		...
		#print('dicconnect:',socket_name)


		if socket_name in self.active_connections_hash:
			if websocket in self.active_connections_hash[socket_name]:
				self.active_connections_hash[socket_name].remove(websocket)
		#else:
			#print('not manager')
		self.active_connections.remove(websocket)


	async def send_personal_message(self, message: str, websocket: WebSocket):
		...
		#await websocket.send_text(message)

	async def broadcast(self, message: str):
		...
		#for connection in self.active_connections:
		#  await connection.send_text(message)

connector_manager = ConnectionManager()

# websocket для сообщений
@router.websocket("/ws/{socket_name}")
async def websocket_endpoint(websocket: WebSocket, socket_name: str):
	#print(f'create websocket: {socket_name}')
	await connector_manager.connect(websocket,socket_name)

	try:
		while True:
			data = await websocket.receive_text()
			try:
				R = json.loads(data)
				
				if R['action']=='send_message':
					messenger_rules['send'](s,R)

			except ValueError as e:
				pass
		#eeweewew
          #await manager.send_personal_message(f"Your wrote: {data}",websocket)
          #await manager.broadcast(f"Client #{client_id} says: {data}",websocket)

	except WebSocketDisconnect:
		connector_manager.disconnect(websocket,socket_name)
		await connector_manager.broadcast(f"client  left the chat")

# получаем кол-во новых сообщений
@router.get('')
async def init_messenger():
	r = await messenger_rules['init'](s)
	return r
	#config['messenger_rules']['init']()

# список чатов
@router.get('/chatlist')
async def get_chatlist():
	return messenger_rules['chat_list'](s)

# получение списка сообщений в чате
@router.get('/chat/{user_id}')
async def get_chat(user_id: int):
	return messenger_rules['get_chat'](s,user_id)

# загрузка "вперёд"
@router.get('/chat-forward/{user_id}/{last_id}')
async def get_forward(user_id:int, last_id:int):
	return messenger_rules['get_chat'](s,user_id,last_id)

# отправка сообщения
@router.post('/send')
async def send(R: dict):
	return messenger_rules['send'](s,R)


@router.get('/connects')
async def get_chatlist():
	#print('manager.active_connections:',connector_manager.active_connections_hash)
	return {'active_connections':s.manager['id']}
"""
curl -X POST  -H 'Content-Type: application/json' -d '{"message":"Сообщение от пользователя...","user":{id:37}}'



curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"message":"Сообщение от пользователя...", "shop_id": 1, "user_id":37}' \
  http://localhost:5000/messenger/local-send

curl -d "message=Сообщение от пользователя&shop_id=1&user_id=38" -X POST http://localhost:5000/messenger/local-send
"""

@router.get('/get-socket-name')
async def get_socket_name():
	return messenger_rules['get_socket_name'](s.shop_id,s.manager['id'])

# приём локальных сообщений
@router.post('/local-send')
async def from_script(R:dict):
	#print('R:',R)
	socket_name='1|1' # для отладки. менеджер, которому отправляем
	shop_id=R['shop_id']
	user_id=R['user_id']
	message=R['message']
	#print('local_send:', shop_id, user_id, message)
	#print('connections_hash:',connector_manager.active_connections_hash)
	
	result= await messenger_rules['script_send_to_manager'](s,shop_id,user_id, message, connector_manager.active_connections_hash)
	#print('result:',result)
	return {'success':True, "result":result}
	# for sock_id in manager.active_connections_hash:
	# 	if sock_id==manager_id:
	# 		for websocket in manager.active_connections_hash[manager_id]:
	# 			# Сохраняем сообщение от для менеджера
	# 			s.manager()
	# 			await websocket.send_text(R['message'])
	# 		return f"отправляем {manager_id}" 
			
	#return {'success':True, "result":result}


