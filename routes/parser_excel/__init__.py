from fastapi import APIRouter, Request #, File, UploadFile, Form, Depends
from config import config as sysconfig

#from lib.engine import s
from .load_parser_from_config import *
# from lib.celery_conf.parser_excel_tasks import parser_excel_load_sync (перенесено в "ленивый" импорт)
from .preload import preload
from .load import load
#from .sync_load_task import sync_load_task

router = APIRouter()





@router.post('/{config}')
async def process_parser_excel(request: Request, config: str, R:dict):
    s = request.state.engine
    from lib.celery_conf.parser_excel_tasks import parser_excel_load_sync  # ← ЛЕНИВЫЙ ИМПОРТ ЗДЕСЬ
    manager = s.request.state.manager
    config_folder=sysconfig.get('config_folder')

    if not(config_folder):
        config_folder='conf'

    arg={'config':config}
    load_result=await load_parser_from_config(config_folder,config_folder, arg)
    parser=load_result[0]
    errors=load_result[1]

    action = R.get('action')
    if action=='init':
        success=(True,False)[len(errors)]


        return {

            'success':success,
            'parser':parser,
            'errors':errors,
        }

    if action == 'preload':
        return await preload(parser, R)

    if action == 'load':
        delay=parser.get('delay')
        if delay:
            R['manager_id']=manager['id']
            task=parser_excel_load_sync.delay(config,R)
            #print('task: ',task)
            return {'success':True, 'message': 'Задача запущена в фоновом режиме','task_id':task.id}
        else:
            return await load(parser, R)
