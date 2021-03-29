# для тестирования
from lib.core import is_wt_field,random_filename;
import time,random,re
def from_datetime_get_date(dt):
  rez=re.search('^(\d{4}-\d{2}-\d{2})( \d{2}:\d{2}:\d{2})?$',dt)
  if rez: return rez[1]
  return False


def get_func(s):
  rez=re.search('func:\((.+)\)',s)
  if rez: rez=rez[1]
  else: rez=''
  return rez
  #return rez

def from_datetime_get_date(dt):
  if not dt: return False
  rez=re.search('^(\d{4}-\d{2}-\d{2})( \d{2}:\d{2}(:\d{2})?)?$',dt)
  if rez:
    return rez[0]
  return False

def print_console_error(text):
  print("\033[31m {}" .format(text),"\033[0m")

print('обычный текст')
print_console_error('Ошибка')
print('обычный текст')

# f={
#   'name': 'status',
#   'description': 'Выбор из списка (select_values)',
#   'add_description': 'с цветами',
#   'type': 'select',
#   'values': [{'v': '0', 'd': 'Другое', 'c': '#FFFFFF'}, {'v': '1', 'd': 'Ждем материалы от клиента', 'c': '#CC99FF'}, {'v': '2', 'd': 'Сделать медиаплан', 'c': '#FFFF00'}, {'v': '3', 'd': 'Сделать креатив', 'c': '#FF0000'}, {'v': '4', 'd': 'Работа с сайтом', 'c': '#99CCFF'}, {'v': '5', 'd': 'Мониторить рекламу', 'c': '#CCFFCC'}, {'v': '6', 'd': 'Сделать отчет', 'c': '#FF6600'}, {'v': '7', 'd': 'Работа закончена', 'c': '#DDDDDD'}, {'v': '8', 'd': 'Отправлять напоминание', 'c': '#24FF00'}, {'v': '9', 'd': 'Выставлен счёт', 'c': '#99CCFF'}, {'v': '10', 'd': 'Переговоры по продлению', 'c': '#800080'}, {'v': '11', 'd': 'Сделать конкурентный анализ', 'c': '#84193C'}, {'v': '12', 'd': 'Согласование УТП', 'c': '#164775'}, {'v': '13', 'd': 'Совместная работа', 'c': '#c1f498'}],
#   'tab': 'plain',
#   'orig_type': 'select_values'
# }

# print('random_filename:',random_filename())
#print(re.IGNORECASE)
# path='/1/2/12/15'
# from_path='/1/2'
# to_path='/3/4'

# reg1=re.compile('^'+from_path+'$')
# reg2=re.compile('^'+from_path+'/')
# path = re.sub(reg1,to_path,path)
# path = re.sub(reg2,to_path+'/',path)
# print(path)

#print( len( list(''.split('/')) ) -1 )

