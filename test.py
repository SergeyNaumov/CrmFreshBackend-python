# для тестирования
import re

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

print(from_datetime_get_date('d2020-10-15 05:55:12'))

#get_func('f:ajahj:')
#get_func('func:(now())')