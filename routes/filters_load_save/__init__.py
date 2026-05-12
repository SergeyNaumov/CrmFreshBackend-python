from fastapi import APIRouter, Request
from lib.all_configs import read_config
import json



router = APIRouter()
@router.get('/{config}/load_filters_list')
async def load_filters_list(config: str, request: Request):
    # Получаем список фильтров
    form = await read_config(
        request=request,
        action='load_filters_list',
        config=config,
        script='filters_load_save'
    )
    
    _list=await form.db.query(
        query="""
            SELECT
                id v,concat(header,' ',registered) d
            FROM 
                crm_save_filters
            WHERE
                manager_id=%s and config=%s
            ORDER BY registered desc
        """,
        values=[form.manager['id'],config]
    )
    return {'success': True, 'list':_list}

    
@router.get('/{config}/load_filter/{filter_id}')
async def load_filter(config: str, filter_id:int, request: Request):
    form = await read_config(
        request=request,
        action='load_filter',
        config=config,
        script='filters_load_save'
    )
    json_data = await form.db.query(
        query=f"select json from crm_save_filters where id={filter_id} and config=%s",
        values=[config],
        onevalue=1
    )
    
    if json_data:
        json_data=json.loads(json_data)
    
    return {'success':form.success(), 'errors':form.errors, 'filters_data':json_data}

@router.delete('/{config}/{filter_id}')
async def delete_filter(config: str, filter_id:int, request: Request):
    form = await read_config(
        request=request,
        action='load_filters_list',
        config=config,
        
        script='delete_filter'
    )
    await form.db.query(
        query="DELETE FROM crm_save_filters where id=%s and config=%s and manager_id=%s",
        values=[filter_id,config,form.manager['id']]
    )
    return {'success':form.success(), 'errors':form.errors}

@router.post('/{config}/save_filter')
async def save_filter(config: str, R:dict, request: Request):
    # Получаем список изменений
    form = await read_config(
        request=request,
        action='load_filters_list',
        config=config,
        #id=fk_value,
        R=R,
        script='save_filter'
    )
    header=R.get('header')
    json_data=R.get('json')
    if header and json_data:
        json_data = json.dumps(json_data, ensure_ascii=False)
        await form.db.save(
            table='crm_save_filters',
            data={
                'header': header,
                'json': json_data,
                'manager_id': form.manager['id'],
                'config':config
            },
            debug=1,
        )
    
    #wide_form=False
    #if form.wide_form:
    #    wide_form=True



    return {
        'success':form.success(),
        'errors':form.errors,
    }

