# Карта в модераторе выводится ссылкой (легаси works.conf, filter_code)
async def card_url_filter_code(form, field, row):
  value = row.get('wt__card_url') or ''
  if not value:
    return ''
  return (
    '<a href="http://strateg.crm-dev.ru/edit_form.pl?config=users_inet_projects'
    f'&action=edit&id={value}">{value}</a>'
  )


events = {
  'card_url': {
    'filter_code': card_url_filter_code,
  },
}
