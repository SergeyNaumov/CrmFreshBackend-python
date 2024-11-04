from fastapi import APIRouter, Request
#from lib.engine import s
from lib.all_configs import read_config

router = APIRouter()
@router.get('/{config}')
async def init(config: str, request: Request):
    form = await read_config(
        request=request,
        action='get',

        config=config,
        #id=id,
        #R=R,
        script='transfere_cards'
    )

    return {
        'success': True,
        'fields': form.fields,
        'errors':form.errors
    }

@router.post('/{config}')
async def process_transfere(R:dict, request: Request):

    if R['action'] == 'transfere':
        form = await read_config(
            request=request,
            action='transfere',

            config=R['config'],
            #id=id,
            #R=R,
            script='transfere_cards'
        )
        return await form.events['transfere'](form,R)
    else:
        return {'success':False, 'errors':['неизвестный action']}

