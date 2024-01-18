from fastapi import APIRouter #, File, UploadFile, Form, Depends
from config import config as sysconfig
#from lib.engine import s
from .load_parser_from_config import *

from .preload import preload
from .load import load
router = APIRouter()





@router.post('/{config}')
async def process_parser_excel(config: str, R:dict):

    config_folder=sysconfig.get('config_folder')

    if not(config_folder):
        config_folder='conf'

    arg={'config':config}
    load_result=load_parser_from_config(config_folder,config_folder, arg)
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
        return preload(parser, R)

    if action == 'load':
        return load(parser, R)
