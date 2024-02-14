from fastapi import APIRouter #, File, UploadFile, Form, Depends
from fastapi import WebSocket, WebSocketDisconnect
from config import config as sysconfig
from lib.engine import s

from .sockets_connector import sockets_connector
from .models import *
from lib.core import gen_pas


router = APIRouter()





@router.get('/init')
async def init():
    # Инициализация GPT для формы
    gpt_list=[] ; fields={} ; WS=None
    need_inited=False
    if gpt_assist_rules:=sysconfig.get('gptassist_rules'):
        rules=gpt_assist_rules(s)
        gpt_list=rules.get('gpt_list',[])

        if len(gpt_list):
            # Данный конфиг указан в настройках GPTAssist
            need_inited=True
            WS=rules.get('WS')

    return {
        'success':True,
        'gpt_list':gpt_list,
        'need_inited':need_inited, # Инициализация должна происходить тольто тогда, когда это необходимо
        'fields':fields,
        'WS':WS
    }


# Отправка задачи в GPT
@router.post('/send-task')
async def send_request_to_gpt(r:RequestTask):
    gpt_assist_rules=sysconfig.get('gptassist_rules')
    task_id=gen_pas(50)
    s.db.save(
        table='crm_gptassist',
        data={
            'task_id':task_id,
            'engine_id': r.engine,
            'temperature':r.temperature,
            'sys_text':r.sys_text,
            'ask':r.ask
        },
        #debug=1
    )
    return {
        'success':True,
        'task_id': task_id
    }

@router.post('/daemon-result')
async def get_result_from_daemon(d: DaemonResult):
    #print('active_connections_hash:',sockets_connector.active_connections_hash);
    #
    task_id=d.task_id
    status=d.status

    if task_id and status:
        if websocket:=sockets_connector.active_connections_hash.get(task_id):
            #print('websocket:',websocket)
            try:
                await websocket.send_text(f"{status}|{d.question}")
                #result['cnt_sockets']+=1
                return {'success':True,'message':f"send ok for socket {task_id}"}
            except Exception as e:
                print(f'error send: {e}')
                return {'success':False, 'error':f"{ str(task_id)}"}
        else:
            return {'success':False, 'error':f"websocket {task_id} not found"}
    else:
        return {'success':False, 'error':f"wrong request"}
        # сокет найден

    return True



# websocket для отравки ответов от GPT
@router.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await sockets_connector.connect(websocket,task_id)

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
        sockets_connector.disconnect(websocket,task_id)
        await sockets_connector.broadcast(f"client  left the chat")