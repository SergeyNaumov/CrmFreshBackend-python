from fastapi import APIRouter, Request #, File, UploadFile, Form, Depends
from config import config as sysconfig
#from lib.engine import s
from .load_parser_from_config import *
import os, re

from .preload import preload
from .load import load
from .refs import check_refs, create_refs
# Регистрирует фоновый обработчик фото товаров (crm_background).
from lib.svcmsmanager import ds_good_photos  # noqa: F401
router = APIRouter()


def remove_tmp_file(parser, R):
    # Удаляем временный файл предпросмотра (замкнуто на tmp_dir конфига).
    tmp_file=R.get('tmp_file') or R.get('filename') or ''
    tmp_dir=parser.get('tmp_dir') if parser else None
    if not(tmp_file and tmp_dir):
        return {'success':0,'errors':['не указан временный файл']}
    if not(re.match(r'^[a-zA-Z0-9_\-\.]+$',tmp_file)):
        return {'success':0,'errors':['некорректное имя временного файла']}
    full=f"{tmp_dir}/{tmp_file}"
    if os.path.isfile(full):
        try:
            os.remove(full)
        except OSError as e:
            return {'success':0,'errors':[f'не удалось удалить {tmp_file}: {e}']}
    return {'success':1,'errors':[]}


@router.post('/{config}')
async def process_parser_excel(config: str, R:dict, request: Request):

    config_folder=sysconfig.get('config_folder')

    if not(config_folder):
        config_folder='conf'

    project=request.state.project or {}
    manager=request.state.manager or {}
    arg={
        'config':config,
        'project_id':project.get('project_id'),
        'admin_id':manager.get('id'),
    }
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
        return await load(parser, R, request.state.engine.db)

    if action == 'check_refs':
        return await check_refs(parser, R, request.state.engine.db)

    if action == 'create_refs':
        return await create_refs(parser, R, request.state.engine.db)

    if action == 'remove_tmp_file':
        return remove_tmp_file(parser, R)
