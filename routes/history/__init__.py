from fastapi import APIRouter, Request
from lib.all_configs import read_config
import json

async def record_from_json (form, record):
    ...
async def get_times(form, fk_value: int):
    _list = await form.db.query(
        query=f"""
            SELECT 
                t1.{form.work_table_id} id, DATE_FORMAT(t1.{form.field_change_date},%s) registered,
                m.name name,
                 (
                    SELECT t2.id FROM {form.work_table} t2 where t2.{form.foreign_key}={fk_value} and t2.{form.work_table_id}>t1.{form.work_table_id}
                    order by t2.id  limit 1
                ) next_id
            from 
                {form.work_table} t1
                LEFT JOIN manager m ON m.id=t1.manager_id
                
            WHERE
                t1.{form.foreign_key}={fk_value}
            order by t1.{form.work_table_id} desc
        """,
        values=['%d.%m.%y %H:%i:%s']
    )
    for t in _list:
        t['values']=None

    return _list

router = APIRouter()
@router.get('/{config}/{fk_value}/{record_id}')
async def record(config: str, fk_value: int, record_id: int, request: Request):
    # Получаем список изменений
    form = await read_config(
        request=request,
        action='get_record',
        config=config,
        script='get_times'
    )
    
    if len(form.errors):
        # ошибка при чтении конфига
        return {'success':False, 'errors':form.errors}
    
    values=None
    if record_id:
        
        record = await form.db.query(
            query=f"""
                SELECT
                    {form.work_table_id} id, {form.field_change_json} json, {form.field_change_date} registered
                FROM
                    {form.work_table}
                WHERE
                    {form.foreign_key}={fk_value} and {form.work_table_id} = {record_id}
                ORDER BY {form.work_table_id} desc LIMIT 1
            """,
            #debug=1,
            errors=form.errors,
            onerow=1
        )
        if record and record['json']:
            
            values=json.loads(record['json'])
    else:
        # Последнюю запись берём из карты, а не истории
        values = await form.db.query(
            query=f"""
                SELECT
                    *
                FROM
                    {form.orig_table}
                WHERE
                    {form.orig_table_id}={fk_value}
                LIMIT 1
            """,
            #debug=1,
            errors=form.errors,
            onerow=1
        )

    

    if values:
        for field in form.fields:
            #print('f:',field)
            t=field.get('type')
            if name:=field.get('name'):
                v=values.get(name)
                if t in ('select_from_table','filter_extend_select_from_table'):
                    if v:
                        v = await form.db.query(
                            query=f"select {field['header_field']} from {field['table']} where {field['value_field']}=%s",
                            values=[v],
                            onevalue=1
                        )
                    else:
                        v='-'
                
                elif t in ('checkbox','filter_extend_checkbox'):
                    if v:
                        v='вкл'
                    else:
                        v='выкл'
                
                elif t in ('date','filter_extend_date','datetime','filter_extend_datetime'):
                    v=str(v)
                
                elif t in ('select_values'):
                    if v:
                        for item in field['values']:
                            if item['v']==v:
                                v=item['d']
                                break
                    else:
                        v='-'
                values[name]=v

            
        return {'success':True, 'errors':form.errors, 'values':values}
    else:
        return {'success':False, 'errors':[f"запись {record_id} не найдена"]}
        

    

@router.get('/{config}/{fk_value}')
async def get_time_list(config: str, fk_value: int, request: Request):
    # Получаем список изменений
    form = await read_config(
        request=request,
        action='get_history',
        config=config,
        #id=fk_value,
        #R=R,
        script='get_times'
    )
    if not len(form.errors):
        if not hasattr(form,'field_change_json'):
            form.errors.append(f"в конфиге {config} не описано field_change_json")


    if len(form.errors):
        # ошибка при чтении конфига
        return {'success':False, 'errors':form.errors}

    times = await get_times(form, fk_value)
    
    #wide_form=False
    #if form.wide_form:
    #    wide_form=True



    return {
        'success':form.success(),
        'title':form.title,
        'fields':form.fields,
        'log':form.log,
        'errors':form.errors,
        'times':times,
    }

