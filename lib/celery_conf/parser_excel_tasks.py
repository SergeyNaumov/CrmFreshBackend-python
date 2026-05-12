from .config import celery_app
from pathlib import Path

import sys, re, os, csv

base_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(base_dir))

from db import get_db
#from routes.parser_excel.load_parser_from_config import load_parser_from_config_sync
from libsync.crm_messenger import send_sync as send_to_messenger

def clean_empty_tail(_list):
    # вычищаем пустые значения в конце строки
    new_list=[]
    need_clean=1
    # loop in list _str reverse
    for v in reversed(_list):
        if is_empty(v):
            # значение пустое
            if not(need_clean):
                new_list.append('')
        else:
            need_clean=0
            new_list.append(v)

    new_list.reverse()
    return new_list

def is_empty(s):
    #try:
    if isinstance(s,str) and (re.match('\S',s)) :
        return False
    return True

def is_empty_xls_str(hash_fields):
    # строка xls-файла пустая?
    for k in hash_fields:
        #s=
        if is_empty(hash_fields[k]):
            return True
    return False

def print_error(error):
    return {
        'success':False,
        'errors':[error],
        'data':[]
    }

def go_parse(**xarg):
    errors = []
    db=xarg.get('db')
    filename = xarg.get('filename')
    base_dir = Path(__file__).resolve().parent.parent.parent
    tmp_dir = xarg.get('tmp_dir')
    manager_id = xarg.get('manager_id')


    if tmp_dir.startswith('./'):
        tmp_dir = str(base_dir / tmp_dir[2:])

    full_path = f"{tmp_dir}/{filename}"

    # === ОТЛАДКА НАЧИНАЕТСЯ ===
    print(f"[DEBUG] go_parse вызвана")
    print(f"[DEBUG] filename: {filename}")
    print(f"[DEBUG] tmp_dir: {tmp_dir}")
    print(f"[DEBUG] full_path: {full_path}")
    print(f"[DEBUG] Файл существует: {os.path.exists(full_path)}")
    if os.path.exists(full_path):
        print(f"[DEBUG] Размер файла: {os.path.getsize(full_path)} байт")
    else:
        return print_error(f"Файл не существует по пути: {full_path}")

    hash_fields = xarg.get('hash_fields')
    loopback = xarg.get('loopback')
    before_reduce = xarg.get('before_reduce')
    save_reduce = xarg.get('save_reduce')
    before_loopback = xarg.get('before_loopback')
    data_line_number = xarg.get('data_line_number')
    limit = xarg.get('limit')

        # Определение расширения файла
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ['.xls', '.xlsx', '.csv']:
        send_to_messenger(manager_id,f"Неподдерживаемое расширение файла: {ext}")

    # Чтение данных в виде строк (генератороподобно)
    try:
        if ext == '.xls':
            workbook = xlrd.open_workbook(full_path)
            sh = workbook.sheet_by_index(0)
            rows = (sh.row(row_idx) for row_idx in range(sh.nrows))
        elif ext == '.xlsx':
            wb = load_workbook(full_path, read_only=True)
            sh = wb.active
            rows = sh.iter_rows(values_only=True)
        elif ext == '.csv':
            def open_csv():
                encodings = ['utf-8', 'cp1251', 'latin1']
                for enc in encodings:
                    try:
                        f = open(full_path, 'r', encoding=enc, newline='')
                        sample = f.read(1024)
                        f.close()
                        f = open(full_path, 'r', encoding=enc, newline='')
                        return f, enc
                    except UnicodeDecodeError:
                        continue
                raise Exception("Не удалось определить кодировку CSV")
            
            file_obj, encoding = open_csv()
            print('file_obj создан')
            # Указываем разделитель вручную
            reader = csv.reader(file_obj, delimiter=';')
            print('reader создан')
            rows = reader
            print('rows сформированы')
        else:
            return print_error("Логика не должна доходить до сюда")
    except Exception as e:
        send_to_messenger(manager_id,f"Ошибка при чтении файла {str(e)} (go_parse)")
        return print_error(f"Ошибка при чтении файла {str(e)} (go_parse)")

    # Переменные состояния
    line_number = 0
    data = []
    cnt_empty_str = 0
    inserted_records = 0
    updated_records = 0
    total_records=0
    try:
        for row in rows:

            #print('row: ',row)
            # Пропуск строк до data_line_number
            if data_line_number and line_number < data_line_number:
                line_number += 1
                continue

            total_records+=1
            # Преобразуем строку в список значений
            if ext in ['.xls']:
                values = [str(cell.value) for cell in row]
            elif ext == '.xlsx':
                values = [str(cell) if cell is not None else '' for cell in row]
            elif ext == '.csv':
                values = [str(cell) if cell is not None else '' for cell in row]

            # Формируем hash_str или _str
            hash_str = {}
            _str = []

            for col, v in enumerate(values):
                #v=v.replace('№','&#8470;')
                if hash_fields:
                    if name := hash_fields.get(col):
                        hash_str[name] = v
                else:
                    _str.append(v)
            
            #print('hash_str0:',hash_str)
            if before_loopback:
                before_loopback(hash_str)
            # Логика обработки
            #print('hash_str1:',hash_str)
            #return
            if before_reduce:
                before_reduce(db,filename, hash_str)
            elif loopback:
                #print('LOOPBACK before_reduce:',before_reduce)
                # Проверка на пустую строку
                if is_empty_xls_str(hash_str):
                    cnt_empty_str += 1
                else:
                    cnt_empty_str = 0

                operation = loopback(hash_str)
                if operation == 'update':
                    updated_records += 1
                elif operation == 'insert':
                    inserted_records += 1

            else:
                _str = clean_empty_tail(_str)
                data.append(_str)

            # Прерывание при большом количестве пустых строк
            if cnt_empty_str > 20:
                #print('is_empty str > 20')
                print('parser_excel_tasks: is_empty str > 20')
                break

            line_number += 1
            if limit and line_number >= limit:
                print('parser_excel_tasks: выход по лимиту: ', limit)
                break
        if save_reduce:
            #print('SAVE REDUCE')
            message = save_reduce(db,filename, total_records)

        else:
            message = f"Добавлено записей: {inserted_records}<br>Обновлено записей: {updated_records}"

        send_to_messenger(manager_id, message)

    except Exception as e:
        send_to_messenger(manager_id, f"Ошибка при обработке строки: {str(e)}")
        return print_error(f"Ошибка при обработке строки: {str(e)}")
    finally:
        # Закрытие файла, если это CSV
        if ext == '.csv' and 'file_obj' in locals():
            file_obj.close()

    return {
        'success': len(errors) == 0,
        'errors': errors,
        'loaded_filename': filename,
        'data': data,
        'message': message
    }
