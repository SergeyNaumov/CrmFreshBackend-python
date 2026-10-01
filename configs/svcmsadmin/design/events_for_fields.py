# Ссылки на дизайн и UI выводим в списке ссылками (легаси design: filter_code).
# В легаси у url_ui по ошибке использовался wt__url_design -- исправлено на url_ui.
async def url_design_filter_code(form, field, row):
  value = row.get('wt__url_design') or ''
  if not value:
    return ''
  return f'<a href="{value}" target="_blank">{value}</a>'


async def url_ui_filter_code(form, field, row):
  value = row.get('wt__url_ui') or ''
  if not value:
    return ''
  return f'<a href="{value}" target="_blank">{value}</a>'


events = {
  'url_design': {
    'filter_code': url_design_filter_code,
  },
  'url_ui': {
    'filter_code': url_ui_filter_code,
  },
}
