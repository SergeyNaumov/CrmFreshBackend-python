from .go_parse import go_parse, build_hash_fields
import re

def print_error(error):
    return {
        'success':False,
        'errors':[error],
    }

def is_empty_value(v):
    # Пустое значение не должно использоваться для поиска уникальной записи
    if v is None: return True
    if isinstance(v,str) and not v.strip(): return True
    return False

def _check_require_any_of(errors:list, parser:dict, fields, hash_fields):
    # Группы колонок, из которых должна быть выбрана хотя бы одна.
    groups=parser.get('require_any_of') or []
    if not(groups and fields):
        return
    descriptions={}
    for f in fields:
        if isinstance(f,dict):
            descriptions[f.get('name')]=f.get('description') or f.get('name')
    selected=set(hash_fields.values())
    for group in groups:
        if not any(name in selected for name in group):
            labels=[descriptions.get(name,name) for name in group]
            errors.append('не выбрана колонка: '+' или '.join(labels))


def check_before_load_values(errors:list, parser: dict, R:dict):    # Проверяем, корректен ли этот параметр
    before_load_fields=parser.get('before_load_fields')
    before_load_values=R.get('before_load_values')
    if not(before_load_fields):
        before_load_fields={}

    if not(isinstance(before_load_values,dict)):
        before_load_values={}

    if len(before_load_fields) and not(before_load_values):
        return 'не корректное значение before_load_values'

    if(len(before_load_fields) != len(before_load_values)):
        return 'количество before_load_fields и before_load_values не совпадает'

    for name in before_load_values:
        if not(re.match('^[a-zA-Z0-9_]+$',name)):
            return f'некорректное имя before_load_fields: {name}'

    # Все проверки пройдены
    return False


async def load(parser:dict, R:dict, db):
    errors=[]; fields=R.get('fields')
    loaded_filename=R.get('loaded_filename')
    data_line_number=R.get('data_line_number')
    if not(fields and isinstance(fields,list)):
        errors.append('fields не указано')

    if( not(data_line_number or isinstance(data_line_number,int)) ):
        errors.append('data_line_number не указано')

    if not(loaded_filename and re.match(r'^[a-zA-Z0-9_\-\.]+$',loaded_filename)):
        errors.append('loaded_filename не указан или указан не верно')

    if len(errors):
        return {
            'success':False,
            'errors':errors
        }

    if err:=check_before_load_values(errors, parser,R):
        # если кривые параметры -- отлуп
        return print_error(err)


    hash_fields=build_hash_fields(fields)

    # требование "хотя бы одна колонка из группы" (напр. id или название рубрики)
    _check_require_any_of(errors, parser, fields, hash_fields)
    if len(errors):
        return {
            'success':False,
            'errors':errors
        }


    # это пойдёт в loopback как замыкание
    before_load_values=R.get('before_load_values')
    if not(isinstance(before_load_values,dict)):
        before_load_values={}
    # серверные значения (project_id и т.п.), не приходят от пользователя
    const_values=parser.get('const_values') or {}
    unique_fields=parser.get('unique_fields',[])
    work_table_id=parser.get('work_table_id')
    before_loopback=parser.get('before_loopback')
    after_item=parser.get('after_item')
    stats={'insert':0,'update':0}

    async def get_exists(data):
        where=[]
        values=[]

        if len(unique_fields):
            for field_name in unique_fields:
                value=data.get(field_name)
                # Пустое уникальное значение не матчим: иначе строка
                # склеится со случайной записью, где поле тоже пустое.
                if is_empty_value(value):
                    return ''
                where.append(f"{field_name}=%s")
                values.append(value)

            if len(where):
                if exists:=await db.query(
                        query=f"select * from {parser['work_table']} where {' AND '.join(where) } limit 1",
                        values=values,
                        onerow=1
                    ):
                    return exists

        return ''

    async def loopback(data):
        if len(data):
            if before_loopback:
                await before_loopback(data, db)

            # серверные значения (project_id) -- перекрывают данные файла
            for name in const_values:
                data[name]=const_values[name]
            # значения, выбранные пользователем до загрузки
            for name in before_load_values:
                data[name]=before_load_values[name]

            exists=await get_exists(data)
            if exists:
                # запись уже существует, update
                exists_id=exists[ work_table_id ]
                await db.save(
                    table=parser.get('work_table'),
                    data=data,
                    update=1,
                    where=f"{work_table_id}={exists_id}",
                    errors=errors
                )
                record_id=exists_id
                stats['update']+=1
            else:
                # запись ещё не существует
                record_id=await db.save(
                    table=parser.get('work_table'),
                    data=data,
                    errors=errors
                )
                stats['insert']+=1

            # пост-обработка строки (характеристики, сбор фото и т.п.)
            if after_item and record_id:
                await after_item(data, record_id, db, errors)

    await go_parse(
        filename=loaded_filename,
        hash_fields=hash_fields,
        tmp_dir=parser['tmp_dir'],
        data_line_number=data_line_number,
        loopback=loopback
    )

    message=f"Создано: {stats['insert']}, обновлено: {stats['update']}"

    after_load=parser.get('after_load')
    if after_load:
        extra=await after_load(db, {'stats':stats,'errors':errors})
        if extra:
            message+=f". {extra}"

    return {
        'success':(True,False)[len(errors)>0],
        'errors':errors,
        'message':message
    }
