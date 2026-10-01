import re


# Тип multiconnect_old -- совместимость со старым multicheckbox:
# описание опций задаётся строкой `extended` вида `key;подпись;key2;подпись2;`
# (подпись может содержать HTML, например <hr/> или ссылку), а выбранные
# значения хранятся строкой `;key1;;key2;` (формат менять нельзя).
def parse_extended(extended):
  if not extended:
    return []
  parts = [p.strip() for p in str(extended).split(';')]
  parts = [p for p in parts if p != '']
  values = []
  for i in range(0, len(parts) - 1, 2):
    values.append({'v': parts[i], 'd': parts[i + 1]})
  return values


def split_value(value):
  if not value:
    return []
  return re.findall(r';([^;]+);', str(value))


def join_value(keys):
  return ''.join(f';{k};' for k in (keys or []))
