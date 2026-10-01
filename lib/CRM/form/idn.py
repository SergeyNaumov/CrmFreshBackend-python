import re

CYRILLIC = re.compile('[а-яА-ЯёЁ]')


# Кириллический домен -> punycode (ASCII). При ошибке возвращаем как есть.
def domain_to_ascii(value):
  s = str(value or '').strip()
  if not s:
    return s
  try:
    return s.encode('idna').decode('ascii')
  except Exception:
    return s


# punycode -> юникод. Домены регистронезависимы, idna-кодек требует нижний
# регистр ACE-меток.
def domain_to_unicode(value):
  s = str(value or '')
  if 'xn--' not in s.lower():
    return s
  try:
    return s.lower().encode('ascii').decode('idna')
  except Exception:
    return s


# Нормализация поискового значения: срезаем протокол/www/путь и переводим
# кириллицу в punycode (idna нельзя применять к полному URL).
def prepare_search_domain(value):
  s = str(value or '').strip()
  s = re.sub(r'^https?://', '', s, flags=re.I)
  s = re.sub(r'^www\.', '', s, flags=re.I)
  s = re.sub(r'/.*$', '', s)
  if CYRILLIC.search(s):
    s = domain_to_ascii(s)
  return s
