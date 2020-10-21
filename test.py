# для тестирования
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

# path='/1/2/12/15'
# from_path='/1/2'
# to_path='/3/4'

# reg1=re.compile('^'+from_path+'$')
# reg2=re.compile('^'+from_path+'/')
# path = re.sub(reg1,to_path,path)
# path = re.sub(reg2,to_path+'/',path)
# print(path)

print( len( list(''.split('/')) ) -1 )

