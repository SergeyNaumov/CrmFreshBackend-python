import os
import re

from lib.CRM.form.idn import domain_to_unicode


# size_project / size_template / paid_on_year -- read-only значения из
# project_hosting, подготовленные событием permissions (form.old_values).
async def size_before_code(form, field):
  values = getattr(form, 'old_values', None) or {}
  v = values.get(field['name'])
  field['html'] = '' if v in (None, '') else str(v)


# Собственные конфиги сущностей (struct + url_generator).
async def exists_conf_before_code(form, field):
  if not form.id:
    return
  list_ = await form.db.query(
    query='SELECT struct_id id, header, table_name FROM struct WHERE project_id=%s',
    values=[form.id],
    errors=form.errors,
  )
  for item in (list_ or []):
    struct_name = item.get('table_name') or ''
    item['struct_name'] = re.sub(r'^struct_\d+_', '', struct_name)
    item['t_url'] = f'/edit_form/url_generator?project_id={form.id}&struct_id={item["id"]}'
  tmpl = os.path.join(os.path.dirname(__file__), 'exists_conf.html')
  field['html'] = form.template(tmpl, form_id=form.id, list=list_ or [])


# Домены в списке -- кнопка «добавить» с предзаполненным проектом.
async def domains_before_code(form, field):
  if form.id:
    field['link_add'] = f'/edit_form/domain?project_id={form.id}'


# filter_code -- как выводить значения в результатах поиска (admin_table).
async def user_id_filter_code(form, field, row):
  v = row.get('d__user_id')
  if not v:
    return ''
  return (
    f'<a href="https://crm.digitalstrateg.ru/edit_form.pl?action=edit&id={v}'
    f'&config=internet_project" target="_blank">{v}</a>'
  )


async def disabled_filter_code(form, field, row):
  if row.get('ph__domain_id'):
    v = str(row.get('ph__disabled') or '0')
    return 'да' if v not in ('0', '', 'None') else 'нет'
  domain_id = row.get('d__domain_id')
  return (
    'отсутствует карта хостинга '
    f'<a href="https://design-b2b.com/admin2/edit_form.pl?action=new'
    f'&config=project_hosting&domain_id={domain_id}" target="_blank">создать</a>'
  )


async def our_domain_filter_code(form, field, row):
  domain = row.get('d__domain') or ''
  our = row.get('d__our_domain')
  if our or domain.endswith('.design-b2b.com'):
    color, label = 'green', 'у нас'
  else:
    color, label = 'red', 'не у нас'
  return (
    f'<span style="display:inline-block;width:10px;height:10px;'
    f'background-color:{color}"></span> {label}'
  )


async def domain_filter_code(form, field, row):
  domain = row.get('d__domain') or ''
  if not domain:
    return ''
  label = domain_to_unicode(domain)
  out = (
    f'<a href="http://{domain}" target="_blank">{label}</a> | '
    f'<a href="/edit_form/domain/{row.get("d__domain_id")}" target="_blank">редактировать</a>'
  )
  if row.get('d__port'):
    out += f' port: {row.get("d__port")}'
  paid = row.get('d__paid_till') or ''
  if paid and re.search(r'[1-9]', str(paid)):
    out += f' оплачен до {paid}'
  return out


async def template_id_filter_code(form, field, row):
  tid = row.get('t__template_id')
  if not tid:
    return ''
  folder = row.get('t__folder') or ''
  nav = (
    f'/admin2/template_editor/navigator.pl?fname={folder}'
    if str(row.get('d__server_type')) == '3'
    else f'/admin/template_editor/navigator.pl?fname={folder}'
  )
  header = row.get('t__header') or tid
  return (
    f'<a href="/edit_form/template/{tid}" target="_blank">{header}</a>'
    f' | <a href="{nav}" target="_blank">к файлам шаблона</a>'
  )


events = {
  'size_project': {'before_code': size_before_code},
  'size_template': {'before_code': size_before_code},
  'paid_on_year': {'before_code': size_before_code},
  'exists_conf': {'before_code': exists_conf_before_code},
  'domains': {'before_code': domains_before_code},
  'user_id': {'filter_code': user_id_filter_code},
  'disabled': {'filter_code': disabled_filter_code},
  'our_domain': {'filter_code': our_domain_filter_code},
  'domain': {'filter_code': domain_filter_code},
  'template_id': {'filter_code': template_id_filter_code},
}
