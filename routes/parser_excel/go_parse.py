import os, re
import xlrd
from openpyxl import load_workbook
from pprint import pprint

def print_error(error):
    return {
        'success':False,
        'errors':[error],
        'data':[]
    }

def build_hash_fields(fields):
    # fields (с фронта) -> {индекс колонки: имя поля}
    # index 0 -- валидная колонка, '-1' -- "не выбрано"
    hash_fields={}
    for f in (fields or []):
        if not isinstance(f,dict):
            continue
        try:
            sel=int(f.get('selected'))
        except (TypeError,ValueError):
            continue
        if sel>=0:
            hash_fields[sel]=f.get('name')
    return hash_fields


def is_empty(s):
    if isinstance(s,str) and (re.match(r'\S',s)) :
        return False
    return True

def is_empty_row(hash_str):
    # строка считается пустой, если все её значения пусты
    for k in hash_str:
        if not is_empty(hash_str[k]):
            return False
    return True

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


def open_rows(full_path):
    # Читаем первый лист: .xls -- xlrd, .xlsx -- openpyxl.
    # Возвращаем генератор строк (список строковых значений).
    ext=os.path.splitext(full_path)[1].lower()

    if ext=='.xls':
        workbook=xlrd.open_workbook(full_path)
        sh=workbook.sheet_by_index(0)
        return ([str(c.value) for c in sh.row(i)] for i in range(sh.nrows))

    if ext=='.xlsx':
        wb=load_workbook(full_path, read_only=True, data_only=True)
        sh=wb.active
        def gen():
            for row in sh.iter_rows(values_only=True):
                yield [ '' if v is None else str(v) for v in row ]
        return gen()

    raise Exception(f'неподдерживаемое расширение файла: {ext}')


async def go_parse(**xarg):
    errors=[]
    filename=xarg.get('filename')
    tmp_dir=xarg.get('tmp_dir')
    full_path=f"{tmp_dir}/{filename}"

    hash_fields=xarg.get('hash_fields')
    loopback=xarg.get('loopback')
    data_line_number=xarg.get('data_line_number')
    limit=xarg.get('limit')

    try:
        rows=open_rows(full_path)
    except Exception as e:
        return print_error(f"Ошибка при чтении файла {str(e)} (go_parse)")

    # Номер строки в наборе данных, который мы получаем
    line_number=0
    data=[]
    cnt_empty_str=0

    for row in rows:
        if data_line_number and line_number<data_line_number:
            line_number+=1
            continue

        hash_str={}
        _str=[]
        for col,v in enumerate(row):
            if v is None:
                v=''
            if hash_fields:
                # при load-е
                if name:=hash_fields.get(col): hash_str[name]=v
            else:
                # при preload-е
                _str.append(v)

        if loopback:
            # Полностью пустые строки в БД не пишем: пропускаем, но считаем
            # подряд идущие, чтобы вовремя прервать пустой хвост файла.
            if is_empty_row(hash_str):
                cnt_empty_str+=1
            else:
                cnt_empty_str=0
                await loopback(hash_str)
        else:
            _str=clean_empty_tail(_str)
            data.append(_str)

        if cnt_empty_str>20:
            break

        line_number+=1
        if limit and line_number>=limit:
            break

    return {
        'success':(True,False)[len(errors)>0],
        'errors':errors,
        'loaded_filename':filename,
        'data':data
    }
