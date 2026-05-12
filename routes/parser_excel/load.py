#from lib.engine import s
from db import get_db
from .go_parse import go_parse
import os
import re

def print_error(error):
    return {
        'success':False,
        'errors':[error],
    }

def check_before_load_values(errors:list, parser: dict, R:dict):
    # Проверяем, корректен ли этот параметр
    before_load_fields=parser.get('before_load_fields')
    before_load_values=R.get('before_load_values')
    if not(before_load_fields):
        before_load_fields={}

    if len(before_load_fields) and (not(before_load_values) or not(isinstance(before_load_values,dict)) ):
        return 'не корректное значение before_load_values'


    if(len(before_load_fields) != len(before_load_values)):
        return 'количество before_load_fields и before_load_values не совпадает'

    for name in before_load_values:
        if not(re.match('^[a-zA-Z0-9_]+$',name)):
            return f'некорректное имя before_load_fields: {name}'
    
    # Все проверки пройдены
    return False

async def load(parser:dict, R:dict):
    errors=[]; fields=R.get('fields')
    loaded_filename=R.get('loaded_filename')
    data_line_number=R.get('data_line_number')
    result_text=[]
    db=get_db()

    if not(fields and isinstance(fields,list)):
        errors.append('fields не указано')
    
    if( not(data_line_number or isinstance(data_line_number,int)) ):
        errors.append('data_line_number не указано')

    if not(loaded_filename and re.match('^[a-zA-Z0-9_\-\.]+$',loaded_filename)):
        errors.append('loaded_filename не указан или указан не верно')

    if len(errors):
        return {
            'success':False,
            'errors':errors
        }

    if err:=check_before_load_values(errors, parser,R):
        # если кривые параметры -- отлуп
        return print_error(err)


    hash_fields={}
    for f in fields:
        if selected:=f.get('selected'):
            hash_fields[selected]=f.get('name')

    
    # это пойдёт в loopback как замыкание
    before_load_values=R.get('before_load_values')
    #save_method=parser.get('save_method','insert')
    parser_loopback=parser.get('loopback')
    unique_fields=parser.get('unique_fields',[])
    field_names={}
    for f in parser.get('fields'):
        #print('f: ',f)
        field_names[ f.get('name') ]=f['description']

    async def get_exists(data):
        where=[]
        values=[]
        
        if len(unique_fields):
            #record=""
            for field_name in unique_fields:
                if field_name in data:
                    where.append(f"{field_name}=%s")
                    values.append(data[field_name])
                    #if record:
                    #    record+=' ; '
                    #record+=f"{field_names.get('field_name')}: {data[field_name]}"
            if len(where):
                if exists:=await db.query(
                        query=f"select * from {parser['work_table']} where {' AND '.join(where) } limit 1",
                        values=values,
                        onerow=1,
                        debug=1
                    ):
                    return exists


        return ''
    
    before_loopback=parser.get('before_loopback')
    async def loopback(data):
        if len(data):
            #print('data:',data)
            #print('before_load_fields:',before_load_values)
            await before_loopback(data)
            # Добавляем before_load_values в data
            for name in before_load_values:
                data[name]=before_load_values[name]

            if e:=await get_exists(data):
                # запись уже существует, update
                work_table_id=parser['work_table_id']
                exists_id=e[ work_table_id ]
                await db.save(
                    table=parser.get('work_table'),
                    data=data,
                    update=1,
                    where=f"{work_table_id}={exists_id}",
                )
                #updated_records+=1
                return 'update'
            else:
                # запись ещё не существует
                await db.save(
                    table=parser.get('work_table'),
                    data=data,
                    #debug=1,
                    errors=errors
                )
                #inserted_records+=1
                return 'insert'
        #return f"Добавлено записей: {inserted_records}<br>Обновлено записей: {updated_records}"
            
    #delay=parser.get('delay')
    in_celery_worker = os.environ.get('CELERY_WORKER_RUNNING') == 'true'
    if in_celery_worker:
        # Создаем новый event loop для Celery
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            message = await go_parse(
                filename=loaded_filename,
                hash_fields=hash_fields,
                tmp_dir=parser['tmp_dir'],
                data_line_number=data_line_number,
                loopback=loopback,
                result_text=result_text
            )
        finally:
            loop.close()
    else:

        message=await go_parse(
            filename=loaded_filename,
            hash_fields=hash_fields,
            tmp_dir=parser['tmp_dir'],
            data_line_number=data_line_number,
            #before_loopback=parser.get('before_loopback'),
            loopback=loopback,
            result_text=result_text
        )
    
    return {
        'success':(True,False)[len(errors)>0],
        'errors':errors,
        'message':message
    }