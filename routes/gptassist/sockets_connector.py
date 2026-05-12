from fastapi import WebSocket, WebSocketDisconnect
class Connection:
	def __init__(self):
		self.active_connections: List[WebSocket] = []
		self.active_connections_hash={}
		self.id_by_socket={}
	async def connect(self, websocket: WebSocket, task_id:str):
		await websocket.accept()

		self.active_connections.append(websocket)

		#if not(task_id in self.active_connections_hash):
		#	self.active_connections_hash[task_id]=[]

		self.active_connections_hash[task_id]=websocket

	def disconnect(self, websocket: WebSocket,task_id:str):
		...



		if task_id in self.active_connections_hash:
			if websocket in self.active_connections_hash[task_id]:
				self.active_connections_hash[task_id].remove(websocket)
		self.active_connections.remove(websocket)


	async def send_personal_message(self, message: str, websocket: WebSocket):
		...
		#await websocket.send_text(message)

	async def broadcast(self, message: str):
		...
		#for connection in self.active_connections:
		#  await connection.send_text(message)

sockets_connector = Connection()