def check_before_load_values(errors:list, parser: dict, R:dict):
    # Проверяем, корректен ли этот параметр
    before_load_fields=parser.get('before_load_fields')
    before_load_values=R.get('before_load_values')
    if not(before_load_fields):
        before_load_fields={}

    if len(before_load_fields) and (not(before_load_values) or not(isinstance(before_load_values,dict)) ):
        send_to_messenger(manager_id, 'не корректное значение before_load_values')
        return 'не корректное значение before_load_values'


    if(len(before_load_fields) != len(before_load_values)):
        send_to_messenger(manager_id, 'количество before_load_fields и before_load_values не совпадает')
        return 'количество before_load_fields и before_load_values не совпадает'


    for name in before_load_values:
        if not(re.match('^[a-zA-Z0-9_]+$',name)):
            send_to_messenger(manager_id, f'некорректное имя before_load_fields: {name}')
            return f'некорректное имя before_load_fields: {name}'
    
    # Все проверки пройдены
    return False

def load_sync(db, parser:dict, R:dict):
    manager_id=R.get('manager_id')
    errors=[]; fields=R.get('fields')
    loaded_filename=R.get('loaded_filename')
    data_line_number=R.get('data_line_number')
    result_text=[]
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

    def get_exists(data):
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
                if exists:=db.query(
                        query=f"select * from {parser['work_table']} where {' AND '.join(where) } limit 1",
                        values=values,
                        onerow=1,
                        debug=1
                    ):
                    return exists


        return ''
    
    before_loopback=parser.get('before_loopback')
    def loopback(data):
        if len(data):
            #print('data:',data)
            #print('before_load_fields:',before_load_values)
            #before_loopback(data)
            # Добавляем before_load_values в data
            for name in before_load_values:
                data[name]=before_load_values[name]

            if e:=get_exists(data):
                # запись уже существует, update
                work_table_id=parser['work_table_id']
                exists_id=e[ work_table_id ]
                db.save(
                    table=parser.get('work_table'),
                    data=data,
                    update=1,
                    where=f"{work_table_id}={exists_id}",
                )
                #updated_records+=1
                return 'update'
            else:
                # запись ещё не существует
                db.save(
                    table=parser.get('work_table'),
                    data=data,
                    #debug=1,
                    errors=errors
                )
                #inserted_records+=1
                return 'insert'
        #return f"Добавлено записей: {inserted_records}<br>Обновлено записей: {updated_records}"
            
    #delay=parser.get('delay')

    save_reduce=parser.get('save_reduce')
    before_reduce=parser.get('before_reduce')

    message=go_parse(
        db=db,
        filename=loaded_filename,
        hash_fields=hash_fields,
        tmp_dir=parser['tmp_dir'],
        data_line_number=data_line_number,
        before_loopback=parser.get('before_loopback'),
        before_reduce=before_reduce,
        save_reduce=save_reduce,
        loopback=loopback,
        result_text=result_text,
        manager_id=manager_id
    )
    
    return {
        'success':(True,False)[len(errors)>0],
        'errors':errors,
        'message':message
    }

@celery_app.task()
def parser_excel_load_sync(config_name: str, R: dict):
    from routes.parser_excel.load_parser_from_config import load_parser_from_config_sync  # ← ЛЕНИВЫЙ ИМПОРТ ЗДЕСЬ
    db = get_db(sync=1)

    parser,errors = load_parser_from_config_sync('conf', 'conf', {'config':config_name})
    # для отложенной работы компонента: /vue/parser-excel/manager_employee
    print(f'parser_excel_load_sync: parser: {parser}')
    print(f'parser_excel_load_sync: parser: R: {R}')
    print('RUN load_sync...')
    result = load_sync(db,parser, R)
    print(f'parser_excel_load_sync: result: {result}')