# Домен менеджера в списке выводим ссылкой (легаси manager.pl: filter_code).
async def domain_filter_code(form, field, row):
  value = row.get('d__domain') or ''
  if not value:
    return ''
  return f'<a href="http://{value}" target="_blank">{value}</a>'


events = {
  'domain': {
    'filter_code': domain_filter_code,
  },
}
