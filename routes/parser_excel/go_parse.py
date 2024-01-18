import xlrd,re
from pprint import pprint

def print_error(error):
    return {
        'success':False,
        'errors':[error],
        'data':[]
    }
def is_empty(s):
    #try:
    if isinstance(s,str) and (re.match('\S',s)) :
        return False
    #elif (isinstance(s,str) or isinstance(s,int)) and s>0

    return True

    #except Exception as e:
    #    print('Ошибка для при проверке ',s,type(s), str(e))
        #quit()

def is_empty_xls_str(hash_fields):
    # строка xls-файла пустая?
    for k in hash_fields:
        #s=
        if is_empty(hash_fields[k]):
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

def parse_str(row):
    _str=[] ; hash_str={} ; col=0
    is_empty_cnt=0

# def get_row_values(row):
#     result=[]
#     for r in row: result.ar.value
        
# def get_hash_fields():
#     result={}
#     fields=[

#         {'name':'doc_number','description':'Номер документа'},
#         {'name':'date','description':'Дата'},

#         {'name':'time','description':'Время'},
#         {'name':'comment','description':'Комментарий'},
#         {'name':'contragent','description':'Контрагент'},
#         {'name':'inn','description':'ИНН'},
#         {'name':'dogovor','description':'Договор'},
#         {'name':'calc_np','description':'УчитыватьНП'},
#         {'name':'calc_avance','description':'Зачитывать аванс'},
#         {'name':'kurs','description':'Курс'},
#         {'name':'var_nalog','description':'ВариантРасчетаНалогов'},
#         {'name':'service_type','description':'Тип услуги'},
#         {'name':'treb','description':'Зачет взаимных требований'},
#         {'name':'version_object','description':'Версия объекта'},
#         {'name':'num_page','description':'№ стр.'},
#         {'name':'type_price','description':'Тип цен'},
#         {'name':'other_income','description':'Статья прочих доходов'},
#         {'name':'nds','description':'НДС'},
#         {'name':'total','description':'Всего'},
#         {'name':'service','description':'Услуга'},
#         {'name':'cnt','description':'Количество'},
#         {'name':'price','description':'Цена'},
#         {'name':'summa','description':'Сумма'},
#         {'name':'np','description':'НП'},
#     ]
#     idx=0
#     for f in fields:
#         result[idx]=f['name']
#         idx+=1

#     return result


def go_parse(**xarg):
    errors=[]
    filename=xarg.get('filename')
    tmp_dir=xarg.get('tmp_dir')
    full_path=f"{tmp_dir}/{filename}"

    #file_path=xarg.get('file')
    hash_fields=xarg.get('hash_fields')
    loopback=xarg.get('loopback')
    beore_loopback=xarg.get('loopback')
    data_line_number=xarg.get('data_line_number')
    limit=xarg.get('limit')
    try:
        workbook = xlrd.open_workbook(full_path)
        sh = workbook.sheet_by_index(0)
        
    except Exception as e:
        return print_error(f"Ошибка при чтении файла {str(e)} (go_parse)")
    
    # Номер строки в наборе данных, который мы получаем
    line_number=0 
    data=[]
    cnt_empty_str=0

    for row_index in range(sh.nrows):
        if data_line_number and line_number<data_line_number:
            line_number+=1
            continue

        row = sh.row(row_index)
        hash_str={}
        _str=[]
        col=0
        for r in row:
            v=str(r.value)

            if hash_fields:
                # при load-е
                if name:=hash_fields.get(col): hash_str[name]=v
            else:
                # при preload-е
                _str.append(v)
            
            col+=1
        #print('str:',_str)
        if loopback:
            # Loopback
            if is_empty_xls_str(hash_str):
                cnt_empty_str+=1
            #else:
                #if before_loopback:
                #    before_loopback(hash_str)
                #print('hash_str:',hash_str)
            loopback(hash_str)

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

    #dt=df.to_dict(orient='records')
    #dt=df.tolist()
    #print('df:',df)
    idx=0
    #for o in df:
    #   print(o)
    #   data.append(o)

    #   idx+=1
    #   if limit and idx>limit:
    #       break


