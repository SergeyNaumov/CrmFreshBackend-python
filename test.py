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

"""
curl -X POST \
-H "Content-Type: application/json" \
-H "Authorization: Token 0504bf475461ecb2b0223936a54ea814d2fc59d2" \
-H "X-Secret: 60df5c61174703321131e32104288e324733a2f5" \
-d '[ "мск сухонска 11/-89" ]' \
https://cleaner.dadata.ru/api/v1/clean/address


UPDATE manager set password=sha256('123') where login='admin';
"""

